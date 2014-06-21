#-*- coding:UTF-8 -*-
#===================================================================================================
#
# conv_test.py (for Nabo)
# 2014, XKY
# License: LGPL v3
#
#===================================================================================================
from nabo import Nabo #Parser
from nabo import Conv #HTML code processor
from pprint import pprint

if __name__ == "__main__":
	# Target: http://blogpeople.blog.me/150181071013
	test = Nabo("blogpeople")
	test.open("http://blogpeople.blog.me/150181071013")
	
	post = Conv( test )
	post.autoclean()
	post = post.commit()
	
	pprint( test.DATA["naver"]["body"] )
	#pprint( post.DATA["naver"]["body"] )