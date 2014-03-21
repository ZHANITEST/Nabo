#-*- coding:UTF-8 -*-
#===================================================================================================
#
# demo/writer.py
# parsing post, write json file.
#
#===================================================================================================
import os
os.chdir("..")
import nabo


# username
username = "despair4045"

# post url
posturl = "http://despair4045.blog.me/90192573172"

# write body file?
b_body = True;

# download images?
b_imgs = True;
downloadpath = "/imgs"






# start
if __name__ == "__main__":
	# open & get response
	post = nabo.Nabo( username )
	post.open( posturl )

	postid = post.DATA["POST_ID"]
	
	if( b_body == True ):
		# file object
		f = ( lambda fname,body:open(fname,"w").write(body) )
		
		# make directory	
		if( os.path.isdir(postid) == False ) :
			os.mkdir( postid )
		
		f( postid+"/title.txt", post.DATA["POST_TITLE"] )
		f( postid+"/body.txt", post.DATA["POST_BODY"] )
	
	if( b_imgs == True ):
		urls = post.getIMGs()
		print urls