from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
from books_db import BooksDB
from passlib.hash import bcrypt
from http import cookies
from session_store import SessionStore
from socketserver import ThreadingMixIn

SESSION_STORE = SessionStore()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

	def end_headers(self):
		self.sendCookie()
		self.send_header("Access-Control-Allow-Origin", self.headers["Origin"]) #-- if you add this... delete all of these headers
		#add access control allow origin because it will help on Thursday
		self.send_header("Access-Control-Allow-Credentials", "true") #is this right??
		BaseHTTPRequestHandler.end_headers(self) #call the actual self.end_headers()

	def readCookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
		else:
			self.cookie = cookies.SimpleCookie()

			#on every request
			#call on all the do____ at the top! self.loadSessionData() -- All of them even do_GEToptions()
			#DON'T FORGET!!
	
	#call on every single response!!!
	def sendCookie(self):
		for morsel in self.cookie.values():
			self.send_header("Set-Cookie", morsel.OutputString())

	def loadSessionData(self):
		self.readCookie()
		if "sessionId" in self.cookie:
			#read the session id
			sessionId = self.cookie["sessionId"].value
			#read the session data from the session id
			sessionData = SESSION_STORE.getSessionData(sessionId)
			#if session data not found for the session id
			if sessionData == None:
				#create a new session and create a new cookie
				sessionId = SESSION_STORE.createSession()
				sessionData = SESSION_STORE.getSessionData(sessionId)
				self.cookie["sessionId"] = sessionId
		#they are new
		else:
			#create a new session and create a new cookie
			sessionId = SESSION_STORE.createSession()
			sessionData = SESSION_STORE.getSessionData(sessionId)
			self.cookie["sessionId"] = sessionId

		self.sessionData = sessionData #sessionData is a dictionary-- all of the other code can access the data if you save it to self.sessionData

	def handleNotFound(self):
		self.send_response(404)
		self.end_headers()
		self.wfile.write(bytes("Not Found", "utf-8"))

	def handle401(self):
		self.send_response(401)
		self.end_headers()
		self.wfile.write(bytes("Unauthorized", "utf-8"))

	def handleGETbooks(self):
		if "userId"  not in self.sessionData: #user not logged in
			self.handle401() #like handleNotFound() but with 401
			return
		print(self.sessionData)
		self.send_response(200)
		self.send_header("Content-Type", "application/json")
		self.end_headers()
		db = BooksDB()
		all_records = db.getAllBooks()
		self.wfile.write(bytes(json.dumps(all_records), "utf-8"))

	def handleGetOneBook(self, member_id):
		if "userId"  not in self.sessionData: #user not logged in
			self.handle401() #like handleNotFound() but with 401
			return
		db = BooksDB()
		one_record = db.getOneBook(member_id)

		if one_record != None:
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()
			self.wfile.write(bytes(json.dumps(one_record), "utf-8"))
		else:
			self.handleNotFound()

	def handleDeleteOneBook(self, member_id):
		if "userId"  not in self.sessionData: #user not logged in
			self.handle401() #like handleNotFound() but with 401
			return
		db = BooksDB()
		one_record = db.getOneBook(member_id)

		if one_record != None:
			db.deleteOneBook(member_id)
			self.send_response(200)
			self.end_headers()

	def handleDeleteSessions(self):
		if "userId" not in self.sessionData:
			self.handle401()
			return
		del self.sessionData["userId"]

	def handleUpdateBook(self, member_id):
		if "userId"  not in self.sessionData: #user not logged in
			self.handle401() #like handleNotFound() but with 401
			return
		db = BooksDB()
		one_record = db.getOneBook(member_id)
		#combine delete and create
		#capture using create 
		length = self.headers["Content-Length"]
		body = self.rfile.read(int(length)).decode("utf-8")
		parsed_body = parse_qs(body)
		book_title = parsed_body['title'][0]
		book_author = parsed_body['author'][0]
		book_date = parsed_body['date'][0]
		book_pages = parsed_body['pages'][0]
		book_genre = parsed_body['genre'][0]
		#update record in db
		if one_record != None:
			db.updateOneBook(member_id, book_title, book_author, book_date, book_pages, book_genre)
			self.send_response(200)
			self.end_headers()


	def handleCREATEbooks(self):
		if "userId"  not in self.sessionData: #user not logged in
			self.handle401() #like handleNotFound() but with 401
			return
		length = self.headers["Content-Length"]
		body = self.rfile.read(int(length)).decode("utf-8")
		parsed_body = parse_qs(body)
		book_title = parsed_body['title'][0]
		book_author = parsed_body['author'][0]
		book_date = parsed_body['date'][0]
		book_pages = parsed_body['pages'][0]
		book_genre = parsed_body['genre'][0]
		db = BooksDB()
		db.insertBook(book_title, book_author, book_date, book_pages, book_genre)
		self.send_response(201)
		self.end_headers()

	def handleGetOneUser(self, email):
		db = BooksDB()
		one_record = db.checkOneUser(email)

		if one_record != None:
			return False
		else:
			return True

	def handleCREATEusers(self):
		length = self.headers["Content-Length"]
		body = self.rfile.read(int(length)).decode("utf-8")
		parsed_body = parse_qs(body)
		email = parsed_body['email'][0]
		password = parsed_body['password'][0]
		first_name = parsed_body['fname'][0]
		last_name = parsed_body['lname'][0]
		password = bcrypt.hash(password)

		no_duplicates = self.handleGetOneUser(email)

		if no_duplicates == True:
			db = BooksDB()
			db.insertUser(email, password, first_name, last_name)
			user = db.checkOneUser(email)
			self.sessionData["userId"] = user["id"]
			self.send_response(201)
			self.end_headers()
		elif no_duplicates == False:
			self.send_response(422)
			self.end_headers()
		else:
			handleNotFound()

	def handleCREATEsessions(self):
		length = self.headers["Content-Length"]
		body = self.rfile.read(int(length)).decode("utf-8")
		parsed_body = parse_qs(body)
		email = parsed_body['email'][0]
		password = parsed_body['password'][0]
		#How to use verify???????

		no_duplicates = self.handleGetOneUser(email)

		if no_duplicates == False:
			password_match = self.verifyPassword(email, password)
			if password_match == True:
				#save the users ID to the sessionData for this client
				#save into self.sessionData
				db = BooksDB()
				user = db.checkOneUser(email)
				self.sessionData["userId"] = user["id"]

				self.send_response(201)
				self.end_headers()
				#respond with 201 + show the loggedinscreen
			else:
				self.send_response(401)
				self.end_headers()
		else:
			self.send_response(401)
			self.end_headers()

	def verifyPassword(self, email, password):
		#read info from db
		#return the password
		db = BooksDB()
		matched = db.verifyOneUser(email)
		match_password = matched['password']
		#check to see if this still works. I changed it from responding with only the password to everything.
		return bcrypt.verify(password, match_password)

	def do_GET(self):
		self.loadSessionData()

		print("The path is:", self.path)

		parts = self.path.split("/")
		collection = parts[1]
		if len(parts) > 2:
			member_id = parts[2]
		else:
			member_id = None

		if collection == "books":
			if member_id != None:
				self.handleGetOneBook(member_id)
			else:
				self.handleGETbooks()
		else:
			self.handleNotFound()

	def do_POST(self):
		self.loadSessionData()
		if self.path == "/books":
			self.handleCREATEbooks()
		elif self.path == "/users":
			self.handleCREATEusers()
		elif self.path == "/sessions":
			self.handleCREATEsessions()
		else:
			self.handleNotFound()
		#POST member

	def do_OPTIONS(self):
		self.loadSessionData()
		#Comment this out so you can see the error and then uncomment and see how it fixes it
		self.send_response(200)
		self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()

	#def do_PUT(self, member_id):


	def do_DELETE(self):
		self.loadSessionData()
		print("The path is:", self.path)

		parts = self.path.split("/")
		collection = parts[1]
		if len(parts) > 2:
			member_id = parts[2]
		else:
			member_id = None

		if collection == "books":
			if member_id != None:
				self.handleDeleteOneBook(member_id)
		elif collection == "sessions":
			self.handleDeleteSessions()
		else:
			self.handleNotFound()

	def do_PUT(self):
		self.loadSessionData() 
		print("The path is:", self.path)

		parts = self.path.split("/")
		collection = parts[1]
		if len(parts) > 2:
			member_id = parts[2]
		else:
			member_id = None

		if collection == "books":
			if member_id != None:
				self.handleUpdateBook(member_id)
		else:
			self.handleNotFound()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

	pass

def run():
	listen = ("127.0.0.1", 8080)
	server = ThreadedHTTPServer(listen, MyHTTPRequestHandler)

	print("Server ready!")
	server.serve_forever()

run()