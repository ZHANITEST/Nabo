#===================================================================================================
#
# demo/writer.py
# parsing post, write json file.
#
#===================================================================================================
import os, json
os.chdir("..")
import nabo


# username
username = ""

# post url
posturl = ""

# write body file?
b_body = True;

# download images?
b_imgs = True;
downloadpath = "./imgs"



post_obj = {
	"title":None,
	"body":None,
	"date":None
}



# start
if __name__ == "__main__":
	# open & get response
	post = nabo.Nabo( username )
	post.open( posturl )

	if( b_body == True ):
		f = open( post.DATA["POST_ID"]+".json", "w" )
		f.write( post.DATA["POST_BODY"] )
		f.close()
	
	if( b_imgs == True ):
		if( os.isdir(downloadpath) != True ):
			os.mkdir( downloadpath )
		
		imgs = post.getIMGs()
		
		for n in range( 0, len(imgs) ):
			try: