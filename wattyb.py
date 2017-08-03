import requests
from bs4 import BeautifulSoup

def main():

    urlString = "https://www.wattpad.com/192745276-assassin-one-author%27s-note-updates-friday"
    # Get links to webpages with other chapters aka table of content
    links = get_links(urlString)

    # write all of the chapters inside of links
    chapNumber = 0
    for listOfLinks in links:
        writeOneChapter(listOfLinks, chapNumber)
        chapNumber = chapNumber + 1

# Writes a chapters content using and url
def writeOneChapter(listOfLinks,chapNumber):
    # Create file + name it
    file_name = "Chapter_" + str(chapNumber)
    fileD = open(file_name,"w")

    for urlString in listOfLinks: 
        # Get page
        page = requests.get(urlString, headers = {'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')
        preList = soup.find_all("pre")
        text = ""
        for pre in preList:
            text = text + pre.get_text()

        fileD.write(text)

# Returns a list of list of links e.i [["...chap1-1","...chap1-2"][....]]
def get_links(urlString):

    links =[]
    # Get table of content
    page = requests.get(urlString, headers = {'User-Agent': 'Mozilla/5.0'})
    # Create soup object
    soup = BeautifulSoup(page.content, 'html.parser')
    ul = soup.find_all("ul", class_= "table-of-contents")
    ul = str(ul)
    # Get links from table of contents
    soup = BeautifulSoup(ul, 'html.parser')
    tableOfContents = soup.find_all("a")
    for a in tableOfContents:
        link = a.get("href")
        urlString = "https://www.wattpad.com" + link
        links.append(get_more_links(urlString))

    return links

def get_more_links(urlString):

    pageN = 1
    chap_links = []
    text = " "
    # Keep making http requests until we get to a page with <pre> != ""
    while text != "":
        text = ""
        newUrl = urlString +"/page/" + str(pageN)
        
        # Get the page html
        page = requests.get(newUrl, headers = {'User-Agent': 'Mozilla/5.0'})
        # Create soup object
        soup = BeautifulSoup(page.content, 'html.parser')
        # Retrieve <pre> content
        prelist = soup.find_all("pre")
        # Retrieve pre text
        #print("we\'ve entered the loop")
        for pre in prelist:
            text = text + pre.get_text()
        if text != "":
            chap_links.append(newUrl)
        pageN = pageN + 1
        #print("|"+text+"|") 
    for chap in chap_links: print(chap) # This is a debug statement
    return chap_links



main()
