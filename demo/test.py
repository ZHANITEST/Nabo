#===================================================================================================
#
# test.py (for Nabo)
# 2014, XKY
# License: LGPL v3
#
#===================================================================================================
from nabo import Nabo
from pprint import pprint

if __name__ == "__main__":
	# Target: http://blogpeople.blog.me/150181071013
	test = Nabo("blogpeople")
	test.open("http://blogpeople.blog.me/150181071013")
	
	print "title:", test.DATA["POST_TITLE"]
	print "date :", test.DATA["POST_DATE"]