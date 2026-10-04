"""The team's Google Drive folder is the only place images go."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pdpkit import cli, config


class DriveFolderTests(unittest.TestCase):
    def test_found_under_any_my_drive_root(self):
        with tempfile.TemporaryDirectory() as d:
            my_drive = Path(d) / "My Drive"
            (my_drive / "imageGrabber").mkdir(parents=True)
            with mock.patch.object(config, "drive_roots", return_value=[Path(d) / "nope", my_drive]):
                self.assertEqual(config.find_drive_folder(), my_drive / "imageGrabber")
                self.assertEqual(config.drive_installed(), my_drive)

    def test_missing_shortcut_and_missing_drive_are_told_apart(self):
        with tempfile.TemporaryDirectory() as d:
            my_drive = Path(d) / "My Drive"
            with mock.patch.object(config, "drive_roots", return_value=[my_drive]):
                self.assertIsNone(config.find_drive_folder())
                self.assertIn("not installed", cli._drive_help())
                my_drive.mkdir()
                self.assertIn("no 'imageGrabber' folder", cli._drive_help())

    def test_run_stops_without_drive_unless_local_is_allowed(self):
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(config, "OUTPUT_ROOT", config.LOCAL_OUTPUT), mock.patch.object(config, "ALLOW_LOCAL", False), \
             mock.patch.object(config, "drive_roots", return_value=[Path(d) / "x"]):
            with self.assertRaises(SystemExit) as cm:
                cli._require_output()
            self.assertIn("Google Drive for Desktop", str(cm.exception))
            self.assertIn("PDP_ALLOW_LOCAL", str(cm.exception))

    def test_old_local_output_is_moved_into_drive(self):
        with tempfile.TemporaryDirectory() as d:
            local, drive = Path(d) / "pdp_output", Path(d) / "My Drive" / "imageGrabber"
            (local / "fall-tumbler" / "custom-images").mkdir(parents=True)
            (local / "fall-tumbler" / "custom-images" / "gallery_01.jpg").write_bytes(b"x")
            (local / "skull-candle-warmer").mkdir()
            (drive / "skull-candle-warmer").mkdir(parents=True)        # already in Drive: left alone
            with mock.patch.object(config, "OUTPUT_ROOT", drive), mock.patch.object(config, "LOCAL_OUTPUT", local), \
                 mock.patch.object(config, "OUTPUT_IS_DRIVE", True):
                cli._require_output()
            self.assertTrue((drive / "fall-tumbler" / "custom-images" / "gallery_01.jpg").is_file())
            self.assertFalse((local / "fall-tumbler").exists())
            self.assertTrue((local / "skull-candle-warmer").exists())   # not clobbered
            self.assertTrue(local.exists())                             # not empty, so kept


if __name__ == "__main__":
    unittest.main()


class DesktopCopyTests(unittest.TestCase):
    def test_product_folder_is_copied_and_recopied_only_when_changed(self):
        from pdpkit import images
        with tempfile.TemporaryDirectory() as d:
            drive = Path(d) / "My Drive" / "imageGrabber" / "fall-tumbler"
            (drive / "custom-images").mkdir(parents=True)
            (drive / "custom-images" / "gallery_01.jpg").write_bytes(b"abc")
            (drive / "custom-images" / "originals").mkdir()
            (drive / "custom-images" / "originals" / "gallery_01.png").write_bytes(b"big")
            (drive / "product_summary.md").write_text("x")
            desk = Path(d) / "Desktop" / "imageGrabber images"
            copy = images.mirror_product(drive, desk)
            self.assertEqual(copy, desk / "fall-tumbler")
            self.assertEqual((copy / "custom-images" / "gallery_01.jpg").read_bytes(), b"abc")
            self.assertTrue((copy / "product_summary.md").is_file())
            self.assertFalse((copy / "custom-images" / "originals").exists())      # originals are not mirrored
            first = (copy / "custom-images" / "gallery_01.jpg").stat().st_mtime_ns
            images.mirror_product(drive, desk)
            self.assertEqual((copy / "custom-images" / "gallery_01.jpg").stat().st_mtime_ns, first)   # unchanged: untouched
            (drive / "custom-images" / "gallery_02.jpg").write_bytes(b"new")
            images.mirror_product(drive, desk)
            self.assertTrue((copy / "custom-images" / "gallery_02.jpg").is_file())

    def test_copy_is_skipped_when_off_or_when_the_folder_is_the_copy(self):
        from pdpkit import images
        with tempfile.TemporaryDirectory() as d:
            desk = Path(d) / "Desktop" / "imageGrabber images"
            (desk / "thing").mkdir(parents=True)
            self.assertIsNone(images.mirror_product(desk / "thing", desk))
            self.assertIsNone(images.mirror_product(desk / "thing", None))


class CopyOnSkipTests(unittest.TestCase):
    def test_already_grabbed_products_are_copied_to_the_desktop_too(self):
        from pdpkit import batch
        with tempfile.TemporaryDirectory() as d:
            drive = Path(d) / "drive"; desk = Path(d) / "desk"
            (drive / "fall-tumbler" / "custom-images").mkdir(parents=True)
            (drive / "fall-tumbler" / "custom-images" / "gallery_01.jpg").write_bytes(b"x")
            (drive / "fall-tumbler" / "product_summary.json").write_text('{"url": "https://s.com/products/fall"}')
            with mock.patch.object(config, "OUTPUT_ROOT", drive), mock.patch.object(config, "COPY_ROOT", desk), \
                 mock.patch("pdpkit.scrape.make_session"):
                results = batch.process([batch.Row("Fall Tumbler", "https://s.com/products/fall", 0)])
            self.assertEqual(results[0].status, "skipped")
            self.assertTrue((desk / "fall-tumbler" / "custom-images" / "gallery_01.jpg").is_file())
