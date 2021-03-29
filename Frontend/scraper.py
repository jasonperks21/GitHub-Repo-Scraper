from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from github import Github
import urllib.parse

def scrape_github(search_term, num_pages=1):
	my_url = 'https://github.com/search?q='+search_term.strip().replace(" ", "+")

	# opening up connection, grabbing the page
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	# Grabs each repo
	repo_containers = page_soup.findAll("div", {"class":"mt-n1"})

	# Create list of scraped info
	scraped_list = []
	# Scraping
	for container in repo_containers:
		# Get name
		repo_name = container.a.text
		# Get description
		try:
			description = container.p.text.strip()
		except AttributeError:
			description = None
		# Get tags
		try:
			tag_containers = container.findAll("a",{"class":"topic-tag topic-tag-link f6 px-2 mx-0"})
			tags = []
			for tcontainer in tag_containers:
				tags.append(tcontainer.text.strip())
			if len(tags) == 0:
				tags = None
		except AttributeError:
			tags = None
		# Get stars
		try:
			num_stars = container.find("a", href=re.compile("stargazers")).text.strip()
		except AttributeError:
			num_stars = None
		# Get language
		try:
			language = container.find("span", itemprop=re.compile("programmingLanguage")).text
		except AttributeError:
			language = None
		# Get license
		try:
			license = container.find(text=re.compile("license")).strip()
		except AttributeError:
			license = None
		# Get last_updated
		try:
			last_updated = container.find("relative-time")["datetime"]
		except AttributeError:
			last_updated = None
		# Get num_issues
		try:
			num_issues_string = container.find("a", href=re.compile("issues")).text.strip()
			num_issues = num_issues_string[0:num_issues_string.find(" ")]
		except AttributeError:
			num_issues = None
		# Add to dictionary
		repo_dict = {
		"name":	repo_name,
		"description": description,
		"tags": tags,
		"num_stars": num_stars,
		"language": language,
		"license": license,
		"last_updated": last_updated,
		"num_issues": num_issues
		}
		# Add to list
		scraped_list.append(repo_dict)
	return scraped_list

#def github_api(search_term, num_pages=1):
ACCESS_TOKEN = 'f4fbd715766cde1dc4af0a75fd21eac83d3006c6'
g = Github(ACCESS_TOKEN)
keywords = input('Enter search term: ')
#keywords = [keyword.strip() for keyword in keywords.split(',')]
#query = '+'.join(keywords) + '+in:readme+in:description'
query = keywords.strip().replace(' ', '+')
result = g.search_repositories(query)
print(f'Found {result.totalCount} repo(s)')

print(query)
for repo in result:
	print(repo.name)