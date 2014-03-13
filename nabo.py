# -*- coding:UTF-8 -*-
#============================================================
#
# Nabo
# Naver blog Parser
#
# 2014, XKY
# License: LGPL v3
#
#============================================================
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import urllib2
import re

#============================================================
# class: NaboError
#============================================================
class NaboError(Exception):pass

#============================================================
# class: nabo
#============================================================
class Nabo:
	def __init__(self, username):
		# 블로그 데이터 정의
		self.DATA = {
			"USER_ID"	:	username,
			"BLOG_URL"	:	"http://blog.naver.com/"+ username,
			"POST_BODY"	: None 
		}



	def open(self, url):
		userid = self.DATA["USER_ID"]
		
		# 입력한 url 끝에 슬래쉬 지우기
		if url[-1] == "/":
			url = url[:-1]
		
		# blog.naver.com 패턴일 때
		rep = re.match( "http://blog.naver.com/"+userid+"/(\d+)", url )
		if rep != None:
			self.DATA["POST_ID"] = rep.group(1)
		
		# blog.me 패턴일 때
		elif rep == None:
			rep = re.search( "http://"+userid+".blog.me/(\d+)", url )
			if  rep != None:
				self.DATA["POST_ID"] = rep.group(1)
			else:
				raise NaboError, "Can't found post id"
		
		self.DATA["POST_FRAMEURL"] = "http://blog.naver.com/PostView.nhn?blogId="+ userid +"&logNo="+ self.DATA["POST_ID"] + "&redirect=Dlog&widgetTypeCall=true"
		
		# HTML 리퀘스트 요청
		req = urllib2.Request( self.DATA["POST_FRAMEURL"] )
		html = urllib2.urlopen( req ).read()
		
		# 패턴 람다식
		search = ( lambda x,y : re.search(x, y).group(1) )


		
		# 날짜 읽기
		#\d{4}/\d{2}/\d{2} .+:\d\d
		self.DATA["POST_DATE"] = search( "(\d{4}/\d{2}/\d{2} .+:\d\d)", html)
		
		# 제목 읽기
		#self.DATA["POST_TITLE"] = re.search( "<title>(.+):", html ).group(1)
		self.DATA["POST_TITLE"] = search( "<title>(.+):", html )
		
		#본문 읽기
		# r0: post-view[\d]+" .+">[\s]+(<p>.+)</div>
		# r1: post-view[\d]+\" .+\">[\s]+(.+)</div>
		self.DATA["POST_BODY"] = search( "post-view[\d]+\" .+\">[\s]+(.+)</div>", html )
		
	
	def getIMGs(self):
		lobj = re.search( "(http://[\w\s\d./_-]+.type=w2)", self.DATA["POST_BODY"] ).groups()
		return lobj