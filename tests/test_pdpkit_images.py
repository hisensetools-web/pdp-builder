"""Image compression: resize, re-encode, flatten transparency, never make a file worse."""
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image, ImageChops

from pdpkit import config, images, scrape


def png_bytes(w, h):
    """A photo-like PNG: smooth gradient plus grain, the shape of a real product shot.
    (A flat image with sparse dots is a JPEG worst case and would not represent anything real.)"""
    base = Image.linear_gradient("L").resize((w, h))
    grain = Image.effect_noise((w, h), 18)
    img = Image.merge("RGB", (base, ImageChops.add(base, grain, scale=1.4), grain))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


class CompressTests(unittest.TestCase):
    def test_large_png_is_resized_and_becomes_a_smaller_jpeg(self):
        src = png_bytes(3000, 2000)
        with mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=2048, IMAGE_QUALITY=82, IMAGE_FORMAT="jpeg"):
            out = images.compress(src, ".png")
        self.assertEqual(out.ext, ".jpg")
        self.assertEqual(max(out.width, out.height), 2048)
        self.assertEqual((out.width, out.height), (2048, 1365))      # aspect ratio kept
        self.assertLess(len(out.data), len(src))
        self.assertGreater(out.saved_pct, 0)
        self.assertEqual(Image.open(io.BytesIO(out.data)).format, "JPEG")

    def test_small_image_is_not_upscaled(self):
        src = png_bytes(400, 300)
        with mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=2048, IMAGE_QUALITY=82, IMAGE_FORMAT="jpeg"):
            out = images.compress(src, ".png")
        self.assertEqual((out.width, out.height), (400, 300))

    def test_transparency_is_flattened_onto_white_not_black(self):
        img = Image.new("RGBA", (2400, 2400), (0, 0, 0, 0))      # big enough that a resize happens
        buf = io.BytesIO()
        img.save(buf, "PNG")
        with mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=2048, IMAGE_QUALITY=95, IMAGE_FORMAT="jpeg"):
            out = images.compress(buf.getvalue(), ".png")
        self.assertEqual(out.ext, ".jpg")
        self.assertEqual(Image.open(io.BytesIO(out.data)).convert("RGB").getpixel((1000, 1000)), (255, 255, 255))

    def test_an_already_optimised_small_file_keeps_its_original_bytes(self):
        import random
        random.seed(7)
        noisy = Image.new("RGB", (300, 300))                     # noise: cannot be squeezed further
        noisy.putdata([(random.randrange(256), random.randrange(256), random.randrange(256)) for _ in range(300 * 300)])
        buf = io.BytesIO()
        noisy.save(buf, "JPEG", quality=25)
        small = buf.getvalue()
        with mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=2048, IMAGE_QUALITY=95, IMAGE_FORMAT="jpeg"):
            out = images.compress(small, ".jpg")
        self.assertEqual(out.data, small)
        self.assertEqual(out.note, "original")
        self.assertEqual(out.saved_pct, 0)

    def test_oversized_image_is_always_resized_even_if_the_reencode_is_bigger(self):
        flat = Image.new("RGB", (4000, 4000), (255, 255, 255))   # PNG of flat white is tiny; JPEG will be bigger
        buf = io.BytesIO()
        flat.save(buf, "PNG")
        with mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=2048, IMAGE_QUALITY=95, IMAGE_FORMAT="jpeg"):
            out = images.compress(buf.getvalue(), ".png")
        self.assertEqual(max(out.width, out.height), 2048)
        self.assertEqual(out.note, "")

    def test_unreadable_bytes_pass_through(self):
        with mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=2048, IMAGE_QUALITY=82, IMAGE_FORMAT="jpeg"):
            out = images.compress(b"not an image at all", ".jpg")
        self.assertEqual(out.data, b"not an image at all")
        self.assertEqual(out.note, "unreadable")

    def test_compression_can_be_turned_off(self):
        src = png_bytes(3000, 2000)
        with mock.patch.object(config, "COMPRESS_IMAGES", False):
            out = images.compress(src, ".png")
        self.assertEqual(out.data, src)
        self.assertEqual(out.ext, ".png")

    def test_webp_format_option(self):
        src = png_bytes(2500, 2500)
        with mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=1000, IMAGE_QUALITY=80, IMAGE_FORMAT="webp"):
            out = images.compress(src, ".png")
        self.assertEqual(out.ext, ".webp")
        self.assertEqual(Image.open(io.BytesIO(out.data)).format, "WEBP")


class DownloadCompressionTests(unittest.TestCase):
    def test_downloaded_images_are_written_compressed_and_the_manifest_records_both_sizes(self):
        big = png_bytes(3000, 2000)

        class Resp:
            status_code = 200
            content = big
            headers = {"content-type": "image/png"}

        refs = [scrape.ImageRef("https://s.com/a.png", alt="a", kind="gallery")]
        with tempfile.TemporaryDirectory() as d, \
             mock.patch("pdpkit.scrape._get", return_value=Resp()), \
             mock.patch("pdpkit.scrape.time.sleep"), \
             mock.patch.multiple(config, COMPRESS_IMAGES=True, IMAGE_MAX_PX=2048, IMAGE_QUALITY=82,
                                 IMAGE_FORMAT="jpeg", MIN_IMAGE_BYTES=10):
            manifest = scrape.download_images(mock.Mock(), refs, Path(d))
            written = Path(d) / manifest[0]["file"]
            self.assertEqual(manifest[0]["file"], "gallery_01.jpg")      # png in, jpg out
            self.assertEqual(manifest[0]["size"], "2048x1365")
            self.assertEqual(manifest[0]["source_bytes"], len(big))
            self.assertEqual(manifest[0]["bytes"], written.stat().st_size)
            self.assertLess(manifest[0]["bytes"], manifest[0]["source_bytes"])
            self.assertEqual(Image.open(written).size, (2048, 1365))

    def test_keep_originals_writes_the_untouched_file_alongside(self):
        big = png_bytes(3000, 2000)

        class Resp:
            status_code = 200
            content = big
            headers = {"content-type": "image/png"}

        refs = [scrape.ImageRef("https://s.com/a.png", alt="a", kind="gallery")]
        with tempfile.TemporaryDirectory() as d, \
             mock.patch("pdpkit.scrape._get", return_value=Resp()), \
             mock.patch("pdpkit.scrape.time.sleep"), \
             mock.patch.multiple(config, COMPRESS_IMAGES=True, KEEP_ORIGINALS=True, IMAGE_MAX_PX=2048,
                                 IMAGE_QUALITY=82, IMAGE_FORMAT="jpeg", MIN_IMAGE_BYTES=10):
            scrape.download_images(mock.Mock(), refs, Path(d))
            original = Path(d) / "originals" / "gallery_01.png"
            self.assertTrue(original.is_file())
            self.assertEqual(original.read_bytes(), big)
            self.assertLess((Path(d) / "gallery_01.jpg").stat().st_size, original.stat().st_size)

    def test_cli_flags_override_the_env_settings(self):
        from pdpkit import cli
        import argparse
        before = (config.COMPRESS_IMAGES, config.IMAGE_MAX_PX, config.IMAGE_QUALITY, config.IMAGE_FORMAT, config.KEEP_ORIGINALS)
        try:
            cli._apply_image_opts(argparse.Namespace(no_compress=False, keep_originals=True, max_px=1200,
                                                     quality=70, format="webp"))
            self.assertEqual((config.IMAGE_MAX_PX, config.IMAGE_QUALITY, config.IMAGE_FORMAT), (1200, 70, "webp"))
            self.assertTrue(config.KEEP_ORIGINALS)
            cli._apply_image_opts(argparse.Namespace(no_compress=True))
            self.assertFalse(config.COMPRESS_IMAGES)
        finally:
            (config.COMPRESS_IMAGES, config.IMAGE_MAX_PX, config.IMAGE_QUALITY,
             config.IMAGE_FORMAT, config.KEEP_ORIGINALS) = before

    def test_size_line(self):
        from pdpkit.cli import _size_line
        self.assertIn("smaller", _size_line([{"bytes": 1_000_000, "source_bytes": 4_000_000}]))
        self.assertEqual(_size_line([]), "0 KB")


if __name__ == "__main__":
    unittest.main()
