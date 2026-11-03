# LVK Rabbit 🐰

An adorable animated pixel-art rabbit for Codex, Petdex, and [Lucky Vibe Kanban (LVK)](https://luckyvibekanban.com).

LVK Rabbit is a cream-colored, lop-eared coding companion with round glasses, a mint-green hoodie, and a laptop marked with a four-leaf clover. It was designed in ChatGPT and animated with Codex and OpenAI's Hatch Pet skill.

![LVK Rabbit idle animation](previews/idle.gif)

## Animations

| Idle | Working | Waiting |
|---|---|---|
| ![Idle](previews/idle.gif) | ![Working](previews/running.gif) | ![Waiting](previews/waiting.gif) |

| Failed | Review | Jumping |
|---|---|---|
| ![Failed](previews/failed.gif) | ![Review](previews/review.gif) | ![Jumping](previews/jumping.gif) |

The package also includes right/left running and waving animations (9 standard states in total).

## Install in Codex

Clone or download this repository, then copy `pet.json` and `spritesheet.webp` together into:

```text
~/.codex/pets/lvk-rabbit/
```

Restart your Codex app if needed and select the custom pet using your app's available controls. Availability depends on the Codex client.

## Petdex

This package uses the Codex / Petdex v1 sprite atlas: 1536 × 1872 pixels, 8 columns × 9 rows, 192 × 208 pixels per frame. It includes 57 used frames and 15 fully transparent unused cells.

For submission, use the two-file `petdex/` bundle from the publication kit or submit this repository's root directory:

```bash
npx petdex login
npx petdex submit ./
```

Submission requires Petdex sign-in and goes through review. An approved entry can then be installed using its assigned slug.

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0)** — see the [LICENSE](LICENSE) file and the [official license](https://creativecommons.org/licenses/by/4.0/).

The pet artwork (`spritesheet.webp`), animated previews (`previews/*.gif`), contact sheet, metadata, and documentation are published under CC BY 4.0 to the extent the publisher holds applicable rights. Reuse, modification, redistribution, and commercial use are permitted under its conditions, including appropriate attribution, a license link, and an indication of modifications.

**Attribution:** *LVK Rabbit* — Masato Fujino, [source repository](https://github.com/nagisasaka/lvk-rabbit), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Indicate if you modify the material. Attribution does not imply endorsement.

Designed with assistance from OpenAI ChatGPT and animated with Codex / Hatch Pet. This is an independently created community character, **not an official OpenAI character or OpenAI-endorsed project**. AI-generated elements may not be protected by copyright in every jurisdiction; this license applies only to rights the licensor can grant.

