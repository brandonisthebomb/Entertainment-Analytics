from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import pymysql.cursors

# List of the 2015 top grossing films, which will be parsed for the URLs
url = "http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=2015&p=.htm"

# General http address for Box Office Mojo
bom = "http://www.boxofficemojo.com"

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

# Return a list of the movie URLs from html soup
def getMovieURLs():

	# Keep track of the current page
	currentPage = 0
#
	# URL that will be edited 
	url = "http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=2015&p=.htm"

	# Create the list
	urlList = []

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
				urlList.append(url) # Add it to the list, maybe should do some sorting here?
				scrapeDataFromMovie(url)


	#print (urlList)
	putURLsIntoDatabase(urlList)

def scrapeDataFromMovie(url):



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





getMovieURLs()
