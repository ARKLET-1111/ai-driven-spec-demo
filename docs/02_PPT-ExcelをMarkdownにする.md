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
