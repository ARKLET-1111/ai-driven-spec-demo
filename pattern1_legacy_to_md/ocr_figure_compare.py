"""図（PNG）の中の文字を、中華系でないOCRエンジン2種で直接読み比べる。
- ocrmac  : Apple Vision（macOS標準・ローカル・追加ダウンロードなし）
- easyocr : JaidedAI（タイ）。モデルは GitHub から取得。Linux/Windows でも動く
Docling の既定 RapidOCR（PaddleOCR系・中国）は先方NGのため使わない。
"""
import sys, time
from pathlib import Path
png = Path(sys.argv[1])

print("=== ocrmac (Apple Vision) ===")
try:
    from ocrmac import ocrmac
    t = time.time()
    res = ocrmac.OCR(str(png), language_preference=["ja-JP", "en-US"], recognition_level="accurate").recognize()
    # 上から順に並べる（Vision の座標は左下原点なので y を反転）
    res.sort(key=lambda r: (-r[2][1], r[2][0]))
    for text, conf, box in res:
        print(f"[{conf:.2f}] {text}")
    print(f"-- {len(res)} 行, {time.time()-t:.1f}s")
except Exception as e:
    print("失敗:", type(e).__name__, e)

print()
print("=== easyocr (ja+en, CPU) ===")
try:
    import easyocr
    t = time.time()
    reader = easyocr.Reader(["ja", "en"], gpu=False, verbose=False)
    lines = reader.readtext(str(png), detail=1, paragraph=False)
    lines.sort(key=lambda r: (r[0][0][1], r[0][0][0]))
    for box, text, conf in lines:
        print(f"[{conf:.2f}] {text}")
    print(f"-- {len(lines)} 行, {time.time()-t:.1f}s")
except Exception as e:
    print("失敗:", type(e).__name__, e)
