"""A landing page (no /products/ in the URL) must still yield the product's own gallery.

Shaped like tykapryde.com/the-sol-light: a custom page whose top scroller holds the product
images, with marketing images further down and a related-products carousel at the bottom.
"""
import unittest
from unittest import mock

from pdpkit import scrape

LANDING_URL = "https://tykapryde.com/the-sol-light"
LANDING_HTML = """
<!doctype html><html><head>
<title>The Sol Light</title>
<link rel="canonical" href="https://tykapryde.com/the-sol-light">
<meta property="og:image" content="https://tykapryde.com/cdn/shop/files/social-share.jpg">
</head><body>
  <header class="site-header"><img src="/cdn/shop/files/logo-wordmark.jpg" alt="logo"></header>

  <div class="product-gallery swiper">
    <img src="/cdn/shop/files/sol_front_1200x.jpg" alt="Sol Light front">
    <img data-src="/cdn/shop/files/sol_side_1200x.jpg" alt="Sol Light side">
    <img srcset="/cdn/shop/files/sol_desk_600x.jpg 600w, /cdn/shop/files/sol_desk_1600x.jpg 1600w" alt="on a desk">
  </div>

  <section class="benefits"><img src="/cdn/shop/files/benefit-focus.jpg" alt="focus infographic"></section>
  <section class="testimonial-slider"><img src="/cdn/shop/files/happy-student.jpg" alt="student"></section>

  <section class="related-products carousel">
    <a href="/products/sol-desk-mat"><img src="/cdn/shop/files/other-product.jpg" alt="mat"></a>
  </section>

  <form action="/cart/add"><a href="/products/sol-study-light">View product</a></form>
  <script>var meta = {"product":{"handle":"sol-study-light"}};
  window.routes = "/products/sol-study-light";</script>
</body></html>
"""

PRODUCT_JSON = {"product": {
    "id": 9, "title": "Sol Study Light", "handle": "sol-study-light", "vendor": "Tykapryde",
    "body_html": "<p>Focus light.</p>", "options": [{"name": "Color", "values": ["White"]}],
    "variants": [{"id": 1, "title": "White", "price": "49.00", "available": True}],
    "images": [
        {"src": "https://tykapryde.com/cdn/shop/files/sol_front.jpg?v=1", "alt": "front"},
        {"src": "https://tykapryde.com/cdn/shop/files/sol_side.jpg?v=1", "alt": "side"},
        {"src": "https://tykapryde.com/cdn/shop/files/sol_scroller_3.jpg?v=1", "alt": "third"},
        {"src": "https://tykapryde.com/cdn/shop/files/sol_scroller_4.jpg?v=1", "alt": "fourth"},
    ]}}


class HandleDiscoveryTests(unittest.TestCase):
    def test_finds_the_product_a_landing_page_is_built_around(self):
        self.assertEqual(scrape.find_product_handle(LANDING_HTML), "sol-study-light")

    def test_canonical_to_a_product_page_wins_over_frequency(self):
        html = ('<link rel="canonical" href="https://s.com/products/the-real-one">'
                '<a href="/products/other">x</a><a href="/products/other">y</a>')
        self.assertEqual(scrape.find_product_handle(html), "the-real-one")

    def test_no_product_links_at_all(self):
        self.assertIsNone(scrape.find_product_handle("<html><body>nothing here</body></html>"))

    def test_collection_and_asset_paths_are_not_handles(self):
        self.assertIsNone(scrape.find_product_handle('<a href="/collections/all/products/">x</a>'
                                                     '<script src="/products/index.js"></script>'))


class GalleryContainerTests(unittest.TestCase):
    def setUp(self):
        from bs4 import BeautifulSoup
        self.soup = BeautifulSoup(LANDING_HTML, "html.parser")

    def _img(self, alt):
        return self.soup.find("img", alt=alt)

    def test_scroller_images_count_as_gallery(self):
        self.assertTrue(scrape.in_gallery_container(self._img("Sol Light front")))
        self.assertTrue(scrape.in_gallery_container(self._img("on a desk")))

    def test_marketing_and_furniture_do_not(self):
        self.assertFalse(scrape.in_gallery_container(self._img("focus infographic")))
        self.assertFalse(scrape.in_gallery_container(self._img("logo")))

    def test_related_products_carousel_does_not(self):
        self.assertFalse(scrape.in_gallery_container(self._img("mat")))

    def test_a_testimonial_slider_is_not_the_product_gallery(self):
        self.assertFalse(scrape.in_gallery_container(self._img("student")))


class LandingPageGrabTests(unittest.TestCase):
    def test_grab_uses_the_discovered_products_json_for_the_gallery(self):
        calls = []

        class Resp:
            def __init__(self, text, json_body=None, ctype="text/html"):
                self.status_code, self.text, self._json = 200, text, json_body
                self.headers = {"content-type": ctype}

            def raise_for_status(self):
                pass

            def json(self):
                if self._json is None:
                    raise ValueError("not json")
                return self._json

        def fake_get(session, url, **kw):
            calls.append(url)
            if url.endswith("/products/sol-study-light.json"):
                return Resp("{}", PRODUCT_JSON, "application/json")
            if url.endswith(".json"):
                return Resp("<html>not found</html>")          # the landing URL has no product JSON
            return Resp(LANDING_HTML)

        with mock.patch("pdpkit.scrape._get", side_effect=fake_get), \
             mock.patch("pdpkit.scrape.download_images", return_value=[]) as dl, \
             mock.patch("pdpkit.scrape.Path.write_text"), mock.patch("pdpkit.scrape.Path.mkdir"):
            data, _, _ = scrape.grab(LANDING_URL, session=mock.Mock())

        self.assertIn("https://tykapryde.com/products/sol-study-light.json", calls)
        self.assertEqual(data.handle, "sol-study-light")
        self.assertEqual(data.title, "Sol Study Light")

        saved = [r for r in dl.call_args[0][1]]                 # what would be downloaded
        gallery = [r.url for r in saved if r.kind == "gallery"]
        # the four real product images, ahead of everything else
        for name in ("sol_front.jpg", "sol_side.jpg", "sol_scroller_3.jpg", "sol_scroller_4.jpg"):
            self.assertIn(f"https://tykapryde.com/cdn/shop/files/{name}", gallery)
        # the scroller's own <img> tags count too, and marketing images do not
        self.assertIn("https://tykapryde.com/cdn/shop/files/sol_desk.jpg", gallery)
        self.assertNotIn("https://tykapryde.com/cdn/shop/files/benefit-focus.jpg", gallery)
        self.assertNotIn("https://tykapryde.com/cdn/shop/files/other-product.jpg", gallery)

    def test_without_discovery_the_gallery_would_have_been_one_share_image(self):
        refs = scrape.extract_image_refs(LANDING_HTML, LANDING_URL, None)
        gallery = [r.url for r in refs if r.kind == "gallery"]
        self.assertIn("https://tykapryde.com/cdn/shop/files/sol_front.jpg", gallery)   # container detection alone
        self.assertNotIn("https://tykapryde.com/cdn/shop/files/benefit-focus.jpg", gallery)


if __name__ == "__main__":
    unittest.main()
