---
description: 날짜 폴더 추가·캡션 수정 후 명명 규칙·캡션 점검·공개 URL로 자가 검증한다
---

# 검증 — sweetdeo-ig-pub

날짜 폴더를 넣거나 캡션을 고친 뒤, 게시하기 전에 확인한다.
**이미 커밋된 폴더의 이미지를 덮어쓰거나 이름을 바꾸지 않는다** — 게시된 IG 글이 그 URL 을 참조한다.

날짜는 `$ARGUMENTS` 가 있으면 그것(YYYY-MM-DD), 없으면 가장 최근 폴더를 쓴다.

## 1. 구조·명명 규칙

```bash
D=<날짜>; ls "$D"
ls "$D" | grep -c '\.jpg$'
```

- JPG 만, 파일명 `NN.jpg`(두 자리). PNG·`slide_` 접두사·공백·한글 파일명이 있으면 실패로 본다.
- 캐러셀은 보통 10장(`01`~`10`). 장수가 다르면 그 자체를 보고한다.

## 2. 캡션 점검 (생성기가 경고를 낸다)

```bash
python3 make-post-page.py "$D"
```

- 경고(⚠️) 항목을 그대로 보고한다: 첫 줄 125자·숫자 훅, 빈 줄 문단, `sweetdeo.cafe24.com` CTA,
  해시태그 개수(상한 5)·한국어 태그 유무.
- **캡션을 임의로 고치지 않는다.** 생성기(`sweetdeo-carousel` 의 `research_bot`)가 원본이다.

## 3. 공개 서빙 확인

```bash
for f in $(ls "$D"/*.jpg); do printf '%s ' "$f"; curl -s -o /dev/null -w '%{http_code}\n' "https://kangbola.github.io/sweetdeo-ig-pub/$f"; done
```

푸시 직후 404 는 Pages 빌드 지연일 수 있다 — 1~2분 뒤 다시 확인하고, 계속 404 면 경로·브랜치를 본다.

## 4. 커밋 전 확인

```bash
git status --short
git diff --stat
```

- 추가된 것이 이미지·캡션·post.html 뿐인지(비밀값·개인 파일이 섞이지 않았는지).
- 기존 날짜 폴더의 수정/삭제가 포함되면 **멈추고** 이유를 확인한다.

## 5. 요약

- 폴더·장수·캡션 경고 수, 공개 URL 응답 코드
- 커밋에 포함될 파일 목록과, 남은 위험(기존 URL 변경 여부)
