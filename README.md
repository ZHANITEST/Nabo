Nabo
====
파이썬 표준 라이브러리로 작성한 네이버 블로그 포스트 파서입니다.
* "<아이디>.blog.me"와 "blog.naver.com/<아이디>" 도메인 지원
* '전체공개' 되어있는 글만 파싱 가능



Example
====
See '/demo/test.py'.
```
#-*- coding:UTF-8 -*-
from nabo import Nabo

mypost = Nabo( "아이디" )
mypost.open( "글 주소" )

print mypost.DATA["naver"]["title"] # 글 제목
print mypost.DATA["naver"]["date"]  # 작성 날짜
print mypost.DATA["naver"]["body"]  # 글 본문(html)
```



Loadmap
====
* Using login session
* Return binary object(file, video, swf, etc..) urls
* Clean HTML code



License
====
LGPL v3
