# パターン①「既存のPPT/Excel仕様書 → Markdown」検証メモ

検証日: 2026-09-24（環境: macOS / Python 3.10 / Docling 2.130.0）

## 入力（自作ダミー・実資料は不使用）
- `input/numlib_機能仕様書_v0.9.pptx` … 8枚。表紙／概要／関数仕様×2（表）／エラーコード表／**処理フロー（図のみ・文字情報なし）**／試験観点表／改訂履歴
- `input/numlib_関数一覧.xlsx` … 3シート（関数一覧／エラーコード／試験項目）
- 生成スクリプト: `make_dummy_inputs.py`

## 結果
| 入力 | ツール | 時間 | 結果 |
|---|---|---|---|
| PPTX | `docling --to md --image-export-mode referenced` | 0.08秒 | 見出し・箇条書き・表は**そのまま使える品質**。図は `*_artifacts/*.png` に書き出され、MDには画像リンクのみ |
| XLSX | `docling --to md` | 0.02秒 | 3シートとも表として取れる。**シート名は出ない**（表の見出しを人が足す） |
| 図PNG | Docling経由のOCR（どのエンジンでも） | — | 図全体が「Picture」と判定され**文字はMDに出ない** |
| 図PNG | OCRを直接実行（Apple Vision / ocrmac） | 0.5秒 | 日本語の文は正確。**数式・添字（`|a[i][k]|` → `1allIk］`）は崩れる** |
| 図PNG | OCRを直接実行（EasyOCR ja+en, CPU） | 3.7秒 | 行が分断され誤字が多い（選沢／入れ着える／固足）。Linux/Windows での現実的な下限 |

詳細: `output/_flow_gauss.ocr.txt`

## 先方に伝えるべき知見
1. **テキストと表が入っている資料は、OCRなしで一瞬でMD化できる**（Docling。IBM製OSS、Apache-2.0、完全ローカル）
2. **Doclingの既定OCRは RapidOCR（PaddleOCR系・中国製。モデルを modelscope.cn から取得）**。何も指定せず画像やスキャンPDFを通すと中華系エンジンが走る。`--ocr-engine` で明示的に切り替えること（Mac: `ocrmac`、Linux/Windows: `easyocr` か `tesseract`）
3. 図の中の文字は「Doclingで場所を特定 → OCRを直接かけて図の下に追記」の2段構え。**数式や添字は人が確認する前提**。図は最終的に Mermaid で書き直させる方が確実（AIに図を読ませるより、図の意味を文章で渡す）
4. 画像を base64 で埋め込む既定出力（139KB）はAIに渡すには重い。`--image-export-mode referenced` で外部ファイルにする

## 未検証・次にやること
- [ ] 図 → Mermaid 変換をAI（Nemotron）にやらせて品質を見る
- [ ] Excel 内に貼られた画像／セル結合の多い表（実資料で起こりがち）
- [ ] Tesseract（jpn）の精度。先方環境が Linux/Windows の場合の第一候補
- [ ] granite-docling-258M（IBM のVLM）で図を直接読めるか。日本語は実験的サポートのため期待値は低い
