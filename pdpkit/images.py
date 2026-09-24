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
from pathlib import Path

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


def compress(data: bytes, fallback_ext: str = ".jpg", *, max_px: int | None = None, quality: int | None = None,
             fmt: str | None = None, force: bool = False) -> Compressed:
    """Resize + re-encode one image. Never raises: an image we cannot read is passed through.
    max_px / quality / fmt override the .env settings for this call; force ignores PDP_COMPRESS=0."""
    global _warned
    if not config.COMPRESS_IMAGES and not force:
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

    cap = config.IMAGE_MAX_PX if max_px is None else max_px
    q = config.IMAGE_QUALITY if quality is None else quality
    resized = bool(cap) and max(img.size) > cap
    if resized:
        img.thumbnail((cap, cap), Image.LANCZOS)

    fmt = (fmt or config.IMAGE_FORMAT).lower()
    if fmt == "png":
        target, ext, params = "PNG", ".png", {"optimize": True}
    elif fmt == "webp":
        target, ext, params = "WEBP", ".webp", {"quality": q, "method": 6}
    else:
        target, ext, params = "JPEG", ".jpg", {"quality": q, "optimize": True, "progressive": True}

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


# --------------------------------------------------------------------------- whole folders
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".bmp", ".tif", ".tiff")
COMPRESSED_DIR = "compressed"
INDEX_NAME = ".compressed_index.json"
SKIP_DIRS = (COMPRESSED_DIR, "originals", "__pycache__")


def _unique_name(taken: set[str], stem: str, ext: str) -> str:
    name, n = stem + ext, 2
    while name in taken:
        name, n = f"{stem}-{n}{ext}", n + 1
    taken.add(name)
    return name


def compress_folder(folder: Path, *, out: Path | None = None, fmt: str | None = None, quality: int | None = None,
                    max_px: int | None = None, in_place: bool = False, redo: bool = False) -> list[dict]:
    """Compress every image under `folder` (subfolders included) with the heavy preset into one flat
    `folder/compressed/` directory, so the competitor images and whatever Higgsfield produced end up
    light and in one place. A second run only touches files that are new or changed since the last
    one (`.compressed_index.json`). `in_place=True` replaces each source file instead (the original
    is deleted once the lighter file is written)."""
    import json
    import time

    folder = Path(folder)
    fmt = fmt or config.HEAVY_FORMAT
    quality = config.HEAVY_QUALITY if quality is None else quality
    max_px = config.HEAVY_MAX_PX if max_px is None else max_px
    dest = None if in_place else Path(out) if out else folder / COMPRESSED_DIR
    index_path = (dest or folder) / INDEX_NAME
    index: dict = {}
    if not redo and index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            index = {}
    if dest:
        dest.mkdir(parents=True, exist_ok=True)

    sources = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
                     and not any(part in SKIP_DIRS for part in p.relative_to(folder).parts)
                     and (dest is None or dest not in p.parents))
    taken = {p.name for p in dest.iterdir()} if dest else set()
    for entry in index.values():
        taken.discard(entry.get("out", ""))
    results: list[dict] = []
    for src in sources:
        rel = src.relative_to(folder).as_posix()
        st = src.stat()
        prev = index.get(rel)
        if prev and prev.get("size") == st.st_size and prev.get("mtime") == int(st.st_mtime) \
                and (dest is None or (dest / prev.get("out", "")).exists()):
            results.append({"source": rel, "out": prev.get("out", ""), "bytes": prev.get("bytes", 0),
                            "source_bytes": st.st_size, "skipped": True})
            taken.add(prev.get("out", ""))
            continue
        data = src.read_bytes()
        shot = compress(data, src.suffix.lower(), max_px=max_px, quality=quality, fmt=fmt, force=True)
        if dest:
            # keep the subfolder in the name only when two files would otherwise collide
            stem = src.stem
            if prev and prev.get("out"):
                name = prev["out"]
                taken.add(name)
            else:
                name = _unique_name(taken, stem, shot.ext) if stem + shot.ext not in taken \
                    else _unique_name(taken, f"{src.parent.name}-{stem}", shot.ext)
            target = dest / name
            target.write_bytes(shot.data)
        else:
            target = src.with_suffix(shot.ext)
            if shot.note == "original" and target == src:
                name = src.name
            else:
                target.write_bytes(shot.data)
                if target != src:
                    src.unlink()
                name = target.name
            st = target.stat()
            rel = target.relative_to(folder).as_posix()
        results.append({"source": rel, "out": name, "bytes": len(shot.data), "source_bytes": len(data),
                        "size": [shot.width, shot.height], "note": shot.note, "skipped": False})
        index[rel] = {"out": name, "size": st.st_size, "mtime": int(st.st_mtime), "bytes": len(shot.data),
                      "at": int(time.time())}
    try:
        index_path.write_text(json.dumps(index, indent=1), encoding="utf-8")
    except OSError:
        pass
    return results


BAT_NAME = "compress_images.bat"


def write_compress_bat(folder: Path) -> Path:
    """Drop a double-clickable compress_images.bat into a product folder. It runs `pdp.py compress`
    on that folder, so every image in it (competitor_imgs, the Higgsfield output folder, anything
    else you paste in) is compressed into compressed/ without opening a terminal."""
    pdp = config.ROOT / "pdp.py"
    lines = [
        "@echo off",
        "rem Compresses every image in this folder and its subfolders into compressed\ (light WebP by default).",
        "rem Paste your Higgsfield images anywhere in this folder and double-click. Re-running only does new files.",
        "rem Options: compress_images.bat --format jpeg --quality 70 --max-px 1600   |   --redo   |   --in-place",
        'cd /d "%~dp0"',
        f'python "{pdp}" compress "%~dp0." %*',
        "if errorlevel 1 echo.& echo Something went wrong, see above.",
        "pause",
        "",
    ]
    path = Path(folder) / BAT_NAME
    path.write_text("\r\n".join(lines), encoding="utf-8")
    return path
