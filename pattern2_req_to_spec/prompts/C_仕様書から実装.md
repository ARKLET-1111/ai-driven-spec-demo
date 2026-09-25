カレントディレクトリ `pattern3_impl/` の `AGENTS.md` と `SPEC.md` を最後まで読み、AGENTS.md の「作業手順」どおりに numlib を実装してください。

1. `numlib.h` → `numlib.c` → `test_numlib.c` の順に作成する（テストは SPEC §8 の観点IDをコメントに書き、全観点を網羅する）
2. `make test` が通るまで修正する（SPEC が正）
3. `make coverage` を実行し、行カバレッジ 90% 以上になるまで `tests/coverage/raw/numlib.c.gcov` の未実行行（`#####`）を見てテストを追加する（最大 5 ラウンド）
4. `tests/results/YYYY-MM-DD_HH-MM_unit.md` に結果を保存する（ラウンドごとの pass/fail、カバレッジ推移、追加したテスト、未カバー行と理由、【設計判断】【要確認】）
5. 最後に、作成したファイル一覧・テスト件数・最終カバレッジ・【設計判断】【要確認】の一覧を報告する

守ること: `SPEC.md` / `Makefile` / `AGENTS.md` は変更しない。このディレクトリの外に触らない。ネットワークやパッケージのインストールをしない。
