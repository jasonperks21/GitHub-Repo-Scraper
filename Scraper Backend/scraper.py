from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#def scrape_github(search_term, num_pages=1):
	# '''Search_term : str
	# 		The search term for the github repos
	# 	num_pages : int
	# 		The number of pages to scrape
	# 	returns scraped_info : list
	# 		A list of dictionaries containing the info
	# '''
	#search_term = input("Enter search term: ")
my_url = 'https://github.com/search?q=computer+vision'

	# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

	# html parsing
page_soup = soup(page_html, "html.parser")

	# Grabs each repo
repo_containers = page_soup.findAll("div", {"class":"mt-n1"})

	# Scraping
for container in repo_containers:
	repo_name = container.a.text
	description = container.p.text.strip()
	tag_containers = container.findAll("a",{"class":"topic-tag topic-tag-link f6 px-2 mx-0"})
	tags = []
	for tcontainer in tag_containers:
		tags.append(tcontainer.text.strip())
