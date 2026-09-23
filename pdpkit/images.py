"""Compress downloaded images so the folder is ready to use without another pass.

Every image is straightened (EXIF orientation), capped at PDP_IMAGE_MAX_PX on its longest side
and re-encoded as JPEG at PDP_IMAGE_QUALITY. Transparency is flattened onto white, because a
JPEG has no alpha channel and a black background is the usual surprise otherwise.

An image that needs no resizing and re-encodes bigger than what the store served (already
optimised WebP often does) is kept exactly as downloaded: compressing never makes a file worse.

Needs Pillow. Without it every image is saved exactly as downloaded and the run says so once.
"""
from __future__ import annotations

import io
import logging
from dataclasses import dataclass

from . import config

log = logging.getLogger("pdpkit.images")

_warned = False


@dataclass
class Compressed:
    data: bytes
    ext: str
    width: int = 0
    height: int = 0
    original_bytes: int = 0
    note: str = ""          # "" = re-encoded, "original" = kept as downloaded, "no-pillow" / "unreadable"

    @property
    def saved_pct(self) -> int:
        if not self.original_bytes or len(self.data) >= self.original_bytes:
            return 0
        return round(100 * (1 - len(self.data) / self.original_bytes))


def available() -> bool:
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


def compress(data: bytes, fallback_ext: str = ".jpg") -> Compressed:
    """Resize + re-encode one image. Never raises: an image we cannot read is passed through."""
    global _warned
    if not config.COMPRESS_IMAGES:
        return Compressed(data, fallback_ext, original_bytes=len(data), note="original")
    try:
        from PIL import Image, ImageOps
    except ImportError:
        if not _warned:
            log.warning("Pillow is not installed, images are saved as downloaded (pip install pillow)")
            _warned = True
        return Compressed(data, fallback_ext, original_bytes=len(data), note="no-pillow")

    try:
        img = Image.open(io.BytesIO(data))
        img = ImageOps.exif_transpose(img) or img
        img.load()
    except Exception as e:  # noqa: BLE001 - a broken or exotic file must not stop the download
        log.debug("cannot read image (%s); keeping the original bytes", e)
        return Compressed(data, fallback_ext, original_bytes=len(data), note="unreadable")

    cap = config.IMAGE_MAX_PX
    resized = bool(cap) and max(img.size) > cap
    if resized:
        img.thumbnail((cap, cap), Image.LANCZOS)

    fmt = config.IMAGE_FORMAT.lower()
    if fmt == "png":
        target, ext, params = "PNG", ".png", {"optimize": True}
    elif fmt == "webp":
        target, ext, params = "WEBP", ".webp", {"quality": config.IMAGE_QUALITY, "method": 6}
    else:
        target, ext, params = "JPEG", ".jpg", {"quality": config.IMAGE_QUALITY, "optimize": True, "progressive": True}

    if target == "JPEG" and img.mode not in ("RGB", "L"):
        if img.mode in ("RGBA", "LA", "P"):
            rgba = img.convert("RGBA")
            flat = Image.new("RGB", rgba.size, (255, 255, 255))
            flat.paste(rgba, mask=rgba.split()[-1])
            img = flat
        else:
            img = img.convert("RGB")

    buf = io.BytesIO()
    try:
        img.save(buf, target, **params)
    except Exception as e:  # noqa: BLE001
        log.debug("cannot encode image as %s (%s); keeping the original bytes", target, e)
        return Compressed(data, fallback_ext, original_bytes=len(data), note="unreadable")
    out = buf.getvalue()

    if not resized and len(out) >= len(data):
        # nothing to shrink and the store's own encoding is already smaller:
        # don't trade quality for a bigger file
        return Compressed(data, fallback_ext, img.width, img.height, len(data), note="original")
    return Compressed(out, ext, img.width, img.height, len(data))
