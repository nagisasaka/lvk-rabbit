# LVK Rabbit

LVK Rabbitは、柔らかい立体感を持つ、Codex・Petdex向けのオリジナルアニメーションPetです。

クリーム色の垂れ耳、丸眼鏡、ミントグリーンのパーカー、四つ葉クローバー付きノートPCが特徴の、ちょっと早とちりで一生懸命なコーディングウサギです。ChatGPTでデザインを決め、CodexとコミュニティのHatch Pet / hatch-pet-v2ワークフローで制作しました。

**現在のリリース：v2.4.1** — 標準9状態と16方向の視線を、v2形式のアトラスに収録しています。

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

### Failed：また挑戦できる失敗の表現

開発に失敗はつきものです。深く悲しむキャラクターを繰り返し見ると、感情移入する人には日常的なつまずきまで重く感じられることがあります。LVK RabbitのFailedは、問題を明確に伝えつつ、少しコミカルな「やっちゃった！」と、一緒にまた挑戦できる雰囲気を目指しています。

### 16方向の視線

![16方向を時計回りに見る](previews/look.webp)

v2.2では横向きでも黒目の縦長の形と大きさを保ち、顔の振り幅を控えめにしました。Jumpingは、先頭・末尾の大きさを維持しながら、手と耳を上げて喜ぶ動作に戻しています。

ダウンロードまたはclone後に[操作プレビュー](previews/index.html)をローカルで開くと、ポインターによる視線操作、ライト／ダーク背景、表示サイズを確認できます。

## v2.4.1の変更

Failedの両目の位置に、漫画表現の横長のバツ目を追加しました。うつむいた頭の小さな揺れに追従し、両端は手の後ろに隠れます。輪郭ありの青い汗は保ちながら、失敗を少しコミカルに伝えます。

Wavingは上げた袖をほんの少し太くし、茶色の輪郭線の太さを整えました。採用済みの腕の長さ・角度・手・袖口・ミント色は維持しています。

v2.4.0からの変更は `failed` の8コマと `waving` の4コマのみ。他7状態・正面セル・16方向と、アトラス全体の透過情報は同一です。見た目の微調整なので、更新は任意です。パッケージ形式やクライアント側の状態割り当ては変わりません。

[Failedの新旧比較](previews/failed-before-after-light.gif)・[ダーク背景の小サイズ比較](previews/failed-before-after-dark-small.gif)・[Idle → Failed → Idle](previews/idle-failed-idle-light.gif)・[手振りの新旧比較](previews/idle-wave-idle-light.gif)。

比較対象は公開済みv2.4.0と今回のv2.4.1です。

## インストール

[最新Release](https://github.com/nagisasaka/lvk-rabbit/releases/latest)からPet用ZIPをダウンロードし、既存版をバックアップしてから展開してください。ZIP内の `lvk-rabbit` フォルダーを配置し、`pet.json` と `spritesheet.webp` を同じフォルダーに保ちます。

```text
~/.codex/pets/lvk-rabbit/
```

公開用のPet IDは従来の `lvk-rabbit` を維持しています。`spriteVersionNumber: 2` に対応するクライアントを使用してください。カスタムPetの利用可否や選択操作はクライアントによって異なります。必要に応じてアプリを再起動し、LVK Rabbitを選択してください。

v1形式のみ対応するクライアント向けには、既存の[v1.1.0タグ](https://github.com/nagisasaka/lvk-rabbit/tree/v1.1.0)を残しています。

## 形式・検証

- 作品のリリース番号は **v2.4.1**、スプライト形式の番号は **2** です。
- 透過・可逆圧縮WebP：**1536×2288px**、8列×11行、1セル192×208px。
- 標準57フレーム＋視線16コマ＋正面1コマを収録し、残る14セルは透明です。
- 標準9状態：idle / running-right / running-left / waving / jumping / failed / waiting / running（作業中）/ review。
- 視線は0〜337.5°を22.5°刻みで時計回りに配置。0°は上、90°は右、180°は下、270°は左です。正面用セルは0始まりで行0・列6にあります。

[コンタクトシート](qa/contact-sheet.png)、[方向一覧](qa/look-directions.png)、[黒目の比較](qa/eyes-before-after.png)、[形式検証結果](qa/validation.json)、[視覚QAの要約](qa/release.json)を同梱しています。ライト／ダーク背景と小サイズで視覚QAを実施済みです。制作時の実アプリ内動作は未検証です。

FailedとWavingはそれぞれ承認済みのバツ目版・輪郭線修正版と画素単位で一致し、その他のセルはv2.4.0を維持しています。Pillowを導入したPython環境で `python scripts/render_previews.py` を実行すると、完成品からプレビューを再作成できます。

## Releaseの自動公開

GitHub Actionsが `main` へのpush、Pull Request、バージョンタグのpush時にPetを検証してZIPを作ります。`vX.Y.Z` タグをpushした場合のみ、検証後にReleaseを公開します。使用するのはリポジトリ専用の一時的な `GITHUB_TOKEN` と `contents: write` 権限で、個人用トークンは不要です。

次回は `VERSION`、採用画像と `qa/release.json` 内のSHA256を更新し、`releases/vX.Y.Z.txt` を追加します。プレビューを再生成してcommitし、対応する注釈付きタグをpushしてください。Actionsがドラフトを作成し、Pet ZIPと `SHA256SUMS.txt` を添付して公開します。公開済みの添付ファイルは上書きしません。途中で止まった場合はActionsの失敗したジョブを再実行できます。

ローカルでの梱包は `scripts/requirements-release.txt` を導入後、`python scripts/build_release.py` を実行します。出力先は `dist/` です。

## ライセンス

**クリエイティブ・コモンズ 表示 4.0 国際（CC BY 4.0）**。ライセンス全文は [`LICENSE`](LICENSE)、条件の案内は[公式ページ](https://creativecommons.org/licenses/by/4.0/deed.ja)を参照してください。

画像（`spritesheet.webp`）、アニメーションWebP、コンタクトシート、メタデータ、ドキュメントは、公開者が許諾できる権利の範囲でCC BY 4.0として提供します。適切な著作者表示、ライセンスへのリンク、変更した場合の明示などの条件を守れば、改変・再配布・商用利用が可能です。

**クレジット表記例：** *LVK Rabbit* — Masato Fujino, [原本](https://github.com/nagisasaka/lvk-rabbit), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。改変した場合はその旨も明示してください。クレジットは著作者による推薦や承認を意味しません。
