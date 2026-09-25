# PowerPoint / Excel の仕様書を Markdown にする

すべて手元の PC の中で完結し、資料は外に出ない。詳しい結果と注意は [詳細版](https://github.com/ARKLET-1111/ai-driven-spec-demo/blob/main/docs/)。

## 結論

| 資料の中身 | 方法 | 品質 |
|---|---|---|
| 文字・箇条書き・表 | Docling で変換（1 ファイル 0.1 秒） | **そのまま使える** |
| 図（画像） | Docling で画像を取り出し → OCR を別途かける | 日本語の文は読める。**記号・添字は崩れる**ので人が確認 |
| 図を AI に使わせたい | OCR 結果＋本文を渡して **Mermaid に書き直させる** | 正しいかは人が判定 |

## 手順

```bash
# 準備（1回）
pip install docling                  # IBM 製 OSS・Apache-2.0
pip install easyocr                  # 図の文字を読む用（Mac は pip install ocrmac）

# 変換（画像は外部ファイルに出す。base64 埋め込みだと MD が巨大になる）
docling 仕様書.pptx --to md --image-export-mode referenced --output out/
docling 関数一覧.xlsx --to md --output out/
```

- PPT：見出し・箇条書き・表が Markdown に。図は `out/*_artifacts/*.png` に書き出され、MD にはリンクだけ
- Excel：各シートが表として並ぶ。**シート名は出ない**ので表の上に見出しを足す
- 図の文字：Docling に画像を渡しても「図」と判定されて文字は出ない。OCR を直接かける（[スクリプト](../pattern1_legacy_to_md/ocr_figure_compare.py)）

実例：[変換前](../pattern1_legacy_to_md/input/) → [変換後](../pattern1_legacy_to_md/output/numlib_機能仕様書_v0.9.md)／[要件定義書（PPT）の変換](../pattern2_req_to_spec/A2_from_requirements_pptx/requirements_from_pptx.md)

## 注意

- **Docling の既定 OCR は中国製（RapidOCR）**で、初回に中国のサーバーからモデルを取得する。文字と表だけなら OCR は動かないが、画像・スキャン PDF を通すときは必ず `--ocr-engine` を指定する（Mac: `ocrmac`、Linux/Windows: `easyocr` か `tesseract`）
- ネットに繋がらない環境へは、ネットのある PC で `pip download docling`（画像も扱うなら OCR モデルも）を取得して持ち込む

## OCR の選択肢（図・スキャン PDF を読むとき）

Nemotron-3-Super は画像を読めない。文字と表だけなら OCR は不要。図を読むときは別のものを使う。

| 選択肢 | 費用 | 日本語 | 外部に出るか | 先方環境で |
|---|---|---|---|---|
| **Tesseract**（Google 発 OSS） | 無料 | 中 | 出ない | ◎ Linux/Windows の第一候補 |
| **EasyOCR**（タイ発 OSS） | 無料 | 中〜低（実測：誤字あり） | 出ない | ○ |
| Apple Vision | 無料 | 高（実測：記号は崩れる） | 出ない | △ Mac 限定 |
| RapidOCR / PaddleOCR（中国） | 無料 | 高 | 出ない | **✕ 中華系。Docling の既定** |
| **Gemma 3**（Google・画像対応） | 無料（GPU） | 図の意味まで説明できる。要検証 | 出ない | ◎ DGX Spark に同居できる見込み |
| NVIDIA の文書読み取りモデル | 無料（GPU） | 英語中心。要検証 | 出ない | ○ |
| クラウド OCR | 有料 | 最高 | **出る** | **✕** |

使い方：安い OCR で文字を抜き、必要なら Gemma 3 で図の意味を説明させ、Nemotron に本文と突き合わせて Mermaid に書き直させる。**どの方式でも記号・添字は人が一度見る。** 実測したのは Apple Vision と EasyOCR のみで、他は要検証。
