"""Validate the approved v2 pet and build a reproducible public release ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def build_release(root: Path, output: Path, tag: str | None = None):
    version = (root / "VERSION").read_text().strip()
    require(re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version), "VERSION must be a stable X.Y.Z version")
    expected_tag = f"v{version}"
    require(tag is None or tag == expected_tag, "Tag does not match VERSION")
    notes = root / "releases" / f"{expected_tag}.txt"
    require(notes.is_file() and notes.read_text().strip(), "Release notes are missing")
    metadata = json.loads((root / "pet.json").read_text())
    require(metadata.get("id") == "lvk-rabbit", "Public pet ID must remain lvk-rabbit")
    require(metadata.get("displayName") == "LVK Rabbit", "Public display name must remain LVK Rabbit")
    require(metadata.get("spriteVersionNumber") == 2, "spriteVersionNumber must be 2")
    require(metadata.get("spritesheetPath") == "spritesheet.webp", "Unexpected spritesheetPath")
    data = (root / "spritesheet.webp").read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    qa = json.loads((root / "qa/release.json").read_text())
    require(qa.get("release") == expected_tag, "QA release does not match VERSION")
    require(qa.get("spritesheet_sha256") == digest, "Atlas differs from the approved QA hash")
    require(qa.get("visual_qa") == "pass", "Visual QA has not passed")
    with Image.open(root / "spritesheet.webp") as opened:
        require(opened.format == "WEBP" and not getattr(opened, "is_animated", False), "Atlas must be a static WebP")
        require(opened.mode == "RGBA" and opened.size == (1536, 2288), "Expected an RGBA 1536x2288 v2 atlas")
        atlas = opened.copy()
    used = unused = 0
    for row, count in enumerate(COUNTS):
        for column in range(8):
            alpha = atlas.getchannel("A").crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))
            occupied = column < count or (row, column) == (0, 6)
            require(bool(alpha.getbbox()) == occupied, f"Unexpected {'empty' if occupied else 'nontransparent'} cell at row {row}, column {column}")
            used += occupied
            unused += not occupied
    raw = atlas.tobytes()
    require(all(raw[i:i+3] == b"\0\0\0" for i in range(0, len(raw), 4) if raw[i+3] == 0), "Hidden RGB residue in transparent pixels")
    install = f"""LVK Rabbit {expected_tag}

日本語
spriteVersionNumber: 2 対応クライアントが必要です。
既存版をバックアップし、この lvk-rabbit フォルダーを ~/.codex/pets/ に配置してください。
pet.json と spritesheet.webp は同じフォルダーに保持してください。
必要に応じてアプリを再起動し、LVK Rabbitを選択してください。

English
Requires a client supporting spriteVersionNumber: 2.
Back up your existing pet, then place this lvk-rabbit folder in ~/.codex/pets/.
Keep pet.json and spritesheet.webp together. Restart if needed and select LVK Rabbit.

Documentation: https://github.com/nagisasaka/lvk-rabbit/tree/{expected_tag}
For v1-only clients: https://github.com/nagisasaka/lvk-rabbit/releases/tag/v1.1.0

Attribution: LVK Rabbit — Masato Fujino
https://github.com/nagisasaka/lvk-rabbit
CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
See LICENSE; indicate any modifications. No endorsement is implied.
"""
    files = {"pet.json": (root / "pet.json").read_bytes(), "spritesheet.webp": data,
             "LICENSE": (root / "LICENSE").read_bytes(), "INSTALL.txt": install.encode()}
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"lvk-rabbit-{expected_tag}.zip"
    # WebP is already compressed. Stored entries also make bytes reproducible
    # across Python/zlib versions, including local vs Actions environments.
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as zipped:
        for name, content in files.items():
            info = zipfile.ZipInfo(f"lvk-rabbit/{name}", date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            zipped.writestr(info, content)
    with zipfile.ZipFile(archive) as zipped:
        require(zipped.testzip() is None, "ZIP integrity check failed")
        for name, content in files.items():
            require(zipped.read(f"lvk-rabbit/{name}") == content, f"ZIP readback mismatch: {name}")
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS.txt").write_text(f"{checksum}  {archive.name}\n")
    report = {"release": expected_tag, "spritesheet_sha256": digest, "archive_sha256": checksum,
              "archive": archive.name, "used_cells": used, "transparent_unused_cells": unused}
    (output / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    if args.tag and args.tag.endswith("-v1"):
        from build_v1_release import build_v1_release
        report = build_v1_release(ROOT, args.output_dir, args.tag)
    else:
        report = build_release(ROOT, args.output_dir, args.tag)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
