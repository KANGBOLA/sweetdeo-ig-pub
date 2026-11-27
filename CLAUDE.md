# CLAUDE.md — sweetdeo-ig-pub

@sweet_deo 데일리 IG 캐러셀의 **공개 이미지 호스트**(GitHub Pages).
Insta Graph API 가 `image_url` 을 서버에서 받아가야 해서, 게시용 JPG 만 모아 항상 켜 둔 공개 저장소다.

```
<YYYY-MM-DD>/        01.jpg ~ 10.jpg   게시용 마케팅 JPG (두 자리 번호)
                     caption.txt      게시 캡션 (내부 기록 블록 포함)
                     post.html        폰 게시용 패키지 페이지 (선택, 재생성 가능)
make-post-page.py    날짜 폴더 → post.html 생성 + 캡션 점검 (멱등)
index.html            Pages 루트 안내 페이지
oauth.html            연결 코드 표시 페이지 (noindex)
```

URL 규칙: `https://kangbola.github.io/sweetdeo-ig-pub/<날짜>/01.jpg`

## 자주 쓰는 명령

```bash
python3 make-post-page.py 2026-11-22          # post.html 생성 + 캡션 경고 출력
ls 2026-11-22 | grep -c '\.jpg$'              # 이미지 장수
curl -s -o /dev/null -w '%{http_code}\n' https://kangbola.github.io/sweetdeo-ig-pub/2026-11-22/01.jpg
```

## 작업 규칙

1. **계획 먼저** — 어느 날짜 폴더에 무엇을(이미지 교체/추가, post.html 생성) 하는지 먼저 정한다.
2. **실행 후 자가 검증** — `NN.jpg` 두 자리 규칙, 이미지 장수, `make-post-page.py` 의 경고 0건,
   공개 URL 200 응답까지 확인한다(`/verify-and-dryrun`).
3. `post.html` 은 생성물이다. 손으로 고친 내용은 다시 만들면 사라진다 — 고칠 것은 `caption.txt` 쪽이다.
4. 캡션 경고(첫 줄 125자·숫자 훅·빈 줄 문단·자사몰 CTA·해시태그 5개 상한)는 **고치지 말고 보고**한다.
   캡션을 만드는 쪽은 `sweetdeo-carousel` 의 생성기다.

## 주의

- **공개 저장소다.** 이 저장소에 올라간 것은 누구나 볼 수 있다. 토큰·API 키·주소·연락처·내부 메모를
  새로 넣지 않는다. 마케팅 JPG 이외의 파일(개인 사진·계약서·원본 PSD 등)을 올리지 않는다.
- **이미 나간 URL 은 바꾸지 않는다.** 게시된 IG 글이 그 URL 을 참조한다 — 파일 이름 변경·삭제·
  덮어쓰기는 이미 올라간 게시물의 이미지를 깨뜨린다. 교체가 필요하면 새 날짜 폴더에 올린다.
- 이미지 규격은 1080×1350 JPG, 파일명은 `01.jpg` 형식(2자리). `slide_` 접두사·PNG 를 쓰지 않는다.
- `oauth.html` 은 코드를 화면에만 표시한다. 여기에 값을 심거나 저장하지 않는다.
