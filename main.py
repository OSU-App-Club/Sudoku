#Copyright 2013 by Ryley Herrington
import datetime
import urllib
import wsgiref.handlers
import webapp2

from datetime import datetime, timedelta
from google.appengine.ext import db

#Sample of puzzle format on input
#038796215659132478271458693845219367713564829926873154194325786362987541587641932

# Database model for single puzzle
# 	Used to persist puzzles across inputs
class Sudoku(db.Model):
	author = db.StringProperty()
	puzzle = db.StringProperty(multiline=True)
	solved_puzzle = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)

def row(i):
	
	## the input is one long string so when you floor divide it
	## and multiply it you get the starting index of the row
	r=(i//9)*9
	return [ r, r+1, r+2, r+3, r+4, r+5, r+6, r+7, r+8 ]

def col(i):
	c=(i%9)
	## hey! adding by 9 each times gives you the column values
	return [c, c+9, c+18, c+27, c+36, c+45, c+54, c+63, c+72 ]

def square(i):
	s=(i//27)*27 + (((i%9)//3)*3)
	return [s, s+1, s+2, s+9, s+10, s+11, s+18, s+19, s+20 ]


# Abstract class for solving sudoku puzzles
# 	All solve proccessing happens in this class
class Board:
	possible = {}
	value	 = {}

def setUniqueCells(b, cells):
	found_change = False
	all_possibles = ""
	for c in cells:
		if int(b.value[c]) == 0:
			all_possibles = all_possibles + b.possible[c]
	for v in "123456789":
		if int(all_possibles.count(v)) == 1:
			for c in cells:
				if int(b.possible[c].count(v) == 1) and int(b.value[c]) == 0:
					setCell(b, c, v)
					found_change = True
	return found_change

def setUniqueInBoard(b):
	change = True
	while change == True:
		change = False
		for k in range(0, 81, 9):
			if setUniqueCells(b, row(k)):
				change = True
		for k in range (9):
			if setUniqueCells(b, col(k)):
				change = True
		for k in range(0, 81,27):
			for j in range(k, k+9, 3):
				if setUniqueCells(b, square(j)):
					change = True

def markCell(b, position, val):
	if int(b.value[position]) == 0:
		p = b.possible[position]
		i = p.find(val)
		if i == 0:
			p = p[1:]
		elif i != -1:
			p = p[:i] + p[i+1:]
		b.possible[position] = p
		if int(b.value[position]) == 0 and int(len(p)) == 1:
			setCell(b, position, p[0])
	

def setCell(b, position, newVal):
	if int(b.value[position]) == 0:
		b.value[position] = newVal
		if newVal != '0':
			b.possible[position] = newVal
			for x in row(position):
				if (x != position):
					markCell(b, x, newVal)
			for x in col(position):
				if (x != position):
					markCell(b, x, newVal)
			for x in square(position):
				if (x != position):
					markCell(b, x, newVal)


	for i in range(81):
		b.possible[i] = "123456789"
		b.value[i] = '0'
	position=0
	for val in line:
		if val is not '0':
			setCell(b, position, val)
		position = position + 1
	setUniqueInBoard(b)


def sudokubook_key(sudokubook_name=None):
	return db.Key.from_path('Guestbook', sudokubook_name or 'default_sudokubook')

def prettyPrint(puzzle):
	answer = ''
	for k in range (0, 81, 9):
		answer = answer + puzzle[k+0:k+3] + ' | ' + puzzle[k+3:k+6] + ' | ' + puzzle[k+6:k+9]+'<br/>'
		if k is 18 or k is 45:
			answer =answer + '---- + ---- + ----'+'<br/>'

	answer = answer+'<br/>'
	return answer

# Redirect of / or mainpage
#	Outputs webpage(HTML) with all puzzles and allows web submission
class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.out.write('<html><body>')
		sudokubook_name='cs496'

		sudokus = db.GqlQuery("SELECT * "
							"FROM Sudoku "
							"ORDER BY date DESC LIMIT 10")

		for sudoku in sudokus:
			if sudoku.author == None:
				sudoku.author = "Anonymous"
			self.response.out.write(sudoku.author+" wanted to solve this puzzle:</br>")
			self.response.out.write(prettyPrint(sudoku.puzzle))

		self.response.out.write("""
			<form action="/?%s" method="post">
				<div><textarea name="puzzle" rows="3" cols="60"></textarea></div>
				<div><input type="submit" value="Enter sudoku"></div>
			</form>
		</body>
		</html>"""%(urllib.urlencode({'sudokubook_name': sudokubook_name})))

	def post(self):
		sudokubook_name = 'cs496'
		sudoku = Sudoku(parent=sudokubook_key(sudokubook_name))
		sudoku.puzzle = self.request.get('puzzle')
		sudoku.put()

		self.redirect('/')

# Redirect of /solve
# 	Handles input of puzzle and requests to get all stored & solved puzzles
class SolveHandler(webapp2.RequestHandler):
	
	# HTTP GET
	#  All stored sudoku puzzles; solve if haven't been solve yet
	#  Return as prettyPrint() solutions in plain text
	def get(self):
		sudokus = db.GqlQuery("SELECT * "
							"FROM Sudoku "
							"WHERE ANCESTOR IS :1 "
							"ORDER BY date DESC LIMIT 10",
							 sudokubook_key('cs496'))

		for sudoku in sudokus:
			if sudoku.solved_puzzle == None:
				b = Board()
				partialSolve(b, sudoku.puzzle)
				fullAnswer = ''
				for k in range (0, 81):
					fullAnswer = fullAnswer + b.value[k]
				sudoku.solved_puzzle = fullAnswer
				sudoku.put()
	
			self.response.out.write('<p>%s<p>'%prettyPrint(sudoku.solved_puzzle))
	
	# HTTP POST
	# Params
	#	puzzle: input puzzle as single line
	#	author: name attributed to inputed puzzle (Default: Anonymous)
	def post(self):
		sudokubook_name = 'cs496'
		sudoku = Sudoku(parent=sudokubook_key(sudokubook_name))

		sudoku.puzzle = self.request.get('puzzle')
		sudoku.author = "Anonymous"
		sudoku.author = self.request.get('author')
		sudoku.solved_puzzle = None
		sudoku.put()

		self.redirect('/view?author=' + sudoku.author)

# Redirect of /view
#	Used by both app to return plain text of puzzles 
class ViewHandler(webapp2.RequestHandler):
	
	# HTTP GET
	#	Query params:
	#		author: used to search for puzzles
	#	Searches database for all puzzles of given "author"; solves if needbe
	#	Returns plain text solutions with line formatting
	def get(self):
		author = "Anonymous"
		author = self.request.get('author')
		sudoku = db.GqlQuery("SELECT * "
							 "FROM Sudoku "  
							 "WHERE author =:1 LIMIT 1 ", author)  
		for s in sudoku:
			if s.solved_puzzle == None:
				b = Board()
				partialSolve(b, s.puzzle)
				fullAnswer = ''
				for k in range (0, 81):
					fullAnswer = fullAnswer + b.value[k]
				s.solved_puzzle = fullAnswer
				s.put()	

			puzzle = ''
			puzzle = s.solved_puzzle	

		response = ''
		for k in range (0, 81, 9):
			response = response + puzzle[k+0:k+3] + ' | ' + puzzle[k+3:k+6] + ' | ' + puzzle[k+6:k+9]+'\n'
			if k is 18 or k is 45:
				response =response + '---- + ---- + ----\n'
		self.response.out.write(response)

# Redirect of /cron
#	This handles CRON, or background tasks that run on a time schedule, jobs to periodically solve unsolved puzzles
#	Old puzzles are also deleted in this job in keep db small
#	Demonstrates the CRON functionality in GAE; also see https://github.com/OSU-App-Club/Sudoku/blob/master/cron.yaml
class CronHandler(webapp2.RequestHandler):
	def get(self):
		sudokus = db.GqlQuery("SELECT * "
							  "FROM Sudoku")

		for sudoku in sudokus:
			if sudoku.solved_puzzle == None:
				b = Board()
				partialSolve(b, sudoku.puzzle)
				fullAnswer = ''
				for k in range (0, 81):
					fullAnswer = fullAnswer + b.value[k]
				sudoku.solved_puzzle = fullAnswer
				sudoku.put()	
		
			if sudoku.date < datetime.now() - timedelta(minutes=120):
				sudoku.delete()
# Redirect of /share
# 	Used to share link to puzzels by given author on g+
class ShareHandler(webapp2.RequestHandler):
	def get(self):
		author = ""
		author = self.request.get('author')
		self.response.out.write("https://twitter.com/intent/tweet?text="+author+"%20solved%20a%20puzzle%20on%20GAE")
		#this url doesn't exist, we should probably get a osu gae account to run this on	
		#self.response.out.write("https://plus.google.com/share?url=osu_appclub.appspot.com/view?author="+author)


# Core of GAE app
# This redirects urls to certain request handlers: ie requests to someURL/solve with go to SolverHandler()
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/view', ViewHandler),
	('/solve', SolveHandler),
	('/cron', CronHandler),
	('/share', ShareHandler)
], debug=True)

