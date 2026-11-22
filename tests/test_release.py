"""Exercise distribution integrity and failures that must block publication."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_release", ROOT / "scripts/build_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        for name in ["VERSION", "pet.json", "spritesheet.webp", "LICENSE", "qa/release.json"]:
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        self.version = (self.root / "VERSION").read_text().strip()
        self.tag = f"v{self.version}"
        (self.root / "releases").mkdir()
        shutil.copyfile(ROOT / f"releases/{self.tag}.txt", self.root / f"releases/{self.tag}.txt")
        self.out = Path(self.tmp.name) / "dist"

    def test_package_contains_exact_public_files_and_is_reproducible(self):
        first = release.build_release(self.root, self.out, self.tag)
        second = release.build_release(self.root, self.out / "again", self.tag)
        self.assertEqual(first["archive_sha256"], second["archive_sha256"])
        with zipfile.ZipFile(self.out / first["archive"]) as zipped:
            self.assertEqual(set(zipped.namelist()), {"lvk-rabbit/pet.json", "lvk-rabbit/spritesheet.webp", "lvk-rabbit/LICENSE", "lvk-rabbit/INSTALL.txt"})
            self.assertEqual(zipped.read("lvk-rabbit/spritesheet.webp"), (self.root / "spritesheet.webp").read_bytes())
            self.assertEqual(json.loads(zipped.read("lvk-rabbit/pet.json"))["id"], "lvk-rabbit")
        self.assertEqual((first["used_cells"], first["transparent_unused_cells"]), (74, 14))

    def test_wrong_tag_stops_before_output(self):
        with self.assertRaisesRegex(ValueError, "Tag does not match"):
            release.build_release(self.root, self.out, "v999.0.0")
        self.assertFalse(self.out.exists())

    def test_changed_artwork_requires_new_approval_hash(self):
        p = self.root / "qa/release.json"
        qa = json.loads(p.read_text()); qa["spritesheet_sha256"] = "0" * 64
        p.write_text(json.dumps(qa))
        with self.assertRaisesRegex(ValueError, "approved QA hash"):
            release.build_release(self.root, self.out)

    def test_opaque_unused_cell_is_rejected_even_with_updated_hash(self):
        p = self.root / "spritesheet.webp"
        with Image.open(p) as im:
            atlas = im.convert("RGBA")
        atlas.putpixel((7 * 192 + 20, 20), (255, 255, 255, 255))
        atlas.save(p, lossless=True, exact=True)
        q = self.root / "qa/release.json"; qa = json.loads(q.read_text())
        qa["spritesheet_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest(); q.write_text(json.dumps(qa))
        with self.assertRaisesRegex(ValueError, "nontransparent cell"):
            release.build_release(self.root, self.out)

    def test_missing_sprite_version_is_rejected(self):
        p = self.root / "pet.json"; meta = json.loads(p.read_text()); meta.pop("spriteVersionNumber")
        p.write_text(json.dumps(meta))
        with self.assertRaisesRegex(ValueError, "spriteVersionNumber"):
            release.build_release(self.root, self.out)


if __name__ == "__main__":
    unittest.main()
