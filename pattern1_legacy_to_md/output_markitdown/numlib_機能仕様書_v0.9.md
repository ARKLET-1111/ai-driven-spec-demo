<!-- Slide number: 1 -->
# 数値処理ライブラリ numlib 機能仕様書（抜粋）
版数 0.9 ／ 作成日 2026-09-25 ／ 制御ソフト第二課
※ AI検証用のダミー資料。実在の製品・顧客とは無関係

<!-- Slide number: 2 -->
# 1. 概要と前提
目的：組込み制御ソフト向けの小規模な数値処理ライブラリ
対象言語：C（C99準拠）。コンパイラ警告ゼロ（-Wall -Wextra）
制約
動的メモリ確保（malloc/free）は使用しない
スレッドセーフ非対応（呼び出し側で排他）
依存ヘッダは <stddef.h> <stdint.h> のみ
浮動小数点は double。printf 等の標準I/Oは使わない
提供関数
bubble_sort_i32 … 32bit整数配列の昇順ソート（バブルソート・安定）
gauss_eliminate … 連立一次方程式 Ax = b を掃き出し法で解く

<!-- Slide number: 3 -->
# 2. 関数仕様：bubble_sort_i32
| 項目 | 内容 |
| --- | --- |
| シグネチャ | int bubble\_sort\_i32(int32\_t \*arr, size\_t n); |
| 目的 | arr[0..n-1] を昇順に並べ替える。等しい値の相対順序は保つ（安定ソート） |
| 引数 arr | 整列対象の配列。n > 0 のとき非NULL であること |
| 引数 n | 要素数。0 以上。n <= 1 のときは何もしない |
| 戻り値 | 0：成功 ／ -1：引数不正（n > 0 かつ arr == NULL） |
| 事後条件 | 成功時、すべての i について arr[i] <= arr[i+1]。要素の多重集合は不変 |
| 計算量 | 時間 O(n^2)、追加メモリ O(1)。既ソート入力では 1 パスで終了する（早期終了フラグ） |

<!-- Slide number: 4 -->
# 3. 関数仕様：gauss_eliminate（掃き出し法）
| 項目 | 内容 |
| --- | --- |
| シグネチャ | int gauss\_eliminate(double \*a, double \*b, double \*x, size\_t n); |
| 目的 | n×n 行列 A と右辺 b から Ax = b の解 x を求める（部分ピボット選択付き掃き出し法） |
| 引数 a | n×n 行列を行優先（row-major）で格納した配列。非NULL。作業領域として破壊してよい |
| 引数 b | 右辺ベクトル（長さ n）。非NULL。作業領域として破壊してよい |
| 引数 x | 解の出力先（長さ n）。非NULL |
| 引数 n | 次元。1 以上 16 以下（NUMLIB\_MAX\_DIM = 16） |
| 戻り値 | 0：成功 ／ -1：引数不正（NULL または n == 0）／ -2：特異行列 ／ -3：n > 16 |
| 特異判定 | ピボット選択後の |a[k][k]| < 1e-12 のとき特異とみなす（EPS はヘッダで定数定義） |
| 精度 | 条件数 1e6 以下の行列で相対誤差 1e-9 以内 |

<!-- Slide number: 5 -->
# 4. エラーコード一覧
| 値 | シンボル | 意味 | 発生する関数 |
| --- | --- | --- | --- |
| 0 | NUMLIB\_OK | 成功 | 全関数 |
| -1 | NUMLIB\_E\_INVALID\_ARG | NULL ポインタ、n == 0 など引数不正 | 全関数 |
| -2 | NUMLIB\_E\_SINGULAR | 特異行列（解が一意に定まらない） | gauss\_eliminate |
| -3 | NUMLIB\_E\_TOO\_LARGE | n が NUMLIB\_MAX\_DIM(16) を超えた | gauss\_eliminate |

<!-- Slide number: 6 -->
# 5. 処理フロー：gauss_eliminate（図のみ・テキスト情報なし）

![_flow_gauss.png](Picture2.jpg)

<!-- Slide number: 7 -->
# 6. 単体試験観点
| No | 対象 | 観点 | 期待結果 |
| --- | --- | --- | --- |
| T01 | bubble\_sort\_i32 | n = 0 / n = 1 | 0 を返し配列は不変 |
| T02 | bubble\_sort\_i32 | 既に昇順の入力 | 0、順序不変、比較は 1 パスのみ |
| T03 | bubble\_sort\_i32 | 逆順の入力（n = 8） | 0、昇順になる |
| T04 | bubble\_sort\_i32 | 重複値を含む入力 | 0、安定性が保たれる |
| T05 | bubble\_sort\_i32 | INT32\_MIN / INT32\_MAX を含む | 0、オーバーフローなく整列 |
| T06 | bubble\_sort\_i32 | arr == NULL, n = 3 | -1 |
| T07 | gauss\_eliminate | 単位行列 A = I, b 任意 | 0、x == b |
| T08 | gauss\_eliminate | 2×2 で解が既知（x = (1, 2)） | 0、誤差 1e-9 以内 |
| T09 | gauss\_eliminate | ピボット入替が必要（a[0][0] = 0） | 0、正しい解 |
| T10 | gauss\_eliminate | 特異行列（2行が同一） | -2 |
| T11 | gauss\_eliminate | n = 17 | -3 |
| T12 | gauss\_eliminate | a == NULL / n == 0 | -1 |

<!-- Slide number: 8 -->
# 7. 改訂履歴
| 版 | 日付 | 内容 | 作成者 |
| --- | --- | --- | --- |
| 0.8 | 2026-09-10 | 初版（レビュー前） | 制御ソフト第二課 |
| 0.9 | 2026-09-25 | エラーコード -3 を追加、試験観点 T09〜T12 追記 | 制御ソフト第二課 |