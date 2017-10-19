import sys
import requests
from bs4 import BeautifulSoup

def main():
    # Initialize the link to the book
    if(len(sys.argv)>1):
            bookLink = sys.argv[1]#'https://www.wattpad.com/1083624-the-shy-girl-has-a-gun-chapter-2'
    else:
        bookLink = 'https://www.wattpad.com/1083624-the-shy-girl-has-a-gun-chapter-2'
        
    # retrieve the links of all chapters from the TOC
    links = retrieveTOC(bookLink)
    chapNumber = 0
    # write ou each chapter to a file
    for link in links:
        writeChapter(link,chapNumber)
        # increment the chapter number
        chapNumber = chapNumber + 1

# Takes a link to a chapter as input and writes the contents of the chapter to a file
def writeChapter(link, chapNumber):
    # Create a file + name it
    file_name = "Chapter_" + str(chapNumber)
    print(file_name,"writing")
    fileD  = open(file_name, "w")
    # retrieve all of the text contained in the pages of this chapter
    chapterTxt = retrieveAllPages(link)
    # write the chapter to the file
    fileD.write(chapterTxt)
 
# Takes a link to a chapter as input and returns all text contained in a chapter as output
def retrieveAllPages(link):
    # create a chapter string, a text string, and a page number
    chapterTxt = ""
    pageTxt = "something"
    pageN = 1
    while pageTxt != "":
        # Initialize text and create link to a page
        pageTxt = ""
        pageLink = link +"/page/" + str(pageN)
        # retrieve Page and create soup object
        page = requests.get(pageLink, headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')
        # Retrieve pre tag text, witch should be the pages content
        preList = soup.find_all("pre")
        #  write all of the content in pre to text
        for pre in preList:
            pageTxt = pageTxt + pre.get_text()
        # Add the page to the chapter
        chapterTxt = chapterTxt + pageTxt
        pageN = pageN +1

    return chapterTxt 

# This function takes an url as input, and retrieves the links to all chapters contained in the Table Of Contents (TOC) 
def retrieveTOC(bookLink):
    links = []
    # Get story html 
    page = requests.get(bookLink, headers = {'User-Agent':'Mozilla/5.0'})
    # Create soup Object
    soup = BeautifulSoup(page.content, 'html.parser')
    # Retrieve all content contained between TOC tags
    toc = soup.find_all('ul',class_="table-of-contents")
    toc = str(toc)
    # Retrieve all of the links inside TOC
    urls = retrieveUrls(toc)
    # Append address to the begining of urls and add them to links
    print(urls)
    for url in urls:
        links.append("https://www.wattpad.com" +url)

    return links
        
# Takes html text as input and returns all urls contained in a tags
def retrieveUrls(htmlTxt):
    urls = []
    soup = BeautifulSoup(htmlTxt,'html.parser')
    aTags = soup.find_all("a")
    # Get the url contained in each a tag (contained in href attribute)
    for a in aTags:
        link = a.get("href")
        urls.append(link)
    return urls


main()
