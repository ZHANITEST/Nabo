# -*- coding:UTF-8 -*-
#===================================================================================================
#
# Nabo
# Naver blog Parser
#
# 2014, XKY
# License: LGPL v3
#
#===================================================================================================
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import urllib2
import re

#===================================================================================================
# class: NaboError
#===================================================================================================
class NaboError(Exception):pass

#===================================================================================================
# class: nabo
#===================================================================================================
class Nabo:
	def __init__(self, username):
		# 블로그 데이터 정의
		self.DATA = {
			"USER_ID"		:	username,
			"BLOG_URL"		:	"http://blog.naver.com/"+ username,
			"POST_TITLE"	: None, 
			"POST_DATE"		: None, 
			"POST_BODY"		: None,
			"POST_ID"		: None
		}
	#===================================================================================================
	# open: 리퀘스트 + 파싱 + 반영
	#===================================================================================================
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
		
		# 프레임 주소 파싱 / 제거 됨
		#self.DATA["POST_FRAMEURL"] = "http://blog.naver.com/PostView.nhn?blogId="+ userid +"&logNo="+ self.DATA["POST_ID"] + "&redirect=Dlog&widgetTypeCall=true"
		
		# HTML 리퀘스트 요청
		req = urllib2.Request( "http://blog.naver.com/PostView.nhn?blogId="+ userid +"&logNo="+ self.DATA["POST_ID"] + "&redirect=Dlog&widgetTypeCall=true" )
		html = urllib2.urlopen( req ).read()
		
		# 날짜 읽기
		# r1: (\d{4}/\d{2}/\d{2} .+:\d\d)
		# r2: _postAddDate">(.+)<
		
		# 제목 읽기
		# r1: "<title>(.+):"
		# r2: <span[\s]class="pcol1[\s]itemSubjectBoldfont">(.+)</span>
		
		#
		# 날짜, 제목 파싱 시작
		#
		obj = None
		data_ids = [ "POST_TITLE", "POST_DATE" ]
		data_pattens = [ '<span[\s]class="pcol1[\s]itemSubjectBoldfont">(.+)</span>', '_postAddDate\">(.+)<' ]
		for x in range(0, 2):									# =[0, 1]
			obj = re.search( data_pattens[x], html )			# 검색
			if( obj == None ):									# 발견할 수 없다면 False를 리턴
				self.DATA[ data_ids[x] ] = False
			else:												# 찾았다면 반영하기
				self.DATA[ data_ids[x] ] = obj.group(1)
		
		#
		# 본문 파싱 시작
		#
		# (예전에 쓰던 본문 파싱용 정규식들)
		#r1: post-view[\d]+" .+">[\s]+(<p>.+)</div>
		#r2: post-view[\d]+\" .+\">[\s]+(.+)
		html = html.replace("\n", "").replace("\t", "") # 처리하기 쉽게 개행, 2칸 여백들 지우기
		body_head = re.search( "<div[\s]id=\"post-view\d+\"\sclass=\".+\">", html ).group() # 인덱스 시작점 파싱
		body_head = html.index(body_head)
		body_foot = "<div class=\"post_footer_contents\">" 									# 인덱스 끝점 파싱
		body_foot = html.index(body_foot)
		self.DATA["POST_BODY"] = html[body_head:body_foot]									# 찾은 내용을 반영
	#===================================================================================================
	# getIMGs: 본문의 이미지 주소를 파싱
	#===================================================================================================
	def getIMGs(self):
		if self.DATA["POST_BODY"] == None:
			raise NaboError, "You must parsing first."
		else:
			lobj = re.search( "(http://[\w\s\d./_-]+.type=w2)", self.DATA["POST_BODY"] )
			
			# 이미지 주소가 없다면
			if( bool(lobj) == False ):
				return None
			else:
				lobj = lobj.groups()
				return lobj
	#===================================================================================================
	# getFile: self.DATA의 내용을 파일로 쓰기
	#===================================================================================================
	def getFile(self, dict_key, filename = ".txt"):
		if( self.DATA[dict_key] == None ):
			return False
		else:
			f = None
			if( filename == ".txt" ):
				f = open( dict_key + filename, "w" )
			else:
				f = open( filename, "w" )
			f.write( self.DATA[dict_key] )
			f.close()
			return True
	#===================================================================================================
	# callRequest: 직접 리퀘스트 + 호출
	#===================================================================================================
	def callRequest(self):
		if (self.DATA["USER_ID"]==None) or (self.DATA["POST_ID"]==None):
			raise NaboError
		else:
			req = urllib2.Request( "http://blog.naver.com/PostView.nhn?blogId="+ userid +"&logNo="+ self.DATA["POST_ID"] + "&redirect=Dlog&widgetTypeCall=true" )
			html = urllib2.urlopen( req ).read()
			return html