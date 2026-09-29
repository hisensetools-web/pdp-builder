"""Build imageGrabber.zip to hand to someone: the tool, SETUP.bat, RUN.bat and START_HERE.md,
without tests, git history, secrets or downloaded output.   Usage:  py make_zip.py"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INCLUDE_FILES = ["imageGrabber.py", "requirements.txt", "SETUP.bat", "RUN.bat", "START_HERE.md", "README.md", "CLAUDE.md",
                 "products.example.csv", "prompts.example.txt", ".env.example"]
INCLUDE_DIRS = ["pdpkit", "templates"]
SKIP = {"__pycache__", ".pytest_cache"}

out = ROOT / "imageGrabber.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for name in INCLUDE_FILES:
        if (ROOT / name).is_file():
            z.write(ROOT / name, f"imageGrabber/{name}")
    for d in INCLUDE_DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and not (SKIP & set(p.parts)) and p.suffix not in (".pyc", ".pdf"):
                z.write(p, f"imageGrabber/{p.relative_to(ROOT).as_posix()}")
print(f"{out}  ({out.stat().st_size / 1024:.0f} KB)")
