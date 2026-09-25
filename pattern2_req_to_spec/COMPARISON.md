# Nemotron-3-Super と Claude の仕様書比較

同じ指示文（各フォルダの `_prompt_sent.md`）を両方に与えた。Nemotron は OpenRouter 経由 `nvidia/nemotron-3-super-120b-a12b`（オンプレと同じモデル）、Claude は `claude-fable-5-1`。

| 入力 | Nemotron | Claude |
|---|---|---|
| **A** 要件 10 行 | 10 章・試験観点 24・**2 分 52 秒**。設計判断とシグネチャの自己矛盾が 1 つ（`double **`） | 10 章・試験観点 71・矛盾なし |
| **A2** 要件定義書（PPT 8 枚） | 10 章・試験観点 20・要件トレース表・**2 分 40 秒**。要件に方針が書いてあったので矛盾なし | （未実施） |
| **B** 既存仕様書（PPT/Excel）＋図の OCR | 原資料の T01〜T12 を欠落なく引き継ぎ T13〜T15 を追加、【要確認】18 か所、Mermaid 1 図（添字 1 か所ミス＋文法エラー・引用符で直る）・**5 分 17 秒** | 【要確認】24 か所・Mermaid 2 図（描画可） |

費用は Nemotron 1 本あたり 0.5〜0.7 円（OpenRouter 換算）。

## 結論

1. 「見本 1 本＋章立ての指定＋【設計判断】【要確認】の要求」があれば、**Nemotron でも実装に使える仕様書が書ける**
2. 弱点は**一貫性**と**図の文法**。**要件側に方針を 1 枚足す**（A2 で実証）／**生成後に自己点検の 1 ターン**を足す、で消える
3. Claude との差は**量と丁寧さ**で、正しさの差ではない。埋まらなかった穴は実装のテスト・カバレッジで受け止める（→ [pattern3_impl](../pattern3_impl/)）

注記：A・B の実行時、OpenCode がリポジトリの AGENTS.md を自動で読み込んでいた（痕跡が確認できたのは B の §9・§8。関数仕様・試験観点の評価には影響なし）。A2 は別ディレクトリで実行し混入なし。
生成物：各フォルダの `spec_nemotron.md` / `spec_claude.md`。詳しい採点表は [詳細版](https://github.com/ARKLET-1111/ai-driven-spec-demo/blob/main/pattern2_req_to_spec/COMPARISON.md)。
