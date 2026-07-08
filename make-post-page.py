# -*- coding: utf-8 -*-
"""Generate a phone-post package page (post.html) for a given date folder.
Usage: python make-post-page.py 2026-07-09
Reads <date>/caption.txt, emits <date>/post.html referencing the public
GitHub Pages image URLs. Idempotent — safe to re-run.
"""
import sys, json, os

BASE_HOST = "https://kangbola.github.io/sweetdeo-ig-pub/"
ROOT = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IG 게시 패키지 · __DATE__</title>
<style>
  :root{--bg:#0f1020;--card:#1a1b2e;--ink:#f4f4f8;--muted:#9aa0b4;--accent:#ff4a6e}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:16px}
  h1{font-size:19px;margin:4px 0 2px}
  .sub{color:var(--muted);font-size:13px;margin-bottom:16px}
  .step{background:var(--card);border-radius:14px;padding:14px 16px;margin:12px 0}
  .step b{color:var(--accent)}
  ol{margin:6px 0 0;padding-left:20px}
  li{margin:3px 0}
  .imgs{display:flex;flex-direction:column;gap:10px;margin-top:8px}
  figure{margin:0;background:var(--card);border-radius:14px;overflow:hidden}
  figcaption{font-size:13px;color:var(--muted);padding:8px 12px}
  img{width:100%;display:block}
  .num{position:relative}
  .badge{position:absolute;top:8px;left:8px;background:rgba(0,0,0,.72);color:#fff;font-weight:700;border-radius:999px;padding:2px 11px;font-size:13px}
  textarea{width:100%;min-height:230px;background:#0b0c18;color:var(--ink);border:1px solid #2a2c44;border-radius:12px;padding:12px;font:14px/1.55 inherit;resize:vertical}
  button{background:var(--accent);color:#fff;border:0;border-radius:10px;padding:11px 16px;font-size:15px;font-weight:700;width:100%;margin-top:8px}
  .hint{font-size:12px;color:var(--muted);margin-top:6px}
</style>
</head>
<body>
  <h1>📲 IG 게시 패키지</h1>
  <div class="sub">sweet_deo · __DATE__ · 캐러셀 10장 + 본문</div>

  <div class="step">
    <b>올리는 법 (인스타 앱)</b>
    <ol>
      <li>아래 이미지 <b>10장을 순서대로</b> 길게 눌러 사진첩에 저장</li>
      <li>인스타 앱 → ➕ → <b>게시물</b> → 여러장 선택(01→10 순서 확인)</li>
      <li>본문 <b>복사</b> 버튼 → 캡션에 붙여넣기 → 공유</li>
    </ol>
    <div class="hint">순서 중요: 첫 장(01)이 후킹, 마지막(10)이 CTA예요.</div>
  </div>

  <div class="step">
    <b>본문 (탭해서 전체선택 → 복사)</b>
    <textarea id="cap" readonly></textarea>
    <button onclick="copyCap()">본문 복사하기</button>
    <div class="hint" id="msg"></div>
  </div>

  <div class="imgs" id="imgs"></div>

  <script>
    var BASE=__BASE__;
    var caption=__CAPTION__;
    document.getElementById('cap').value=caption;
    var wrap=document.getElementById('imgs');
    for(var i=1;i<=10;i++){
      var nn=(i<10?'0'+i:''+i);
      var fig=document.createElement('figure');
      fig.innerHTML='<div class="num"><span class="badge">'+nn+'</span>'+
        '<img loading="lazy" src="'+BASE+nn+'.jpg" alt="slide '+nn+'"></div>'+
        '<figcaption>'+i+'번째 · 길게 눌러 저장</figcaption>';
      wrap.appendChild(fig);
    }
    function copyCap(){
      var t=document.getElementById('cap');
      t.focus(); t.select(); t.setSelectionRange(0,99999);
      try{
        if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t.value);}
        else{document.execCommand('copy');}
        document.getElementById('msg').textContent='✅ 복사됨 — 인스타 캡션에 붙여넣기';
      }catch(e){
        document.getElementById('msg').textContent='복사 안 되면 글자영역 길게 눌러 수동 복사';
      }
    }
  </script>
</body>
</html>
"""

def main():
    if len(sys.argv) < 2:
        print("usage: python make-post-page.py <YYYY-MM-DD>"); sys.exit(1)
    date = sys.argv[1]
    folder = os.path.join(ROOT, date)
    cap_path = os.path.join(folder, "caption.txt")
    if not os.path.isfile(cap_path):
        print("no caption.txt in", folder); sys.exit(1)
    caption = open(cap_path, encoding="utf-8").read().strip()
    base = BASE_HOST + date + "/"
    html = (TEMPLATE
            .replace("__DATE__", date)
            .replace("__BASE__", json.dumps(base))
            .replace("__CAPTION__", json.dumps(caption, ensure_ascii=False)))
    out = os.path.join(folder, "post.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out)

if __name__ == "__main__":
    main()
