# -*- coding: utf-8 -*-
"""Generate a phone-post package page (post.html) for a given date folder.

Usage: python make-post-page.py 2026-07-09
Reads <date>/caption.txt, emits <date>/post.html referencing the public
GitHub Pages image URLs. Idempotent — safe to re-run.

2026-11-21 (진단 반영) 추가:
  · **한 덱 = 한 형식** 안내. 같은 덱을 캐러셀(/p/)과 릴스(/reel/)로 둘 다 올리면
    그리드에 같은 카드가 두 번 보인다(실제 @sweet_deo 그리드에서 확인).
  · 캡션 자동 점검 — 첫 125자 훅, 문단 구분, 자사몰 CTA, 한국어 해시태그.
    점검은 **경고만** 한다. 캡션을 고치는 것은 생성기(research_bot) 쪽 일이다.
"""
import sys, json, os, re

BASE_HOST = "https://kangbola.github.io/sweetdeo-ig-pub/"
ROOT = os.path.dirname(os.path.abspath(__file__))

HOOK_MAX = 125
MALL = "sweetdeo.cafe24.com"

TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IG 게시 패키지 · __DATE__</title>
<style>
  :root{--bg:#0f1020;--card:#1a1b2e;--ink:#f4f4f8;--muted:#9aa0b4;--accent:#ff4a6e;--ok:#3ddc97;--warn:#ffc857}
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
  .one{background:#241a10;border:1px solid #4a3418}
  .one b{color:var(--warn)}
  .audit{font-size:13px;line-height:1.6}
  .audit ul{margin:6px 0 0;padding-left:20px}
  .audit li{color:var(--warn);margin:3px 0}
  .audit .pass{color:var(--ok);font-weight:700}
</style>
</head>
<body>
  <h1>📲 IG 게시 패키지</h1>
  <div class="sub">sweet_deo · __DATE__ · 캐러셀 10장 + 본문</div>

  <div class="step one">
    <b>오늘은 한 형식만</b>
    <ul style="margin:6px 0 0;padding-left:20px">
      <li>이 덱은 <b>캐러셀(10장)</b> 또는 <b>릴스(영상)</b> 중 <b>하나로만</b> 올립니다.</li>
      <li>둘 다 올리면 같은 카드가 그리드에 두 번 연속 보입니다(2026-11-21 실제 확인).</li>
      <li>릴스로 올렸다면 오늘은 여기서 끝 — 캐러셀은 올리지 않습니다.</li>
    </ul>
    <div class="hint">한 형식만 골라도 팔로워는 같은 글을 한 번 봅니다. 남는 슬롯은 내일 덱에 씁니다.</div>
  </div>

  <div class="step audit">
    <b>캡션 점검</b>
    __AUDIT__
  </div>

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


def _strip_internal(cap: str) -> str:
    """[한글 캡션]/[English caption]/[해시태그] 머리만 남기고 내부 기록 블록은 버린다."""
    keep = ("한글 캡션", "English caption", "해시태그")
    out, keep_on = [], True
    for line in cap.splitlines():
        m = re.match(r"^\[(.+?)\]\s*$", line.strip())
        if m:
            keep_on = m.group(1) in keep
            if keep_on:
                out.append("")
            continue
        if keep_on:
            out.append(line)
    return "\n".join(out).strip()


def audit_caption(cap: str):
    """게시 전 최소 점검. (warnings, passed) — 고치지는 않는다."""
    warn, ok = [], []
    text = _strip_internal(cap)
    first = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
    if len(first) > HOOK_MAX:
        warn.append(f"첫 줄이 {len(first)}자 — 피드에서 {HOOK_MAX}자에서 접혀 문장이 잘립니다.")
    elif not re.search(r"\d", first):
        warn.append(f"첫 줄({len(first)}자)에 숫자가 없습니다 — '결론 + 숫자' 훅이 더 셉니다.")
    else:
        ok.append(f"첫 줄 {len(first)}자 — 접히는 지점 안에서 끝납니다.")
    if "\n\n" not in text:
        warn.append("문단 구분(빈 줄)이 없습니다 — 한 덩어리로 보여 읽히지 않습니다.")
    else:
        ok.append("문단이 빈 줄로 나뉩니다.")
    if MALL not in text:
        warn.append(f"자사몰 CTA가 없습니다 — 캡션에 {MALL} 한 줄을 넣으세요.")
    else:
        ok.append("자사몰 CTA 있음.")
    tags = re.findall(r"#[^\s#]+", text)
    ko = [t for t in tags if re.search(r"[가-힣]", t)]
    if not tags:
        warn.append("해시태그가 없습니다 — 한국어 5 + 영어 3을 권합니다.")
    elif not ko:
        warn.append(f"해시태그 {len(tags)}개가 전부 영어입니다 — 한국어 검색 유입이 0이 됩니다.")
    elif not (4 <= len(ko) <= 8):
        warn.append(f"한국어 해시태그 {len(ko)}개 — 5개 내외로 맞추세요.")
    else:
        ok.append(f"해시태그 {len(tags)}개(한국어 {len(ko)}) — 5+3 형태에 가깝습니다.")
    return warn, ok


def audit_html(warn, ok):
    if not warn and not ok:
        return "<div class='hint'>점검할 캡션이 없습니다.</div>"
    parts = []
    if not warn:
        parts.append("<span class='pass'>통과 — 게시 전 점검에서 걸린 것이 없습니다.</span>")
    else:
        parts.append("<ul>" + "".join(f"<li>{w}</li>" for w in warn) + "</ul>")
    if ok:
        parts.append("<div class='hint'>" + " / ".join(ok) + "</div>")
    return "".join(parts)


def main():
    if len(sys.argv) < 2:
        print("usage: python make-post-page.py <YYYY-MM-DD>"); sys.exit(1)
    date = sys.argv[1]
    folder = os.path.join(ROOT, date)
    cap_path = os.path.join(folder, "caption.txt")
    if not os.path.isfile(cap_path):
        print("no caption.txt in", folder); sys.exit(1)
    caption = open(cap_path, encoding="utf-8").read().strip()
    warn, ok = audit_caption(caption)
    base = BASE_HOST + date + "/"
    html = (TEMPLATE
            .replace("__DATE__", date)
            .replace("__AUDIT__", audit_html(warn, ok))
            .replace("__BASE__", json.dumps(base))
            .replace("__CAPTION__", json.dumps(caption, ensure_ascii=False)))
    out = os.path.join(folder, "post.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out)
    for w in warn:
        print("  ⚠️", w)
    if not warn:
        print("  ✅ 캡션 점검 통과")


if __name__ == "__main__":
    main()
