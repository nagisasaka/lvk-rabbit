"""Package the exact standard animation cells of the approved v2 artwork as v1."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
from PIL import Image
from build_release import ROOT, COUNTS, build_release, require


def build_v1_release(root, output, tag=None):
    version = (root / 'VERSION').read_text().strip()
    artwork_tag = f'v{version}'
    require(tag is None or tag == artwork_tag + '-v1', 'Tag does not match VERSION compatibility tag')
    with tempfile.TemporaryDirectory() as temporary:
        baseline = build_release(root, Path(temporary), artwork_tag)
    source = root / 'compatibility/v1'
    metadata = json.loads((source / 'pet.json').read_text())
    expected = json.loads((root / 'pet.json').read_text())
    expected['spriteVersionNumber'] = 1
    require(metadata == expected, 'v1 metadata must match v2 except spriteVersionNumber')
    data = (source / 'spritesheet.webp').read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    qa = json.loads((source / 'qa.json').read_text())
    require(qa['artwork_release'] == artwork_tag and qa['source_v2_sha256'] == baseline['spritesheet_sha256'], 'v1 QA source mismatch')
    require(qa['spritesheet_sha256'] == digest and qa['visual_qa'] == 'pass', 'v1 approved QA hash or visual QA mismatch')
    with Image.open(source / 'spritesheet.webp') as opened:
        require(opened.format == 'WEBP' and not getattr(opened, 'is_animated', False), 'v1 atlas must be static WebP')
        require(opened.mode == 'RGBA' and opened.size == (1536, 1872), 'v1 atlas must be RGBA 1536x1872')
        atlas = opened.copy()
    with Image.open(root / 'spritesheet.webp') as opened:
        original = opened.convert('RGBA')
    used = unused = 0
    for row, count in enumerate(COUNTS[:9]):
        for column in range(8):
            box = (column*192, row*208, (column+1)*192, (row+1)*208)
            cell = atlas.crop(box)
            if column < count:
                require(cell.tobytes() == original.crop(box).tobytes(), f'Animation pixels changed at {row},{column}')
                used += 1
            else:
                require(not any(cell.tobytes()), f'Unused v1 cell is not zero RGBA at {row},{column}')
                unused += 1
    install = f'''LVK Rabbit {artwork_tag} — sprite format 1

Same nine animations as {artwork_tag}; no pointer-following gaze.
同じ9状態を収録したv1互換版です。視線追従は含みません。
Back up your current pet, then place the lvk-rabbit folder in ~/.codex/pets/.
既存版をバックアップし、lvk-rabbitフォルダーを ~/.codex/pets/ に配置してください。
Keep pet.json and spritesheet.webp together. Pet ID remains lvk-rabbit.
The v1 and v2 packages use the same ID; choose one for this installation.
v1とv2は同じIDを使うため、このインストール先ではどちらか一方を選びます。
Documentation: https://github.com/nagisasaka/lvk-rabbit/tree/{artwork_tag}-v1
CC BY 4.0 — LVK Rabbit by Masato Fujino. See LICENSE; indicate modifications.
https://creativecommons.org/licenses/by/4.0/
'''
    files = {'pet.json': (source / 'pet.json').read_bytes(), 'spritesheet.webp': data,
             'LICENSE': (root / 'LICENSE').read_bytes()}
    output.mkdir(parents=True, exist_ok=True)
    archives = {}
    for suffix, prefix in [('', 'lvk-rabbit/'), ('-petdex', '')]:
        name = f'lvk-rabbit-{artwork_tag}-format-v1{suffix}.zip'
        contents = dict(files)
        if prefix:
            contents['INSTALL.txt'] = install.encode()
        with zipfile.ZipFile(output / name, 'w', compression=zipfile.ZIP_STORED) as zipped:
            for filename, content in contents.items():
                info = zipfile.ZipInfo(prefix + filename, date_time=(2020, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                zipped.writestr(info, content)
        with zipfile.ZipFile(output / name) as zipped:
            require(zipped.testzip() is None, 'ZIP integrity failure')
            for filename, content in contents.items():
                require(zipped.read(prefix + filename) == content, 'ZIP readback mismatch')
        archives[name] = hashlib.sha256((output / name).read_bytes()).hexdigest()
    (output / 'SHA256SUMS-v1.txt').write_text(''.join(f'{digest}  {name}\n' for name, digest in archives.items()))
    report = {'artwork_release': artwork_tag, 'spriteVersionNumber': 1,
              'spritesheet_sha256': digest, 'source_v2_archive_sha256': baseline['archive_sha256'],
              'used_cells': used, 'transparent_unused_cells': unused,
              'all_animation_cells_rgba_identical': True, 'archives': archives}
    (output / 'validation-v1.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    print(json.dumps(build_v1_release(ROOT, args.output_dir, args.tag), indent=2))
