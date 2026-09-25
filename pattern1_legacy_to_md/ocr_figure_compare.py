"""図（PNG）の中の文字を、中華系でないOCRエンジン3種で直接読み比べる。
- ocrmac  : Apple Vision（macOS標準・ローカル・追加ダウンロードなし）
- easyocr : JaidedAI（タイ）。モデルは GitHub から取得。Linux/Windows でも動く
- tesseract: Google 発の OSS。Linux/Windows の第一候補（Mac に無ければ Docker の Debian で実行）
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

print()
print("=== tesseract (jpn+eng, CLI) ===")
import shutil, subprocess
if not shutil.which("tesseract"):
    print("未導入。Mac で brew が使えない場合は Docker で: docker run --rm -v \"$PWD/input:/w:ro\" debian:bookworm-slim bash -c 'apt-get update -qq && apt-get install -y -qq tesseract-ocr tesseract-ocr-jpn && tesseract /w/_flow_gauss.png stdout -l jpn+eng --psm 3'")
else:
    for psm in ("3", "6"):
        t = time.time()
        r = subprocess.run(["tesseract", str(png), "stdout", "-l", "jpn+eng", "--psm", psm],
                           capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        print(f"--- psm {psm} ---")
        for l in lines:
            print(f"[    ] {l}")
        print(f"-- {len(lines)} 行, {time.time()-t:.1f}s")
