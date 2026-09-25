"""ダミーの「レガシー仕様書」を作る（PowerPoint + Excel）。

先方の実資料は機密で使えないため、その書き方（パワポに細かく／Excelの関数一覧表）を
模した架空の C ライブラリ仕様書を自作する。実在の製品・顧客とは無関係。
題材: バブルソート（bubble_sort_i32）と 掃き出し法（gauss_eliminate）。
6枚目の処理フローは「画像として貼られた図」（テキスト情報を持たない）にして、OCR が要るケースを再現する。
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE / "input"
OUT.mkdir(exist_ok=True)

# ---------- 画像（フロー図）を PIL で描く ----------
def load_font(size):
    for p in ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
              "/System/Library/Fonts/Hiragino Sans GB.ttc"]:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()

def make_flow_png(path):
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f = load_font(30); fs = load_font(24)
    steps = [
        "開始（k = 0）",
        "列 k で |a[i][k]| が最大の行 p を選ぶ（部分ピボット選択）",
        "|a[p][k]| < EPS(1e-12) ？ → Yes: E_SINGULAR(-2) を返して終了",
        "行 k と行 p を入れ替える（a と b の両方）",
        "行 k を a[k][k] で割って正規化（対角成分を 1 にする）",
        "他のすべての行 i≠k から a[i][k] × (行 k) を引く",
        "k = k + 1。k < n なら 2 へ戻る",
        "x[i] = b[i] を出力して 0 を返す",
    ]
    x0, y = 120, 60
    for i, s in enumerate(steps):
        d.rounded_rectangle([x0, y, W - x0, y + 80], radius=14, outline="#1f3b73", width=4, fill="#eef3fb")
        d.text((x0 + 24, y + 22), f"{i+1}. {s}", font=f, fill="#111")
        if i < len(steps) - 1:
            d.line([W // 2, y + 80, W // 2, y + 110], fill="#1f3b73", width=4)
            d.polygon([(W // 2 - 10, y + 104), (W // 2 + 10, y + 104), (W // 2, y + 118)], fill="#1f3b73")
        y += 118
    d.text((x0, H - 40), "図6-1 掃き出し法（ガウスの消去法）の処理フロー  ※ EPS は 1e-12 固定", font=fs, fill="#444")
    img.save(path)

flow_png = OUT / "_flow_gauss.png"
make_flow_png(flow_png)

# ---------- PowerPoint ----------
prs = Presentation()
def title_slide(t, sub):
    s = prs.slides.add_slide(prs.slide_layouts[0]); s.shapes.title.text = t; s.placeholders[1].text = sub
def bullet_slide(t, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1]); s.shapes.title.text = t
    tf = s.placeholders[1].text_frame; tf.clear()
    for i, (lvl, txt) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.text = txt; p.level = lvl; p.font.size = Pt(18)
    return s
def table_slide(t, header, rows, col_w=None):
    s = prs.slides.add_slide(prs.slide_layouts[5]); s.shapes.title.text = t
    shape = s.shapes.add_table(len(rows) + 1, len(header), Inches(0.4), Inches(1.4), Inches(9.2), Inches(0.4))
    tb = shape.table
    for c, h in enumerate(header): tb.cell(0, c).text = h
    for r, row in enumerate(rows, start=1):
        for c, v in enumerate(row): tb.cell(r, c).text = str(v)
    for r in range(len(rows) + 1):
        for c in range(len(header)):
            for p in tb.cell(r, c).text_frame.paragraphs: p.font.size = Pt(12)
    if col_w:
        for c, w in enumerate(col_w): tb.columns[c].width = Inches(w)
    return s

title_slide("数値処理ライブラリ numlib 機能仕様書（抜粋）",
            "版数 0.9 ／ 作成日 2026-09-25 ／ 制御ソフト第二課\n※ AI検証用のダミー資料。実在の製品・顧客とは無関係")
bullet_slide("1. 概要と前提", [
    (0, "目的：組込み制御ソフト向けの小規模な数値処理ライブラリ"),
    (0, "対象言語：C（C99準拠）。コンパイラ警告ゼロ（-Wall -Wextra）"),
    (0, "制約"), (1, "動的メモリ確保（malloc/free）は使用しない"), (1, "スレッドセーフ非対応（呼び出し側で排他）"),
    (1, "依存ヘッダは <stddef.h> <stdint.h> のみ"), (1, "浮動小数点は double。printf 等の標準I/Oは使わない"),
    (0, "提供関数"), (1, "bubble_sort_i32 … 32bit整数配列の昇順ソート（バブルソート・安定）"),
    (1, "gauss_eliminate … 連立一次方程式 Ax = b を掃き出し法で解く"),
])
table_slide("2. 関数仕様：bubble_sort_i32", ["項目", "内容"], [
    ["シグネチャ", "int bubble_sort_i32(int32_t *arr, size_t n);"],
    ["目的", "arr[0..n-1] を昇順に並べ替える。等しい値の相対順序は保つ（安定ソート）"],
    ["引数 arr", "整列対象の配列。n > 0 のとき非NULL であること"],
    ["引数 n", "要素数。0 以上。n <= 1 のときは何もしない"],
    ["戻り値", "0：成功 ／ -1：引数不正（n > 0 かつ arr == NULL）"],
    ["事後条件", "成功時、すべての i について arr[i] <= arr[i+1]。要素の多重集合は不変"],
    ["計算量", "時間 O(n^2)、追加メモリ O(1)。既ソート入力では 1 パスで終了する（早期終了フラグ）"],
], col_w=[2.0, 7.2])
table_slide("3. 関数仕様：gauss_eliminate（掃き出し法）", ["項目", "内容"], [
    ["シグネチャ", "int gauss_eliminate(double *a, double *b, double *x, size_t n);"],
    ["目的", "n×n 行列 A と右辺 b から Ax = b の解 x を求める（部分ピボット選択付き掃き出し法）"],
    ["引数 a", "n×n 行列を行優先（row-major）で格納した配列。非NULL。作業領域として破壊してよい"],
    ["引数 b", "右辺ベクトル（長さ n）。非NULL。作業領域として破壊してよい"],
    ["引数 x", "解の出力先（長さ n）。非NULL"],
    ["引数 n", "次元。1 以上 16 以下（NUMLIB_MAX_DIM = 16）"],
    ["戻り値", "0：成功 ／ -1：引数不正（NULL または n == 0）／ -2：特異行列 ／ -3：n > 16"],
    ["特異判定", "ピボット選択後の |a[k][k]| < 1e-12 のとき特異とみなす（EPS はヘッダで定数定義）"],
    ["精度", "条件数 1e6 以下の行列で相対誤差 1e-9 以内"],
], col_w=[2.0, 7.2])
table_slide("4. エラーコード一覧", ["値", "シンボル", "意味", "発生する関数"], [
    ["0", "NUMLIB_OK", "成功", "全関数"],
    ["-1", "NUMLIB_E_INVALID_ARG", "NULL ポインタ、n == 0 など引数不正", "全関数"],
    ["-2", "NUMLIB_E_SINGULAR", "特異行列（解が一意に定まらない）", "gauss_eliminate"],
    ["-3", "NUMLIB_E_TOO_LARGE", "n が NUMLIB_MAX_DIM(16) を超えた", "gauss_eliminate"],
], col_w=[0.8, 3.0, 3.6, 1.8])
s = prs.slides.add_slide(prs.slide_layouts[5]); s.shapes.title.text = "5. 処理フロー：gauss_eliminate（図のみ・テキスト情報なし）"
s.shapes.add_picture(str(flow_png), Inches(0.8), Inches(1.3), width=Inches(8.4))
table_slide("6. 単体試験観点", ["No", "対象", "観点", "期待結果"], [
    ["T01", "bubble_sort_i32", "n = 0 / n = 1", "0 を返し配列は不変"],
    ["T02", "bubble_sort_i32", "既に昇順の入力", "0、順序不変、比較は 1 パスのみ"],
    ["T03", "bubble_sort_i32", "逆順の入力（n = 8）", "0、昇順になる"],
    ["T04", "bubble_sort_i32", "重複値を含む入力", "0、安定性が保たれる"],
    ["T05", "bubble_sort_i32", "INT32_MIN / INT32_MAX を含む", "0、オーバーフローなく整列"],
    ["T06", "bubble_sort_i32", "arr == NULL, n = 3", "-1"],
    ["T07", "gauss_eliminate", "単位行列 A = I, b 任意", "0、x == b"],
    ["T08", "gauss_eliminate", "2×2 で解が既知（x = (1, 2)）", "0、誤差 1e-9 以内"],
    ["T09", "gauss_eliminate", "ピボット入替が必要（a[0][0] = 0）", "0、正しい解"],
    ["T10", "gauss_eliminate", "特異行列（2行が同一）", "-2"],
    ["T11", "gauss_eliminate", "n = 17", "-3"],
    ["T12", "gauss_eliminate", "a == NULL / n == 0", "-1"],
], col_w=[0.7, 2.2, 3.6, 2.7])
table_slide("7. 改訂履歴", ["版", "日付", "内容", "作成者"], [
    ["0.8", "2026-09-10", "初版（レビュー前）", "制御ソフト第二課"],
    ["0.9", "2026-09-25", "エラーコード -3 を追加、試験観点 T09〜T12 追記", "制御ソフト第二課"],
], col_w=[0.7, 1.6, 5.2, 1.7])
pptx_path = OUT / "numlib_機能仕様書_v0.9.pptx"
prs.save(pptx_path)

# ---------- Excel ----------
wb = Workbook()
ws = wb.active; ws.title = "関数一覧"
ws.append(["ID", "関数名", "概要", "引数（名前 : 型 : 制約）", "戻り値", "備考"])
ws.append(["F-001", "bubble_sort_i32", "int32 配列の昇順ソート（安定）",
           "arr : int32_t* : n>0なら非NULL\nn : size_t : 0以上", "0=成功 / -1=引数不正", "O(n^2)。既ソートなら1パスで終了"])
ws.append(["F-002", "gauss_eliminate", "Ax=b を掃き出し法で解く（部分ピボット）",
           "a : double* : n×n 行優先, 非NULL, 破壊可\nb : double* : 長さn, 非NULL, 破壊可\nx : double* : 長さn, 非NULL\nn : size_t : 1..16",
           "0=成功 / -1=引数不正 / -2=特異 / -3=n>16", "EPS=1e-12。条件数1e6以下で相対誤差1e-9以内"])
ws2 = wb.create_sheet("エラーコード")
ws2.append(["値", "シンボル", "意味"])
for r in [[0, "NUMLIB_OK", "成功"], [-1, "NUMLIB_E_INVALID_ARG", "引数不正"], [-2, "NUMLIB_E_SINGULAR", "特異行列"], [-3, "NUMLIB_E_TOO_LARGE", "n が 16 を超えた"]]:
    ws2.append(r)
ws3 = wb.create_sheet("試験項目")
ws3.append(["試験ID", "関数", "入力", "期待結果", "観点"])
for r in [["T01", "bubble_sort_i32", "n=0 / n=1", "0、配列不変", "境界"],
          ["T03", "bubble_sort_i32", "逆順 8 要素", "0、昇順", "正常"],
          ["T04", "bubble_sort_i32", "重複値あり", "0、安定", "安定性"],
          ["T06", "bubble_sort_i32", "arr=NULL, n=3", "-1", "異常"],
          ["T08", "gauss_eliminate", "2×2 既知解", "0、誤差1e-9以内", "精度"],
          ["T09", "gauss_eliminate", "a[0][0]=0", "0、正しい解", "ピボット"],
          ["T10", "gauss_eliminate", "2行同一", "-2", "特異"],
          ["T11", "gauss_eliminate", "n=17", "-3", "境界"]]:
    ws3.append(r)
for w in (ws, ws2, ws3):
    for c in w[1]: c.font = Font(bold=True)
    for row in w.iter_rows():
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    w.column_dimensions["C"].width = 40; w.column_dimensions["D"].width = 44
xlsx_path = OUT / "numlib_関数一覧.xlsx"
wb.save(xlsx_path)
print("wrote", pptx_path.name, pptx_path.stat().st_size, "bytes")
print("wrote", xlsx_path.name, xlsx_path.stat().st_size, "bytes")
