import os 
import re
from bs4 import BeautifulSoup
import sys


def scrapeEmailsFromSinglePage(linkToScrape): 

	print linkToScrape
	
	print "- - - - - - - - - - - - - -- - - - -"
	
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

	#find all links on page 
	soupObjectOfCurrentPage = BeautifulSoup(currentPageString)
	allLinks = soupObjectOfCurrentPage.find_all('a',href=True)


	#iterate through each link and figure out the proper way to format the link to scrape it
	for link in allLinks: 
		if "http" in link['href']: 
			if topLevelDomainToCheck in link['href']:
				if link['href'] not in linksAlreadyChecked:
					if "blog" not in link['href'] and "technology" not in link['href'] and "#" not in link['href']:
						linksAlreadyChecked.append(link['href'])
						scrapeEmailsFromSinglePage(link['href'])
		elif link['href'][0]=="/": 
			#need to account for "/../blabla/folder"

			if currentDomain+link['href'] not in linksAlreadyChecked:
				if "blog" not in linkToScrape+link['href'] and "technology" not in linkToScrape+link['href'] and "#" not in linkToScrape+link['href']: 
					linksAlreadyChecked.append(currentDomain+link['href'])
					scrapeEmailsFromSinglePage(currentDomain+link['href'])
		else:
			if currentDomain+"/"+link['href'] not in linksAlreadyChecked:
				if "blog" not in linkToScrape+link['href'] and "technology" not in linkToScrape+link['href']and "#" not in linkToScrape+link['href']: 
					linksAlreadyChecked.append(currentDomain+"/"+link['href'])
					scrapeEmailsFromSinglePage(currentDomain+"/"+link['href'])

	#end of scrapeEmailsFromSinglePage function - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #



domain = sys.argv[1] 

topLevelDomainToCheck = domain.replace("http://","").replace("www.","").replace("https://","")
if len(topLevelDomainToCheck.split("/"))>0: 
	topLevelDomainToCheck = topLevelDomainToCheck.split("/")[0]

allEmails = []
linksAlreadyChecked = []

print topLevelDomainToCheck

scrapeEmailsFromSinglePage(domain)


print allEmails

