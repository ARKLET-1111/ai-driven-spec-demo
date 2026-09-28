# パターン①「既存のPPT/Excel仕様書 → Markdown」検証メモ

検証日: 2026-09-24〜25（環境: macOS / Python 3.10 / Docling 2.130.0）

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
| 図PNG | OCRを直接実行（Apple Vision / ocrmac） | 0.4秒 | 日本語の文は正確。**数式・添字（`|a[i][k]|` → `1allIk］`）は崩れる** |
| 図PNG | OCRを直接実行（EasyOCR ja+en, CPU） | 4.9秒 | 行が分断され誤字が多い（選沢／入れ着える／固足）。Linux/Windows での現実的な下限 |
| 図PNG | OCRを直接実行（**Tesseract 5.3.0**、Debian 12 の Linux コンテナ、`-l jpn+eng --psm 3`） | 0.3秒 | **8工程すべてを文として読めた。** 記号（`|a[i][k]|`→`la[lk]|`）と一部の語（行→47、固定→同定、≠→は）が崩れる。`--psm 6` は見出し1行しか取れず不可。GPU・torch 不要で Linux の第一候補 |

詳細: `output/_flow_gauss.ocr.txt`

## 分かったこと
1. **テキストと表が入っている資料は、OCRなしで一瞬でMD化できる**（Docling。IBM製OSS、Apache-2.0、完全ローカル）
2. **Doclingの既定OCRは RapidOCR（PaddleOCR系・中国製。モデルを modelscope.cn から取得）**。何も指定せず画像やスキャンPDFを通すと、このエンジンが動く。`--ocr-engine` で明示的に切り替えること（Mac: `ocrmac`、Linux/Windows: `easyocr` か `tesseract`）
3. 図の中の文字は「Doclingで場所を特定 → OCRを直接かけて図の下に追記」の2段構え。**数式や添字は人が確認する前提**。図は最終的に Mermaid で書き直させる方が確実（AIに図を読ませるより、図の意味を文章で渡す）
4. 画像を base64 で埋め込む既定出力（139KB）はAIに渡すには重い。`--image-export-mode referenced` で外部ファイルにする

## 未検証・次にやること
- [ ] 図 → Mermaid 変換をAI（Nemotron）にやらせて品質を見る
- [ ] Excel 内に貼られた画像／セル結合の多い表（実資料で起こりがち）
- [x] Tesseract（jpn）の精度 → 上表（2026-09-25、Docker の Debian で実測）
- [ ] granite-docling-258M（IBM のVLM）で図を直接読めるか。日本語は実験的サポートのため期待値は低い

## 変換ツールの比較：Docling vs MarkItDown（2026-09-25 追加）

同じダミー PPTX / XLSX を Microsoft 製の MarkItDown 0.1.8（MIT）でも変換した（`output_markitdown/`）。

| 観点 | Docling 2.130 | MarkItDown 0.1.8 |
|---|---|---|
| 速度 | PPT 0.07 秒・Excel 0.004 秒 | PPT 0.05 秒・Excel 0.02 秒 |
| PPT の箇条書き | `-` 付きで残る（階層は平坦化） | **箇条書き記号が消えて平文になる**（構造が失われる） |
| PPT の表 | 再現。セル内の `\|` を `&#124;` に退避 | 再現。ただし **セル内の `\|`（`\|a[k][k]\|`）を退避しないので、その行で表が崩れる** |
| 識別子の `_` | 見出し・箇条書きは `\_`、表のセル内はそのまま | 全箇所 `\_` にエスケープ（`bubble\_sort\_i32`）。AI は読めるが目視で煩い |
| PPT の図 | PNG を `*_artifacts/` に書き出しリンク | `![…](Picture2.jpg)` と書くだけで**ファイルは出力されない** |
| スライド番号 | なし | `<!-- Slide number: N -->` が入る（元スライドへ辿りやすい） |
| Excel のシート名 | **出ない**（人が見出しを足す） | `## シート名` として出る（こちらが良い） |
| Excel セル内の改行 | 空白に平坦化 | `\n` の文字がそのまま残る |
| PDF | レイアウト解析モデルあり（未検証） | テキスト抽出のみ |

速度は 2026-09-28 に、同じ資料・同じ測り方（変換の呼び出し 1 回目の時間。道具の読み込み時間は含めない）で測り直した値。どちらも 0.1 秒未満で、差は体感できない。上の「結果」の表の 0.08 秒・0.02 秒は 9/24 の計測値。

**結論**: PowerPoint は Docling が安全（表・箇条書き・図の扱いで優位）。Excel は MarkItDown の方がシート名が残る分だけ良い。どちらもローカル完結・無料で、中国製ではない。**主に Docling、Excel だけ MarkItDown**、が今回の推奨。

