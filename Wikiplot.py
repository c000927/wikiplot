# Charlie Sun
# CS 30
# Period 4
# January 13, 2019
# Main file of the Wikiplot

# Import libraries
import urllib.request
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import Iterable
import wikipedia as wiki


def flatten(list):
    """Function that flattens a list"""
    for item in list:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def getWiki():
    """Function that gets information from Wikipedia"""
    # Ask user for the word
    userInput = input("Please input the single word you want to search: ")
    # Ask user for the amount
    searchNum = input("Please input how many articles do you want to search: ")
    linkList = []
    articleList = []
    urlList = []
    # Search the word in Wikipedia
    for items in wiki.search(userInput, results=searchNum):
        linkList.append(items)

    # Check if the word is in the title
    for article in linkList:
        for words in article.split():
            if words in [userInput]:
                articleList.append(article)

    # Get the URL of the article
    for items in articleList:
        articleURL = wiki.page(items).url
        urlList.append(articleURL)

    return urlList


def dataProcessing(urlList):
    """Function that does data processing"""
    totalTokens = []
    # Get the links and request the page
    for link in urlList:
        # Request the URL
        response = urllib.request.urlopen(link)
        # Read the HTML
        html = response.read()
        # Setup the BeautifuLSoup
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(strip=True)
        # Take tokens from the text
        tokens = [t for t in text.split()]
        # Get the stopwords
        stopwordList = stopwords.words("english")
        # Create the clean tokens
        cleanTokens = tokens[:]
        # Remove the stopwords
        for token in tokens:
            if token in stopwords.words("english"):
                cleanTokens.remove(token)
        totalTokens.append(cleanTokens)
    totalTokens = list(flatten(totalTokens))
    # Create the Wikiplot.html file with the links
    file = open("Wikiplot.html", "w+")
    linkContextList = []
    for items in urlList:
        linkContext = """
                      <a href="{}">Article Link</a>
                      """.format(items)
        linkContextList.append(linkContext)
    linksContext = "\n".join(linkContextList)
    context = """

              <html>
              <head></head>
              <body>{}</body>
              </html>
              """.format(linksContext)
    file.write(context)
    file.close()
    # Get the frequency of the words
    freq = nltk.FreqDist(totalTokens)
    # Plot the graph
    freq.plot(20, cumulative=False)


# Run the program and error handling
try:
    dataProcessing(getWiki())
except:
    print("Search error.")
