# AGENTS.md（リポジトリ全体）

このリポジトリは「AI駆動開発で使える仕様書の作り方」のデモ。3段構成：

1. `pattern1_legacy_to_md/` … 既存の PowerPoint / Excel 仕様書 → Markdown（Docling）
2. `pattern2_req_to_spec/` … 要件 or 既存資料 → AIが仕様書を書く（Nemotron-3-Super と Claude の比較）
3. `pattern3_impl/` … AIが書いた仕様書 → 実装・単体試験・カバレッジ（ハーネス）

実装作業は **`pattern3_impl/` の中だけ**で行い、そこにある `AGENTS.md` のルールに従う。他ディレクトリは読み取りのみ。
