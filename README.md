# LVK Rabbit

A friendly animated rabbit for Codex and Petdex, with soft dimensional shading.

LVK Rabbit is a cream-colored, lop-eared coding companion with round glasses, a mint-green hoodie, and a laptop marked with a four-leaf clover. It was designed with ChatGPT and animated with Codex using the community Hatch Pet / hatch-pet-v2 workflow.

**Current release: v2.4.1** — 9 animation states and 16 look directions in the v2 atlas format.

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

Keep the public package ID `lvk-rabbit`. Use a client that supports `spriteVersionNumber: 2`; custom-pet controls and availability depend on the client. Restart the app if needed and select LVK Rabbit.

For a client that only supports the v1 atlas, use the existing [v1.1.0 tag](https://github.com/nagisasaka/lvk-rabbit/tree/v1.1.0).

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

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0)** — see the [LICENSE](LICENSE) file and the [official license](https://creativecommons.org/licenses/by/4.0/).

The pet artwork (`spritesheet.webp`), animated previews (`previews/*.webp`), contact sheet, metadata, and documentation are published under CC BY 4.0 to the extent the publisher holds applicable rights. Reuse, modification, redistribution, and commercial use are permitted under its conditions, including appropriate attribution, a license link, and an indication of modifications.

**Attribution:** *LVK Rabbit* — Masato Fujino, [source repository](https://github.com/nagisasaka/lvk-rabbit), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Indicate if you modify the material. Attribution does not imply endorsement.

Designed with assistance from OpenAI ChatGPT and animated with Codex / Hatch Pet. This is an independently created community character, **not an official OpenAI character or OpenAI-endorsed project**. AI-generated elements may not be protected by copyright in every jurisdiction; this license applies only to rights the licensor can grant.
