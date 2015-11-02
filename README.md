# aidaEmailScraper

scrapeEmails.py is a python script that will list all emails found on a given internet domain (and  subdomains of the domain). Run the program by typing into the command line: python scrapeEmails.py [full-url]. For example: 

python scrapeEmails.py http://www.jana.com 

Running the script requires the BeautifulSoup library (which I have included) as well as PhantomJS. For those running on OS X, I have included the PhantomJS binary, so the script will work out of the box. On Linux or Windows please follow instructions for installing PhantomJS (http://phantomjs.org/download.html). Note: I require a headerless browser like PhantomJS to scrape sites that require javascript (such as jana.com!) and thus, cannot be scraped using cURL. 

I have also included two versions of the email script. The first "scrapeEmails.py" is general and will search for emails on any site on the domain or subdomains of the submitted domain. I found that running this on Jana took a long time (going through all the links on blog.jana.com for example), so I included a version "scrapeJEmails-NoTechOrBlog.py" that scrapes jana.com minus the tech and blog subdomains. 



