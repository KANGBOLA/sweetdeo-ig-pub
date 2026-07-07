# sweetdeo-ig-pub
SWEETDEO 데일리 IG 캐러셀 **공개 이미지 호스트** (GitHub Pages).
- 구조: `<YYYY-MM-DD>/NN.jpg` (게시용 마케팅 JPG) + `caption.txt`
- 상시 공개 → IG Graph API가 `image_url`을 서버사이드로 페치 (happylife 전원 무관)
- 게시(AWS Lambda)와 빌드(happylife 17:00)를 분리하기 위한 항상-켜짐 호스팅
- 마케팅 이미지 전용. 민감 파일 금지.
