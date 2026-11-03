# LVK Rabbit 🐰

LVK Rabbitは、Codex・Petdex・[Lucky Vibe Kanban (LVK)](https://luckyvibekanban.com) で使える、アニメーション付きのオリジナルのピクセルアートPetです。

クリーム色の垂れ耳、丸眼鏡、ミントグリーンのパーカー、四つ葉クローバー付きノートPCが特徴の、ちょっと早とちりで一生懸命なコーディングウサギです。ChatGPTでデザインを決め、CodexとOpenAIのHatch Pet Skillを用いてアニメーションを制作しました。

![LVK Rabbit](previews/idle.gif)

## アニメーション

標準の9状態（idle / running-right / running-left / waving / jumping / failed / waiting / running=作業中 / review）を収録しています。

| Idle | Working | Waiting |
|---|---|---|
| ![Idle](previews/idle.gif) | ![Working](previews/running.gif) | ![Waiting](previews/waiting.gif) |

| Failed | Review | Jumping |
|---|---|---|
| ![Failed](previews/failed.gif) | ![Review](previews/review.gif) | ![Jumping](previews/jumping.gif) |

## インストール・形式

`pet.json` と `spritesheet.webp` の2ファイルを `~/.codex/pets/lvk-rabbit/` に配置します。アプリ側でカスタムPetを選択する操作はCodexクライアントによって異なります。

アトラスはPetdex/Codex Pet v1互換の1536×1872px、8列×9行、1セル192×208px。使用57フレーム、未使用15セルは透明です。

Petdexへの投稿は`npx petdex login`後に`npx petdex submit ./`で可能です（審査あり）。

## ライセンス

**クリエイティブ・コモンズ 表示 4.0 国際（CC BY 4.0）**。ライセンス全文は [`LICENSE`](LICENSE)、条件の案内は[公式ページ](https://creativecommons.org/licenses/by/4.0/deed.ja)を参照してください。

画像（`spritesheet.webp`）、アニメーションGIF、コンタクトシート、メタデータ、ドキュメントは、公開者が許諾できる権利の範囲でCC BY 4.0として提供します。適切な著作者表示、ライセンスへのリンク、変更した場合の明示などの条件を守れば、改変・再配布・商用利用が可能です。

**クレジット表記例：** *LVK Rabbit* — Masato Fujino, [原本](https://github.com/nagisasaka/lvk-rabbit), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。改変した場合はその旨も明示してください。クレジットは著作者による推薦や承認を意味しません。

OpenAI ChatGPTとCodex / Hatch Petの支援を受けて制作した独立のコミュニティ作品であり、OpenAIの公式キャラクターではありません。生成AIによる素材の著作権成立範囲は法域によって異なるため、本ライセンスによる許諾は公開者が保有する権利の範囲に限られます。

