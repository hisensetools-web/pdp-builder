"""The browser path, end to end, against a page whose carousel slides exist only after a click.

Runs only when Playwright and a Chromium binary are available (META_CHROMIUM_PATH or Playwright's
own install); otherwise it is skipped, never failed.
"""
import http.server
import io
import functools
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from pdpkit import config, scrape

PAGE = """<!doctype html><html><head><title>Carousel</title></head><body>
<div class="t-slds" id="car" style="width:600px;overflow-x:auto;white-space:nowrap">
  <div class="t-slds__item" style="display:inline-block;width:600px"><div class="t-slds__bgimage" data-original="/img/slide1.jpg" style="width:600px;height:400px;background-image:url(/img/slide1.jpg)"></div></div>
  <div class="t-slds__item" style="display:inline-block;width:600px"><div class="t-slds__bgimage" data-original="/img/slide2.jpg" style="width:600px;height:400px"></div></div>
</div>
<button class="t-slds__arrow_right" onclick="addSlide()">next</button>
<img src="/img/protected.jpg" alt="guarded">
<div style="height:2500px"></div>
<img loading="lazy" src="/img/hero.jpg" alt="hero">
<script>
  let n = 3;
  function addSlide(){ if(n>4) return; const d=document.createElement('div'); d.className='t-slds__item'; d.style.cssText='display:inline-block;width:600px';
    d.innerHTML='<div class="t-slds__bgimage" style="width:600px;height:400px;background-image:url(/img/slide'+n+'.jpg)"></div>'; document.getElementById('car').appendChild(d); n++; }
  document.getElementById('car').addEventListener('scroll', () => {
    document.querySelectorAll('[data-original]').forEach(el => { el.style.backgroundImage = 'url(' + el.dataset.original + ')'; });
  });
</script></body></html>"""


def _photo(seed: int) -> bytes:
    from PIL import Image, ImageChops
    base = Image.linear_gradient("L").resize((900, 900))
    grain = Image.effect_noise((900, 900), 10 + seed)
    img = Image.merge("RGB", (base, ImageChops.add(base, grain, scale=1.4), grain))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return buf.getvalue()


class Handler(http.server.BaseHTTPRequestHandler):
    images: dict[str, bytes] = {}

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/polnoch1":
            body = PAGE.encode()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        elif self.path.startswith("/img/") and self.path[5:] in self.images:
            if self.path.endswith("protected.jpg") and str(self.server.server_port) not in (self.headers.get("Referer") or ""):
                self.send_response(403); self.end_headers(); return
            body = self.images[self.path[5:]]
            self.send_response(200); self.send_header("Content-Type", "image/jpeg")
        else:
            self.send_response(404); self.end_headers(); return
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


def browser_usable() -> bool:
    if not scrape.browser_available():
        return False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            kw = {"headless": True}
            if config.CHROMIUM_PATH:
                kw["executable_path"] = config.CHROMIUM_PATH
            p.chromium.launch(**kw).close()
        return True
    except Exception:  # noqa: BLE001
        return False


@unittest.skipUnless(browser_usable(), "Playwright + Chromium not available here")
class BrowserCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Handler.images = {f"slide{i}.jpg": _photo(i) for i in range(1, 5)} | {"hero.jpg": _photo(8), "protected.jpg": _photo(9)}
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/polnoch1"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_every_image_the_visitor_would_see_is_saved(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.multiple(config, MIN_IMAGE_BYTES=1000, GRAB_ALL_IMAGES=True):
            data, out_dir, manifest = scrape.grab(self.url, out_dir=Path(d) / "p")
            names = sorted(m["url"].rsplit("/", 1)[-1] for m in manifest)
            # slides 3 and 4 exist only after the carousel's "next" is clicked; protected.jpg refuses
            # a request without a Referer; hero is below the fold and lazy
            self.assertEqual(names, ["hero.jpg", "protected.jpg", "slide1.jpg", "slide2.jpg", "slide3.jpg", "slide4.jpg"])
            self.assertTrue(all((out_dir / "competitor_imgs" / m["file"]).stat().st_size > 1000 for m in manifest))
            gallery = sorted(m["url"].rsplit("/", 1)[-1] for m in manifest if m["kind"] == "gallery")
            self.assertEqual(gallery, ["slide1.jpg", "slide2.jpg", "slide3.jpg", "slide4.jpg"])


if __name__ == "__main__":
    unittest.main()
