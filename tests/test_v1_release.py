"""Check compatibility packaging without permitting artwork drift."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from PIL import Image
import unittest
import test_release
ROOT = test_release.ROOT
sys.path.insert(0, str(ROOT / 'scripts'))
from build_v1_release import build_v1_release
import shutil


class V1ReleaseTests(unittest.TestCase):
    def setUp(self):
        test_release.ReleaseTests.setUp(self)
        shutil.copytree(ROOT / 'compatibility/v1', self.root / 'compatibility/v1')

    def test_v1_layouts_reproducibility_and_counts(self):
        report = build_v1_release(self.root, self.out, self.tag + '-v1')
        again = build_v1_release(self.root, self.out / 'again')
        self.assertEqual(report, again)
        self.assertEqual((report['used_cells'], report['transparent_unused_cells']), (57, 15))
        for name in report['archives']:
            prefix = '' if name.endswith('-petdex.zip') else 'lvk-rabbit/'
            with zipfile.ZipFile(self.out / name) as zipped:
                expected = {prefix + n for n in ['pet.json', 'spritesheet.webp', 'LICENSE']}
                if prefix:
                    expected.add(prefix + 'INSTALL.txt')
                self.assertEqual(set(zipped.namelist()), expected)
                self.assertEqual(json.loads(zipped.read(prefix + 'pet.json'))['spriteVersionNumber'], 1)
                self.assertEqual(zipped.read(prefix + 'spritesheet.webp'), (self.root / 'compatibility/v1/spritesheet.webp').read_bytes())

    def test_v1_wrong_tag(self):
        with self.assertRaisesRegex(ValueError, 'Tag does not match'):
            build_v1_release(self.root, self.out, self.tag)
        self.assertFalse(self.out.exists())

    def mutate_pixel(self, point):
        p = self.root / 'compatibility/v1/spritesheet.webp'
        with Image.open(p) as opened:
            im = opened.convert('RGBA')
        im.putpixel(point, (1, 2, 3, 255))
        im.save(p, lossless=True, exact=True)
        q = self.root / 'compatibility/v1/qa.json'
        qa = json.loads(q.read_text()); qa['spritesheet_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
        q.write_text(json.dumps(qa))

    def test_v1_artwork_drift_even_with_updated_hash(self):
        self.mutate_pixel((90, 90))
        with self.assertRaisesRegex(ValueError, 'Animation pixels changed'):
            build_v1_release(self.root, self.out)

    def test_v1_unused_neutral_cell_rejected(self):
        self.mutate_pixel((6*192 + 90, 90))
        with self.assertRaisesRegex(ValueError, 'Unused v1 cell'):
            build_v1_release(self.root, self.out)

    def test_v1_wrong_metadata(self):
        p = self.root / 'compatibility/v1/pet.json'
        meta = json.loads(p.read_text()); meta['spriteVersionNumber'] = 2; p.write_text(json.dumps(meta))
        with self.assertRaisesRegex(ValueError, 'v1 metadata'):
            build_v1_release(self.root, self.out)
