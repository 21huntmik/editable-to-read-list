import base64
import os

class SessionStore:

	def __init__(self):
		self.sessions = {}

	def generateSessionId(self):
		rnum = os.urandom(32)
		rstring = base64.b64encode(rnum).decode("utf-8")
		return rstring

	def getSessionData(self, sessionId):
		#check to see if the sessionId exists
		#if your server restarts, then id's are replaced
		if sessionId in self.sessions:
			return self.sessions[sessionId]
		else:
			return None

	def createSession(self):
		#put a new dictionary into the dictionary
		#create a session id
		# {{id{info}}, more}
		sessionId = self.generateSessionId()
		self.sessions[sessionId] = {}
		return sessionId