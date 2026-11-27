---
description: 최근 날짜 폴더의 업로드 상태(장수·캡션·공개 URL)와 저장소 변경점을 점검한다
---

# 오늘 점검 — sweetdeo-ig-pub

> 이 저장소에는 워크플로가 없다. 다른 저장소(`sweetdeo-carousel`)가 폴더를 밀어 넣고 Pages 가 서빙한다.
> 그래서 점검은 **Actions 가 아니라 폴더와 공개 URL** 을 본다.

읽기 전용 점검이다. 파일을 고치거나 지우지 않는다.

## 1. 최근 폴더

```bash
ls -d 20*/ | tail -7
git log --oneline -10
git log --since="7 days ago" --name-only --pretty=format: | cut -d/ -f1 | sort -u | tail -10
```

- 최근 7일 사이 빠진 날짜가 있는지, 날짜 폴더가 규칙(`YYYY-MM-DD`)대로인지 본다.

## 2. 폴더 내용

```bash
D=$(ls -d 20*/ | tail -1 | tr -d /); echo "$D"
ls "$D"
ls "$D" | grep -c '\.jpg$'
head -3 "$D/caption.txt"
```

- 이미지가 `01.jpg`~ 두 자리 규칙이고 10장 내외인지, `caption.txt` 가 있는지.
- `_`, `slide_`, `.png` 같은 규칙 밖 파일이 섞였는지.

## 3. 공개 URL (실제로 서빙되는지)

```bash
D=$(ls -d 20*/ | tail -1 | tr -d /)
for f in $(ls "$D"/*.jpg | head -3); do
  printf '%s ' "$f"; curl -s -o /dev/null -w '%{http_code} %{size_download}B\n' "https://kangbola.github.io/sweetdeo-ig-pub/$f"
done
```

200 이 아니면 Pages 빌드 지연(수 분)인지, 경로 오타인지 구분한다.

## 4. 저장소 위생 (공개 저장소)

```bash
git ls-files | grep -v -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}/|^(README|index)\.|make-post-page\.py$|oauth\.html$'
git ls-files | grep -i -E 'token|secret|\.env|key' | head
```

규칙 밖 파일이나 비밀값으로 보이는 것이 있으면 **지우지 말고** 경로와 함께 보고한다.

## 5. 보고

- 최근 폴더와 장수, 공개 URL 상태, 이미 올라간 글과 어긋나는 흔적 — **5줄 이내**.
