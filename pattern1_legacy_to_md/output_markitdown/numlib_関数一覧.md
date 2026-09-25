## 関数一覧
| ID | 関数名 | 概要 | 引数（名前 : 型 : 制約） | 戻り値 | 備考 |
| --- | --- | --- | --- | --- | --- |
| F-001 | bubble\_sort\_i32 | int32 配列の昇順ソート（安定） | arr : int32\_t\* : n>0なら非NULL\nn : size\_t : 0以上 | 0=成功 / -1=引数不正 | O(n^2)。既ソートなら1パスで終了 |
| F-002 | gauss\_eliminate | Ax=b を掃き出し法で解く（部分ピボット） | a : double\* : n×n 行優先, 非NULL, 破壊可\nb : double\* : 長さn, 非NULL, 破壊可\nx : double\* : 長さn, 非NULL\nn : size\_t : 1..16 | 0=成功 / -1=引数不正 / -2=特異 / -3=n>16 | EPS=1e-12。条件数1e6以下で相対誤差1e-9以内 |

## エラーコード
| 値 | シンボル | 意味 |
| --- | --- | --- |
| 0 | NUMLIB\_OK | 成功 |
| -1 | NUMLIB\_E\_INVALID\_ARG | 引数不正 |
| -2 | NUMLIB\_E\_SINGULAR | 特異行列 |
| -3 | NUMLIB\_E\_TOO\_LARGE | n が 16 を超えた |

## 試験項目
| 試験ID | 関数 | 入力 | 期待結果 | 観点 |
| --- | --- | --- | --- | --- |
| T01 | bubble\_sort\_i32 | n=0 / n=1 | 0、配列不変 | 境界 |
| T03 | bubble\_sort\_i32 | 逆順 8 要素 | 0、昇順 | 正常 |
| T04 | bubble\_sort\_i32 | 重複値あり | 0、安定 | 安定性 |
| T06 | bubble\_sort\_i32 | arr=NULL, n=3 | -1 | 異常 |
| T08 | gauss\_eliminate | 2×2 既知解 | 0、誤差1e-9以内 | 精度 |
| T09 | gauss\_eliminate | a[0][0]=0 | 0、正しい解 | ピボット |
| T10 | gauss\_eliminate | 2行同一 | -2 | 特異 |
| T11 | gauss\_eliminate | n=17 | -3 | 境界 |