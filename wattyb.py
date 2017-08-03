import requests
from bs4 import BeautifulSoup

def main():
    #Get a link to any page of the story, an example of input is :
    #"https://www.wattpad.com/192745276-assassin-one-author%27s-note-updates-friday"
    urlString = input():
    # Get links to webpages with other chapters from the table of content
    links = get_links(urlString)

    # Write all of the chapters inside of "links"
    chapNumber = 0
    for listOfLinks in links:
        writeOneChapter(listOfLinks, chapNumber)
        chapNumber = chapNumber + 1

# Writes a chapters content using and url
def writeOneChapter(listOfLinks,chapNumber):
    # Create a Chapters file + name it
    file_name = "Chapter_" + str(chapNumber)
    fileD = open(file_name,"w")
    
    # Since each chapter might have multiple "pages", write them all to the same file
    for urlString in listOfLinks: 
        # Get page
        page = requests.get(urlString, headers = {'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')
        # Get all content within <pre> tags
        preList = soup.find_all("pre")
        # Set the text variable that we will use to store the text inside <pre> tags
        text = ""
        for pre in preList:
            text = text + pre.get_text()
        # Write text to the file
        fileD.write(text)

# Returns a list of list of links e.i [["...chap1-1","...chap1-2"][....]]
def get_links(urlString):
    # Create the links variable
    links =[]
    # Get table of content
    page = requests.get(urlString, headers = {'User-Agent': 'Mozilla/5.0'})
    # Create soup object
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find the Table of Contents
    ul = soup.find_all("ul", class_= "table-of-contents")
    # Make the table of contents html into "string" form
    ul = str(ul)
    # Get links from table of contents by creating another soup object
    soup = BeautifulSoup(ul, 'html.parser')
    # Find all <a> tags inside of the "Table of Contents"
    tableOfContents = soup.find_all("a")
    # Go through the <a> tags and retrieve the contents of "href", then create a chapters url with it.
    # Call the get_more_links function, that checks to see if there is more then one "page" per chapter
    for a in tableOfContents:
        link = a.get("href")
        urlString = "https://www.wattpad.com" + link
        links.append(get_more_links(urlString))

    return links

# Some webpages update after you scroll down
# This function checks to see how many "pages" each chapter has and returns a list of there urls
def get_more_links(urlString):
    # Start with page 1, chap_links is our return value, text must not be empty, or the while loop will never start
    pageN = 1
    chap_links = []
    text = " "
    # Keep making http requests until we get to a page with where the data inbetween the <pre> tags is empty 
    # (we store that data in "text" variable)
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
        for pre in prelist:
            text = text + pre.get_text()
        if text != "":
            chap_links.append(newUrl)
        # Move on to the next page
        pageN = pageN + 1
        #print("|"+text+"|")
    #for chap in chap_links: print(chap) # This is a debug statement
    return chap_links



main()
