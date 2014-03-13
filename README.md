Nabo
====
파이썬 표준 라이브러리로 작성한 네이버 블로그 포스트 파서입니다.

"<아이디>.blog.me"와 "blog.naver.com/<아이디>" 도메인을 지원합니다.



Example
====
```
#-*- coding:UTF-8 -*-
from nabo import Nabo

mypost = Nabo( "아이디" )
mypost.open( "글 주소" )

# 글 제목
print mypost.DATA["POST_TITLE"]

# 작성 날짜
print mypost.DATA["POST_DATE"]

# 글 본문(html)
print mypost.DATA["POST_BODY"]

# 본문에 삽입된 이미지 주소들( tuple getIMGs(void) )
img_urls = mypost.getIMGs()

```



Loadmap
====
* Replace HTML code
* Port to other languages



License
====
LGPL v3
