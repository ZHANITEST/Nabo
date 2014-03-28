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
username = raw_input("id: ")

# post url
posturl = raw_input("post url: ")

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