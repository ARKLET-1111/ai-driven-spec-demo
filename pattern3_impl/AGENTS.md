# AGENTS.md — numlib 実装デモ（pattern3_impl）

このディレクトリで作業する **すべてのAIエージェント**（OpenCode + Nemotron-3-Super / Claude Code 等、モデル問わず）が守るルール。
迷ったら **`SPEC.md` が単一の真実**。SPEC.md で決まらないことは、決めた内容と理由を `tests/results/` の結果ファイルに【設計判断】として書く。

## 1. 目的

`SPEC.md`（AIが既存資料から再構成した仕様書）**だけ**を入力に、C99 で `numlib`（`bubble_sort_i32` / `gauss_eliminate`）を実装し、単体試験・カバレッジ計測まで一気通貫で回す。

## 2. ファイル構成（これ以外を作らない）

```
pattern3_impl/
├── AGENTS.md        … 本ファイル（変更禁止）
├── SPEC.md          … 仕様書（変更禁止。矛盾・不足は結果ファイルに【要確認】で書く）
├── Makefile         … ビルド・テスト・カバレッジ手順（変更禁止）
├── numlib.h         … 公開ヘッダ（SPEC §3/§4 のプロトタイプと 1:1）
├── numlib.c         … 実装本体
├── test_numlib.c    … 単体試験（1ファイルに集約。分割しない）
├── build/           … 生成物（Git管理外）
└── tests/
    ├── results/     … 実行結果 Markdown（自動生成）
    └── coverage/    … カバレッジ（raw/*.gcov、lcov があれば HTML）
```

## 3. コーディング規約

- C99。`gcc -std=c99 -Wall -Wextra -Wpedantic` で**警告ゼロ**
- 動的メモリ確保（`malloc`/`free`）禁止。`numlib.c` から標準入出力を呼ばない（テストコードでの `printf` は可）
- 依存ヘッダは SPEC に書かれたもののみ
- NULL・不正な `n` でクラッシュしない（戻り値でエラー）
- 関数ごとに SPEC の該当節番号をコメントで書く（例: `/* SPEC §4.2 */`）

## 4. テスト規約

- テストは `test_numlib.c` の1ファイル。外部フレームワーク不要。`main` から順に呼ぶ簡易マクロでよい
- **各テストは SPEC §8 の観点ID（T01, T02, …）をコメントに書く**。§8 の全項目を最低1テストで網羅する
- 浮動小数の比較は許容誤差付き（SPEC の精度要件に従う）
- 失敗しても止めず、最後に pass/fail 件数を出力し、fail が1件でもあれば終了コード 1

## 5. 作業手順（この順番で）

1. `SPEC.md` を最後まで読む
2. `numlib.h` → `numlib.c` → `test_numlib.c` の順に書く
3. `make test` が通るまで直す（**SPEC が正**。SPEC と実装が食い違えば実装を直す）
4. `make coverage` を実行し、行カバレッジ **90% 以上**になるまで `tests/coverage/raw/numlib.c.gcov` の `#####` 行（未実行）を見てテストを追加する（最大 5 ラウンド）
5. `tests/results/YYYY-MM-DD_HH-MM_unit.md` に結果を書く：ラウンドごとの pass/fail、カバレッジ推移、追加したテスト、未カバー行とその理由、【設計判断】【要確認】の一覧

## 6. やってはいけないこと

- `SPEC.md` / `Makefile` / `AGENTS.md` の変更
- このディレクトリの外のファイルを読む・書く
- ネットワークアクセス、パッケージのインストール、`git push`
- カバレッジの数字のためだけの無意味なテスト。到達不能・防御的コードは「理由を書いて残す」
