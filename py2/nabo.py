#-*- coding:UTF-8 -*-
#===================================================================================================
#
# [     Nabo     ]
# Parser for Naverblog post.
# https://github.com/xky/Nabo
#
# 2014, XKY
# License: LGPL v3
#
#===================================================================================================
import sys; reload(sys); sys.setdefaultencoding("UTF-8")
import urllib2, urllib, cookielib
import re, json

#===================================================================================================
# class: NaboError
#===================================================================================================
class NaboError(Exception):pass

#===================================================================================================
# class: Nabo
# Parser class
#===================================================================================================
class Nabo:
	#===================================================================================================
	# __init__: 생성자
	#===================================================================================================
	def __init__( self, username ):
	#def __init__( self, username, password ):
		# 블로그 데이터 정의
		# 정의 v2
		'''
		# 로그인 시도
		if( (username) && (password) ):
			result = login( username, password )
			if ( result[1] == True ):
				pass
		'''
		# 공용 헤더
		self.header = { "User-Agent" : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)" }
		self.DATA = {
			"naver":{
				"username"	:	username,
				"host"			:	"http://blog.naver.com/"+ username,
				"title"			:	None,
				"body"			:	None,
				"date"			:	None,
				"num"			:	None
			}
		}
	#===================================================================================================
	# [구현중] login: 로그인 데이터 작성
	#===================================================================================================
	def login( self, username, password, redirect_url="" ):
		# 쿠키
		cookie = cookielib.CookieJar()
		
		# POST로 전송될 값들의 정의
		login_form = urllib.urlencode({
			"id":username,
			"pw":password,
			"enctp":1,
			"locale":"ko_KR",
			"url":redirect_url
		})
		
		
		session = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookie) )
		
		# 로그인 요청
		session.open("https://nid.naver.com/nidlogin.login", session, headers = self.header )
		
		# 미구현이므로 False
		return False
	#===================================================================================================
	# open: 리퀘스트 + 파싱 + 반영
	#===================================================================================================
	def open(self, url):
		#userid = self.DATA["USER_ID"]
		userid = self.DATA["naver"]["username"]
		
		# 입력한 url 끝에 슬래쉬 지우기
		if url[-1] == "/":
			url = url[:-1]
		
		# blog.naver.com 패턴일 때
		rep = re.match( "http://blog.naver.com/"+userid+"/(\d+)", url )
		if rep != None:
			self.DATA["naver"]["num"] = rep.group(1)
		
		# blog.me 패턴일 때
		elif rep == None:
			rep = re.search( "http://"+userid+".blog.me/(\d+)", url )
			if  rep != None:
				self.DATA["naver"]["num"] = rep.group(1)
			else:
				raise NaboError, "Can't found post id"
		
		# 리퀘스트용 헤더 작성
		req = urllib2.Request(
			url = "http://blog.naver.com/PostView.nhn?blogId="+ userid +"&logNo="+ self.DATA["naver"]["num"] + "&redirect=Dlog&widgetTypeCall=true",
			headers = self.header
		)
		html = urllib2.urlopen( req ).read()

		#
		# 날짜, 제목 파싱 시작
		#
		obj = None
		data_ids = ( "title", "date" ) # 접근용 튜플
		data_pattens = [ '<span[\s]class="pcol1[\s]itemSubjectBoldfont">(.+)</span>', '_postAddDate\">(.+)<' ]
		for x in range(0, 2):									# =[0, 1]
			obj = re.search( data_pattens[x], html )			# 검색
			if( obj == None ):									# 발견할 수 없다면 False를 리턴
				self.DATA["naver"][ data_ids[x] ] = False
			else:												# 찾았다면 반영하기
				self.DATA["naver"][ data_ids[x] ] = obj.group(1)
		
		#
		# 본문 파싱 시작
		#
		html = html.replace("\n", "").replace("\t", "") # 처리하기 쉽게 개행, 2칸 여백들 지우기
		body_head = re.search( "<div[\s]id=\"post-view\d+\"\sclass=\".+\">", html ).group() # 인덱스 시작점 파싱
		body_head = html.index(body_head)
		body_foot = "<div class=\"post_footer_contents\">" 									# 인덱스 끝점 파싱
		body_foot = html.index(body_foot)
		self.DATA["naver"]["body"] = html[body_head:body_foot]									# 찾은 내용을 반영
	#===================================================================================================
	# getIMGs: 본문의 이미지 주소를 파싱
	#===================================================================================================
	def getIMGs(self):
		if self.DATA["body"] == None:
			raise NaboError, "You must parsing first."
		else:
			lobj = re.search( "(http://[\w\s\d./_-]+.type=w2)", self.DATA["naver"]["POST_BODY"] )
			
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
		if( self.DATA["naver"][dict_key] == None ):
			return False
		else:
			f = None
			if( filename == ".txt" ):
				f = open( dict_key + filename, "w" )
			else:
				f = open( filename, "w" )
			f.write( self.DATA["naver"][dict_key] )
			f.close()
			return True
	#===================================================================================================
	# getJson: self.DATA의 내용을 Josn형식의 문자열로 리턴
	#===================================================================================================
	def getJson(self):
		result = json.dumps( self.DATA )
		return result
	#===================================================================================================
	# callRequest: 직접 리퀘스트 + 호출
	#===================================================================================================
	def callRequest(self):
		if (self.DATA["naver"]["username"]==None) or (self.DATA["naver"]["num"]==None):
			raise NaboError
		else:
			req = urllib2.Request( "http://blog.naver.com/PostView.nhn?blogId="+ userid +"&logNo="+ self.DATA["naver"]["POST_ID"] + "&redirect=Dlog&widgetTypeCall=true" )
			html = urllib2.urlopen( req ).read()
			return html
	#===================================================================================================
	# showType: 유니코드 에러를 위한 디버깅용 함수.
	#===================================================================================================
	def showType( self, data_key="title" ):
		print type( self.DATA["naver"][data_key] )
	#===================================================================================================
	# toUni: 유니코드 에러를 위한 디버깅용 함수.
	#===================================================================================================
	def toUni( self, data_key="title" ):
		return self.DATA["naver"][data_key].encode('utf-8')






#===================================================================================================
# class: conv
# HTML processor
#===================================================================================================
class Conv:
	#===================================================================================================
	# __init__: 생성자
	#===================================================================================================
	def __init__(self, objNabo):
		self.obj = objNabo
		self.body = objNabo.DATA["naver"]["body"]
	#===================================================================================================
	# autoclean: 기본 정리
	#===================================================================================================
	def autoclean(self):
		# <p> 여는 태그 제거
		self.body = self.body.replace("<p>", "") 
		#self.body = re.sub("(<p .+>).+</p>", "", self.body)
		
		# 문제가 되는 태그 검색&제거( <p>, <span> 포함 )
		m = re.search( "(<p .+>).+</p>", self.body )
		for s in m:
			self.body = self.body.replace( s , "" )

		# 닫는 태그 제거
		self.body = self.body.replace( "</p>", "" )
		self.body = self.body.replace( "</span>", "" )
		self.body = self.body.replace("&nbsp;", "<br>")

	#===================================================================================================
	# commit: 적용
	#===================================================================================================
	def commit(self):
		self.obj.DATA["naver"]["body"] = self.body
		return self.obj