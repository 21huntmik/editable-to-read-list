import sqlite3
#from passlib.hash import bcrypt

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d 

class BooksDB:
	def __init__(self):
		self.connection = sqlite3.connect("books.db")
		self.connection.row_factory = dict_factory
		self.cursor = self.connection.cursor()

	# READ ALL RECORDS FROM THE DATABASE
	def getAllBooks(self):
		self.cursor.execute("SELECT * FROM books")
		books = self.cursor.fetchall()
		return books

	def getOneBook(self, member_id):
		data = [member_id]
		self.cursor.execute("SELECT * FROM books WHERE id = ?", data)
		book = self.cursor.fetchone()
		return book

	def deleteOneBook(self, member_id):
		data = [member_id]
		self.cursor.execute("DELETE FROM books WHERE id = ?", data)
		self.connection.commit()

	def updateOneBook(self, member_id, title, author, date, pages, genre):
		data = [title, author, date, pages, genre, member_id]
		self.cursor.execute("UPDATE books SET title = ?, author = ?, date = ?, pages = ?, genre = ? WHERE id = ?", data)
		self.connection.commit()

	def insertBook(self, title, author, date, pages, genre):
		data = [title, author, date, pages, genre]
		self.cursor.execute("INSERT INTO books (title, author, date, pages, genre) VALUES (?, ?, ?, ?, ?)", data)
		self.connection.commit()

	def insertUser(self, email, password, first_name, last_name):
		#encryptpassword = bcrypt.hash(password)
		data = [email, password, first_name, last_name]
		self.cursor.execute("INSERT INTO users (email, password, fname, lname) VALUES (?, ?, ?, ?)", data)
		self.connection.commit()

	def checkOneUser(self, email):
		data = [email]
		self.cursor.execute("SELECT * FROM users WHERE email = ?", data)
		authentication = self.cursor.fetchone()
		return authentication

	def verifyOneUser(self, email):
		#read the id where the email matches
		data = [email]
		self.cursor.execute("SELECT password FROM users WHERE email = ?", data)
		passwordToCompare = self.cursor.fetchone()
		return passwordToCompare


	#delete a RECORD
	#delete from restaurants where id = ??
	#don't forget to commit


	#update a RECORD
	#update restaurants set name = ?? rating = ?? hours ??
	#don't forget to commit!