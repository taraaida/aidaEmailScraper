import os 
import re
from bs4 import BeautifulSoup
import sys


def scrapeEmailsFromSinglePage(linkToScrape): 

	#create progress dots
	print('.'),
	sys.stdout.flush()
	
	#find current domain in case hrefs linked to straight directories (e.g. href="/apple.html")
	currentDomain = linkToScrape.replace("http://","").replace("www.","").replace("https://","")


	if len(currentDomain.split("/"))>0: 
		currentDomain = currentDomain.split("/")[0]
	if "http://" in linkToScrape:
		currentDomain = "http://"+currentDomain
	elif "https://" in linkToScrape:
		currentDomain = "https://"+currentDomain
	else: 
		currentDomain = "http://"+currentDomain

	#get the html from the page
	os.system("./phantomjs myScraper.js "+linkToScrape)
	currentPage = open("tempPage.txt",'r')
	currentPageString = currentPage.read()

	#match all emails 
	emailPattern = re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
	emailsOnPage = emailPattern.findall(currentPageString)

	#add emails to array if not already found
	for email in emailsOnPage: 
		if email not in allEmails: 
			allEmails.append(email)

	#find all links on page using BeautifulSoup object
	soupObjectOfCurrentPage = BeautifulSoup(currentPageString, "html.parser")
	allLinks = soupObjectOfCurrentPage.find_all('a',href=True)


	#iterate through each link and figure out the proper way to format it to scrape it for more emails
	#format it properly, then add the link to the list of scraped sites and pass the link to the scrapeEmails function
	for link in allLinks: 

		#try to filter down to hyperlinks
		if "mailto" not in link and "javascript:" not in link and "#" not in link: 

			#if http in the link, then nothing to append to scrape the link
			if "http" in link['href']: 
				#check that site is still within submitted domain
				if topLevelDomainToCheck in link['href']:
					#check that site has not been scraped already
					if link['href'] not in linksAlreadyChecked:
						#uncomment the following if statement to scrape technology.jana.com and blog.jana.com
						if "blog" not in link['href'] and "technology" not in link['href']:
							linksAlreadyChecked.append(link['href'])
							scrapeEmailsFromSinglePage(link['href'])

			#if it's a directory (e.g. href="/contact")
			elif link['href'][0]=="/": 
				#check that site has not been scraped already
				if currentDomain+link['href'] not in linksAlreadyChecked:
					#uncomment the following if statement to scrape technology.jana.com and blog.jana.com
					if "blog" not in linkToScrape+link['href'] and "technology" not in linkToScrape+link['href']: 
						linksAlreadyChecked.append(currentDomain+link['href'])
						scrapeEmailsFromSinglePage(currentDomain+link['href'])
			#if it's something else (e.g. href="contact.php", href="../contact.php")	
			else:
				#uncomment the following if statement to scrape technology.jana.com and blog.jana.com
				if "blog" not in linkToScrape+link['href'] and "technology" not in linkToScrape+link['href']: 
					#if they are going up a directory level - I don't catch this in a more general fashion
					if "../" in link['href'][:3]:
						currentDomainWithHttpRemoved = linkToScrape.replace("http://","").replace("www.","").replace("https://","")
						for i in range(0,len(currentDomainWithHttpRemoved.split("/"))-1):
							formattedLinkToScrape = formattedLinkToScrape+currentDomainWithHttpRemoved.split("/")[i]+"/"

						#re-append http/https
						if "https" in linkToScrape:
							formattedLinkToScrape = "https://"+formattedLinkToScrape
						else: 
							formattedLinkToScrape = "http://"+formattedLinkToScrape
	 			
				#assuming it is the case href="contact.php"
				if currentDomain+"/"+link['href'] not in linksAlreadyChecked:
					#uncomment the following if statement to scrape technology.jana.com and blog.jana.com
					if "blog" not in linkToScrape+link['href'] and "technology" not in linkToScrape+link['href']: 
						linksAlreadyChecked.append(currentDomain+"/"+link['href'])
						scrapeEmailsFromSinglePage(currentDomain+"/"+link['href'])

#end of scrapeEmailsFromSinglePage function - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #





#pass in domain
domain = sys.argv[1] 

if "http" not in domain: 
	print "Please pass the full link including the http/https (e.g. http://www.jana.com)"
else: 
	#find topLevelDomain and use this to ensure we only scrape links on this domain/subdomains
	topLevelDomainToCheck = domain.replace("http://","").replace("www.","").replace("https://","")
	if len(topLevelDomainToCheck.split("/"))>0: 
		topLevelDomainToCheck = topLevelDomainToCheck.split("/")[0]

	#collect emails in allEmails array, keep running list of pages we have already checked
	allEmails = []
	linksAlreadyChecked = []

	#start the recursive scraper on the first domain passed in
	
	#start the scraping on the first link passed in
	print "Scraping emails in progress:",
	scrapeEmailsFromSinglePage(domain)

	#print all the emails
	print "\n\nAll Emails Found:"
	
	for email in allEmails:
		print email
	
	print "\n"

