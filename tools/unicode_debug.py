#-*- coding:UTF-8 -*-
#===================================================================================================
#
# unicode_debugger.py (for Nabo)
# Debug test for 'UnicodeEncodeError'
#
# 2014, XKY
# License: LGPL v3
#
#===================================================================================================
from nabo import Nabo #Parser

if __name__ == "__main__":
	# Target: http://blogpeople.blog.me/150181071013
	test = Nabo("blogpeople")
	test.open("http://blogpeople.blog.me/150181071013")
	
	print test.DATA["naver"]["title"]
	print test.showType( "body" )
	
	print "-" * 79
	
	a = test.toUni( "title" )
	print a