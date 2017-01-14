from urllib import FancyURLopener
import json
from bs4 import SoupStrainer, BeautifulSoup


'''Class to provide custom user header to prevent blocking by Google\'s bot watchers. '''
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
openurl = MyOpener().open




'''Create custom object for papers received '''
class Papers:
	#Constructor
	def __init__(self, paperId, title, authors, noOfCitations):
		self.paperId = paperId
		self.title = title
		self.authors = authors
		self.noOfCitations = noOfCitations
	#Pretty Printer
	def __repr__(self):
		return '"id": "%s", title": "%s", "authors": "%s", "num_citations": "%s"' % (self.paperId, self.title, self.authors, self.noOfCitations)

url = str(raw_input("Enter URL to scrape:"))





'''Get div containing results'''
page = BeautifulSoup(openurl(url).read()
,"lxml", parse_only=SoupStrainer('div', id='gs_ccl_results'))


data = []
paper_id = 66
for titles in page.findAll('div', {'class': 'gs_ri'}):
	articles = titles.findAll('h3')
	for article_titles in articles:
			c_article_title = article_titles.text.encode('ascii','ignore').strip()
	authors = titles.findAll('div', {'class': 'gs_a'})
	for paper_authors in authors:
		c_paper_authors = paper_authors.text.encode('ascii','ignore').strip()
	num_citations = titles.findAll('div', {'class': 'gs_fl'}, 'a')
	for citations in num_citations:
		c_citations = citations.contents[0].text.encode('utf-8').strip()
		if c_citations == "Related articles":
			c_citations = ""
	data.append(Papers(str(paper_id), c_article_title, c_paper_authors, c_citations))
	paper_id += 1

json_data = json.dumps(data, indent=4, default=lambda o: o.__dict__)

with open('research_paper_data.json', 'a') as f:
     f.write(url + "\n")
     f.write(json_data)
		


