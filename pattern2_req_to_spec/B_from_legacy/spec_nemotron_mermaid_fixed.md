# Nemotron B の Mermaid 図（人が最小限の修正を加えた版）

元の図（`spec_nemotron.md` 末尾）は Mermaid の文法エラーで描画できない（ノード内の `|` と `[ ]` が裸）。
直したのは 2 点だけ：**(1) 全ノードのラベルを引用符で囲む、(2) 特異判定の添字 `a[p][p]` → `a[p][k]`**（OCR 原文は `lalp］［k］`）。

```mermaid
flowchart TD
    A["開始: k = 0"] --> B{"列 k で |a[i][k]| が最大となる行 p を選択<br/>(部分ピボット選択)"}
    B --> C{"|a[p][k]| < EPS? (1e-12)"}
    C -->|Yes| D["E_SINGULAR (-2) を返して終了"]
    C -->|No| E["行 k と行 p を入れ替える（a と b の両方）"]
    E --> F["行 k を a[k][k] で割って正規化（対角成分を 1 にする）"]
    F --> G["全ての行 i (i ≠ k) について:<br/>因子 = a[i][k]<br/>行 i ← 行 i - 因子 × 行 k<br/>（これにより列 k の他の要素を 0 にする）"]
    G --> H["k ← k + 1"]
    H --> I{"k < n?"}
    I -->|Yes| B
    I -->|No| J["x ← b を出力して 0 を返す"]
    style D fill:#f9f,stroke:#333
    style J fill:#9f9,stroke:#333
```
