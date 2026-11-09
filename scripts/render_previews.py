"""Extract lossless animated previews from the approved atlas (requires Pillow)."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CELL_WIDTH, CELL_HEIGHT = 192, 208
STATES = {
    "idle": [280, 110, 110, 140, 140, 320],
    "running-right": [120] * 7 + [220],
    "running-left": [120] * 7 + [220],
    "waving": [140, 140, 140, 280],
    "jumping": [140, 140, 140, 140, 280],
    "failed": [140] * 7 + [240],
    "waiting": [150] * 5 + [260],
    "running": [120] * 5 + [220],
    "review": [150] * 5 + [280],
}


def save_preview(name, frames, durations):
    output = ROOT / "previews" / f"{name}.webp"
    output.parent.mkdir(exist_ok=True)
    frames[0].save(
        output,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        lossless=True,
        quality=100,
        method=6,
        exact=True,
    )
    # Check the decoded animation, including transparency and frame order.
    with Image.open(output) as decoded:
        assert decoded.n_frames == len(frames), name
        for index, expected in enumerate(frames):
            decoded.seek(index)
            actual = decoded.convert("RGBA")
            assert actual.getchannel("A").tobytes() == expected.getchannel("A").tobytes(), (name, index)
            # Animated WebP can discard RGB hidden under alpha=0 even in
            # lossless mode; every visible pixel and alpha value must match.
            before, after = expected.tobytes(), actual.tobytes()
            assert all(
                before[i : i + 4] == after[i : i + 4]
                for i in range(0, len(before), 4)
                if before[i + 3]
            ), (name, index)
            assert decoded.info["duration"] == durations[index], (name, index)
    print(f"{output.relative_to(ROOT)}: {len(frames)} frames, exact visible RGBA verified")


def main():
    with Image.open(ROOT / "spritesheet.webp") as source:
        atlas = source.convert("RGBA")
    assert atlas.size == (1536, 2288), "Expected the v2 atlas"

    def cell(row, column):
        x, y = column * CELL_WIDTH, row * CELL_HEIGHT
        return atlas.crop((x, y, x + CELL_WIDTH, y + CELL_HEIGHT))

    for row, (name, durations) in enumerate(STATES.items()):
        save_preview(name, [cell(row, col) for col in range(len(durations))], durations)
    save_preview("look", [cell(9 + i // 8, i % 8) for i in range(16)], [220] * 16)


if __name__ == "__main__":
    main()
