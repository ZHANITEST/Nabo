#-*- coding:UTF-8 -*-
#===================================================================================================
#
# json_test.py (for Nabo)
# 2014, XKY
# License: LGPL v3
#
#===================================================================================================
from nabo import Nabo

if __name__ == "__main__":
	# Target: http://blogpeople.blog.me/150181071013
	test = Nabo("blogpeople")
	test.open("http://blogpeople.blog.me/150181071013")
	
	json_string = test.getJson()
	print json_string