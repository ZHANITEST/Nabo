#-*- coding:UTF-8 -*-
#===================================================================================================
#
# login_test.py (for Nabo)
# 2014, XKY
# License: LGPL v3
#
#===================================================================================================
from nabo import Nabo #Parser
from nabo import Conv #HTML code processor

if __name__ == "__main__":
	# Target: http://blogpeople.blog.me/150181071013
	id = raw_input( "Your id: ")
	pw = raw_input( "Your pw: ")
	test = Nabo( id )
	test.login( id, pw )