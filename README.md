Nabo
====
파이썬 표준 라이브러리로 작성한 네이버 블로그 포스트 파서입니다.
* 윈도에서만 실행 가능(리눅스 계열은 안됨)
* "<아이디>.blog.me"와 "blog.naver.com/<아이디>" 도메인 지원
* '전체공개' 되어있는 글만 파싱 가능



Example
====
```
#-*- coding:UTF-8 -*-
from nabo import Nabo

mypost = Nabo( "아이디" )
mypost.open( "글 주소" )

print mypost.DATA["POST_TITLE"] # 글 제목
print mypost.DATA["POST_DATE"] # 작성 날짜
print mypost.DATA["POST_BODY"] # 글 본문(html)

img_urls = mypost.getIMGs() # 본문의 이미지 주소들: tuple getIMGs( void )
```



Loadmap
====
* Support linux platform
* Using login session
* Return binary object(file, video, swf, etc..) urls
* Clean HTML code



License
====
LGPL v3
