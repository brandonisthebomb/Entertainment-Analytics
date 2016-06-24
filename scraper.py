from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import pymysql.cursors
import re

BASE_YEAR = "1980"
CURRENT_YEAR = "2016"


# General http address for Box Office Mojo
BOM = "http://www.boxofficemojo.com"

# Iterate through every year
def baseScrapingLoop():

	# Make sure we start off with a blank SQL database CHANGE THIS LATER
	emptyTable()

	# Loop through each year starting from the first year (1980) to the current year, set above
	for year in range(int(BASE_YEAR), int(CURRENT_YEAR) + 1):

		# List of the (year) top grossing films, which will be parsed for the URLs
		url = "http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=1980&p=.htm"

		# Now, when the “with” statement is executed, Python evaluates the expression, 
		# calls the __enter__ method on the resulting value (which is called a 
		# “context guard”), and assigns whatever __enter__ returns to the variable 
		# given by as. Python will then execute the code body, and no matter what 
		# happens in that code, call the guard object’s __exit__ method.
		with urllib.request.urlopen(url) as response:

			# gets the raw html code from the URL
			html = response.read()
			#print (html)

		# Use Beautiful Soup to organize the html into a more readable way
		soup = BeautifulSoup(html)
		organized = soup.prettify() 	
		#print(organized)	

		scrapeMoviesFromYear(url)


# Iterate through each of the individual pages under the year, 0-100 101-200 etc.
def scrapeMoviesFromYear(url):

	# Keep track of the current page
	currentPage = 0

	# Want to find every movie url for the given year
	while True:
		currentPage += 1
		url = url.replace("?page=" + str(currentPage - 1), "?page=" + str(currentPage))
		#print (url)

		with urllib.request.urlopen(url) as response:	
			html = response.read()

		# base case, if we've reached the end of the pages then stop the loop
		if "There was an error processing this request" in str(html):
			break
		
		# else we do this:
		soup = BeautifulSoup(html, "html.parser")

		# Search the soup for the <a tag that precedes all href links
		for link in soup.find_all('a'):
			name = str(link.get('href'))

			# if movies is in the link then it's the one we're looking for,
			# not ref = ft is a special case that we don't want to be in the list
			if 'movies' in name and 'ref=ft' not in name: 
				url = bom + name
				scrapeDataFromMovie(url)


def scrapeDataFromMovie(url):

	with urllib.request.urlopen(url) as response:

		# gets the raw html code from the URL
		html = response.read()
		#print (html)

		# Use Beautiful Soup to organize the html into a more readable way
		soup = BeautifulSoup(html, 'html.parser')
		#print (soup.encode("utf-8"))

		readStaticData(soup.find_all('b'))


def readStaticData(info):
	# 1 = title

	title = info[1].getText()
	print ("Title: " + title)

	# 2 = domestic total as of some date
	# Comes in this format: $141,319,928, needs to be made an int

	total = int(re.sub('[$,]', '', info[2].getText()))
	print ("Domestic Total Gross: " + str(total))

	# 3 = distributor

	distributor = info[3].getText()
	print ("Distributor: " + distributor)

	# 4 = release date
	# Format Release Date: November 12, 2008 needs to be in yyyy-mm-dd

	release = re.sub("[,]", "", info[4].getText())
	release = datetime.strptime(release, "%B %d %Y")
	release = release.strftime("%Y-%m-%d")
	print ("Release Date: " + release)

	# 5 = Genre

	genre = info[5].getText()
	print ("Genre: " + genre)

	# 6 = Runtime

	runtime = info[6].getText()
	print ("Runtime: " + runtime)

	# 7 = Rating

	rating = info[7].getText()
	print ("Rating: " + rating) 

	# 8 = Production Budget

	budget = info[8].getText()
	print ("Production Budget: " + budget)

	connection = pymysql.connect(host = 'localhost', user = 'root',
		password = 'pass', db = 'test', charset = 'utf8mb4',
		cursorclass = pymysql.cursors.DictCursor) 

	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO" `movies` ()


def putURLsIntoDatabase(myList):

	connection = pymysql.connect(host = 'localhost', user = 'root',
		password = 'pass', db = 'test', charset = 'utf8mb4',
		cursorclass = pymysql.cursors.DictCursor) 

	try:
		with connection.cursor() as cursor:
			# Clears the table
			sql = "TRUNCATE `movies`"
			cursor.execute(sql)

			#Ready to reinsert values into the table
			sql = "INSERT INTO `movies` (`title`) VALUES (%s)"
			for movie in myList:
				cursor.execute(sql, movie)

		connection.commit()

		# Accessing data with a query: 
		# with connection.cursor() as cursor:
		# 	sql = "SELECT * FROM `movies`"
		# 	cursor.execute(sql)
		# 	result = cursor.fetchall()
		# 	print(result[1]['id'])
		# 	print(result[1]['title'])

	# Close the connection
	finally:
		connection.close()


def emptyTable():
	connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'test', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	try:
		with connection.cursor() as cursor:
			# Clears the table
			sql = "TRUNCATE `movies`"
			cursor.execute(sql)
		connection.commit()
	finally:
		connection.close()





baseUrlLoop()
