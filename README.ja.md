# LVK Rabbit

LVK Rabbitは、柔らかい立体感を持つ、Codex・Petdex向けのオリジナルアニメーションPetです。

クリーム色の垂れ耳、丸眼鏡、ミントグリーンのパーカー、四つ葉クローバー付きノートPCが特徴の、ちょっと早とちりで一生懸命なコーディングウサギです。ChatGPTでデザインを決め、CodexとコミュニティのHatch Pet / hatch-pet-v2ワークフローで制作しました。

**現在のリリース：v2.2.0** — 標準9状態と16方向の視線を、v2形式のアトラスに収録しています。

[English](README.md)

![LVK Rabbit](previews/idle.webp)

## アニメーション

| Idle | Working | Waiting |
|---|---|---|
| ![Idle](previews/idle.webp) | ![Working](previews/running.webp) | ![Waiting](previews/waiting.webp) |

| Failed | Review | Jumping |
|---|---|---|
| ![Failed](previews/failed.webp) | ![Review](previews/review.webp) | ![Jumping](previews/jumping.webp) |

| Running right | Running left | Waving |
|---|---|---|
| ![Running right](previews/running-right.webp) | ![Running left](previews/running-left.webp) | ![Waving](previews/waving.webp) |

### 16方向の視線

![16方向を時計回りに見る](previews/look.webp)

v2.2では横向きでも黒目の縦長の形と大きさを保ち、顔の振り幅を控えめにしました。Jumpingは、先頭・末尾の大きさを維持しながら、手と耳を上げて喜ぶ動作に戻しています。

ダウンロードまたはclone後に[操作プレビュー](previews/index.html)をローカルで開くと、ポインターによる視線操作、ライト／ダーク背景、表示サイズを確認できます。

## インストール

`pet.json` と `spritesheet.webp` の2ファイルを、同じフォルダーに配置します。

```text
~/.codex/pets/lvk-rabbit/
```

公開用のPet IDは従来の `lvk-rabbit` を維持しています。`spriteVersionNumber: 2` に対応するクライアントを使用してください。カスタムPetの利用可否や選択操作はクライアントによって異なります。必要に応じてアプリを再起動し、LVK Rabbitを選択してください。

v1形式のみ対応するクライアント向けには、既存の[v1.1.0タグ](https://github.com/nagisasaka/lvk-rabbit/tree/v1.1.0)を残しています。

## 形式・検証

- 作品のリリース番号は **v2.2.0**、スプライト形式の番号は **2** です。
- 透過・可逆圧縮WebP：**1536×2288px**、8列×11行、1セル192×208px。
- 標準57フレーム＋視線16コマ＋正面1コマを収録し、残る14セルは透明です。
- 標準9状態：idle / running-right / running-left / waving / jumping / failed / waiting / running（作業中）/ review。
- 視線は0〜337.5°を22.5°刻みで時計回りに配置。0°は上、90°は右、180°は下、270°は左です。正面用セルは0始まりで行0・列6にあります。

[コンタクトシート](qa/contact-sheet.png)、[方向一覧](qa/look-directions.png)、[黒目の比較](qa/eyes-before-after.png)、[形式検証結果](qa/validation.json)、[視覚QAの要約](qa/release.json)を同梱しています。ライト／ダーク背景と小サイズで視覚QAを実施済みです。制作時の実アプリ内動作は未検証です。

スプライトシートは採用済みv2.2完成品とバイト単位で同一です。Pillowを導入したPython環境で `python scripts/render_previews.py` を実行すると、完成品からプレビューを再作成できます。

## ライセンス

**クリエイティブ・コモンズ 表示 4.0 国際（CC BY 4.0）**。ライセンス全文は [`LICENSE`](LICENSE)、条件の案内は[公式ページ](https://creativecommons.org/licenses/by/4.0/deed.ja)を参照してください。

画像（`spritesheet.webp`）、アニメーションWebP、コンタクトシート、メタデータ、ドキュメントは、公開者が許諾できる権利の範囲でCC BY 4.0として提供します。適切な著作者表示、ライセンスへのリンク、変更した場合の明示などの条件を守れば、改変・再配布・商用利用が可能です。

**クレジット表記例：** *LVK Rabbit* — Masato Fujino, [原本](https://github.com/nagisasaka/lvk-rabbit), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。改変した場合はその旨も明示してください。クレジットは著作者による推薦や承認を意味しません。
