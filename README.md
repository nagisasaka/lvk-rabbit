# LVK Rabbit

A friendly animated rabbit for Codex and Petdex, with soft dimensional shading.

LVK Rabbit is a cream-colored, lop-eared coding companion with round glasses, a mint-green hoodie, and a laptop marked with a four-leaf clover. It was designed with ChatGPT and animated with Codex using the community Hatch Pet / hatch-pet-v2 workflow.

**Current release: v2.4.1** — available in v2 format (9 states + 16 look directions) and v1 format (the same 9 states, without gaze).

[日本語](README.ja.md)

![LVK Rabbit idle animation](previews/idle.webp)

## Animations

| Idle | Working | Waiting |
|---|---|---|
| ![Idle](previews/idle.webp) | ![Working](previews/running.webp) | ![Waiting](previews/waiting.webp) |

| Failed | Review | Jumping |
|---|---|---|
| ![Failed](previews/failed.webp) | ![Review](previews/review.webp) | ![Jumping](previews/jumping.webp) |

| Running right | Running left | Waving |
|---|---|---|
| ![Running right](previews/running-right.webp) | ![Running left](previews/running-left.webp) | ![Waving](previews/waving.webp) |

### Failed: a recoverable setback

Failure is an everyday part of development. Repeatedly seeing a deeply sad companion can add emotional weight to an ordinary setback, especially for people who empathize with the character. LVK Rabbit's Failed expression aims for a clear but gently comic “Oops!”—acknowledging the problem while feeling ready to try again together.

### 16 look directions

![Clockwise gaze loop](previews/look.webp)

The v2.2 gaze and jump improvements are preserved: the artwork keeps substantial oval pupils when looking sideways, uses gentler head turns, and restores a joyful jump with raised hands and ears while keeping the resting endpoints at the correct size.

After downloading or cloning, open [the interactive preview](previews/index.html) locally to try pointer-directed gaze and light/dark backgrounds.

## New in v2.4.1

Failed adds a single wide manga-style cross across both eye positions. It follows the bowed head's gentle sway and sits behind the paws, giving failure a clear, gently comic expression while preserving the outlined blue sweat.

Waving's raised sleeve is subtly fuller, with its brown contour adjusted for consistent weight. The approved arm length, angle, paw, cuff and mint palette are preserved.

Only eight `failed` frames and four `waving` frames changed from v2.4.0. The other seven states, neutral cell, all sixteen look directions and the entire atlas alpha channel are unchanged. This is an optional visual polish update; package format and client event mapping are unchanged.

[Failed before/after](previews/failed-before-after-light.gif) · [Small dark-background Failed comparison](previews/failed-before-after-dark-small.gif) · [Idle → Failed → Idle](previews/idle-failed-idle-light.gif) · [Waving before/after](previews/idle-wave-idle-light.gif).

These compare the published v2.4.0 artwork with v2.4.1.

## Install in Codex

Download the Pet ZIP from the [latest Release](https://github.com/nagisasaka/lvk-rabbit/releases/latest), back up your existing pet, and extract its `lvk-rabbit` folder. Keep `pet.json` and `spritesheet.webp` together in:

```text
~/.codex/pets/lvk-rabbit/
```

Choose the package matching your client. Both use the ID `lvk-rabbit`; install one format at this location. Restart if needed and select LVK Rabbit.

| Package in the v2.4.1 Release | Purpose |
|---|---|
| `lvk-rabbit-v2.4.1.zip` | Format 2; nine states and pointer-following gaze |
| `lvk-rabbit-v2.4.1-format-v1.zip` | Format 1; same artwork and nine states, no gaze |
| `lvk-rabbit-v2.4.1-format-v1-petdex.zip` | Format 1; flat ZIP for Petdex submission |

For editing the existing Petdex entry, use `pet.json` and `spritesheet.webp` extracted from the v1 ZIP. These files are also available in [compatibility/v1](compatibility/v1). The ID remains `lvk-rabbit`.

The v1 conversion has a **1536 × 1872**, 8 × 9 atlas: 57 used cells and 15 transparent cells. All 57 animation cells are RGBA-identical to v2.4.1. Only the extra neutral cell and gaze rows are removed. See the [v1 contact sheet](compatibility/v1/contact-sheet.png), [validation](compatibility/v1/validation.json), and [QA](compatibility/v1/qa.json). The nine animation previews above apply to both formats; gaze previews apply only to v2.

## Atlas and validation

- Release version: **v2.4.1**; sprite format: **2** (these are separate version numbers).
- Lossless transparent WebP: **1536 × 2288**, 8 columns × 11 rows, 192 × 208 per cell.
- 57 standard animation frames, 16 clockwise gaze poses, and 1 neutral cell; the remaining 14 cells are transparent.
- Standard rows: idle, running-right, running-left, waving, jumping, failed, waiting, running (working), review.
- Gaze rows: 0° through 337.5° in 22.5° steps; 0° means up, 90° right, 180° down, and 270° left. The neutral cell is row 0, column 6 (zero-based).

See the [contact sheet](qa/contact-sheet.png), [direction sheet](qa/look-directions.png), [eye comparison](qa/eyes-before-after.png), [format validation](qa/validation.json), and [visual QA summary](qa/release.json). Visual QA covered both backgrounds and small-size previews; live-app behavior was not tested during this production run.

The published Failed and Waving rows are pixel-identical to their approved cross-eyes and consistent-outline candidates; all other cells are retained from v2.4.0. Previews can be regenerated from it with `python scripts/render_previews.py` in an environment with Pillow installed.

## Release automation

GitHub Actions validates the pet and builds a reproducible ZIP on pushes to `main`, pull requests, and version-tag pushes. A pushed `vX.Y.Z` tag publishes a Release only after validation succeeds, using that repository’s temporary `GITHUB_TOKEN` with `contents: write`. No personal token is required.

For the next release, update `VERSION`, the approved artwork and QA hash in `qa/release.json`, and add `releases/vX.Y.Z.txt`; regenerate previews, commit, then push the matching annotated tag. The workflow creates a draft, uploads the Pet ZIP and `SHA256SUMS.txt`, and publishes it. Existing published assets are never overwritten. To retry an interrupted draft publication, rerun the failed Actions job.

Local packaging: install `scripts/requirements-release.txt`, then run `python scripts/build_release.py`. Output is written to `dist/`.

A compatibility tag `vX.Y.Z-v1` attaches the two v1 ZIPs and `SHA256SUMS-v1.txt` to the existing `vX.Y.Z` Release. It verifies the published v2 ZIP before uploading and never replaces existing assets. The artwork version stays the same. Build locally with `python scripts/build_v1_release.py`; approve the conversion in `compatibility/v1/qa.json` first. The `v2.4.1-v1` tag records the compatibility source; the original `v2.4.1` tag is unchanged.

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0)** — see the [LICENSE](LICENSE) file and the [official license](https://creativecommons.org/licenses/by/4.0/).

The pet artwork (`spritesheet.webp`), animated previews (`previews/*.webp`), contact sheet, metadata, and documentation are published under CC BY 4.0 to the extent the publisher holds applicable rights. Reuse, modification, redistribution, and commercial use are permitted under its conditions, including appropriate attribution, a license link, and an indication of modifications.

**Attribution:** *LVK Rabbit* — Masato Fujino, [source repository](https://github.com/nagisasaka/lvk-rabbit), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Indicate if you modify the material. Attribution does not imply endorsement.

Designed with assistance from OpenAI ChatGPT and animated with Codex / Hatch Pet. This is an independently created community character, **not an official OpenAI character or OpenAI-endorsed project**. AI-generated elements may not be protected by copyright in every jurisdiction; this license applies only to rights the licensor can grant.
