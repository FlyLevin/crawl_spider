#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from log_ctl import g_log
import re
import datetime
import random
import string
import operator

def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
    "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
    "they", "is", "an", "at", "but","we", "his", "from", "that", "not",
    "by", "she", "or", "as", "what", "go", "their","can", "who", "get",
    "if", "would", "her", "all", "my", "make", "about", "know", "will",
    "as", "up", "one", "time", "has", "been", "there", "year", "so",
    "think", "when", "which", "them", "some", "me", "people", "take",
    "out", "into", "just", "see", "him", "your", "come", "could", "now",
    "than", "like", "other", "how", "then", "its", "our", "two", "more",
    "these", "want", "way", "look", "first", "also", "new", "because",
    "day", "more", "use", "no", "man", "find", "here", "thing", "give",
    "many", "well"]
    for word in ngram:
        if word in commonWords:
            return True
    return False

def cleanInput(inputs):
    inputs = re.sub('\n+', "", inputs).lower()
    inputs = re.sub('\[[0-9]*\]', "", inputs)
#    inputs = re.sub(' +', "", inputs)
    inputs = bytes(inputs, "UTF-8")
    inputs = inputs.decode("ascii", "ignore")
#    g_log.debug(inputs)
    cleanInput = []
    inputs = inputs.split(' ')
    for item in inputs:
        item = item.strip(string.punctuation)
#        g_log.debug(item)
        if len(item) > 1 or (item.lower()=='a' or item.lower()=='i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(inputs, n):
    inputs = cleanInput(inputs)
    output = {}
    for i in range(len(inputs)-n+1):
        ngramTemp = " ".join(inputs[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] +=1
    return output

# get all the inner link in the page
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    g_log.debug("get the internal links include url: %s" % includeUrl)
    # find out the links start with /
    try:
        links = bsObj.findAll("a", href=re.compile("^(?!http|https)(/|.*"+includeUrl+")"))
    except Exception as e:
        g_log.error(e)
        return []
    for link in links:
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# get all the external links in the page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    g_log.debug("get the external links exclude url: %s" % excludeUrl)
    # find out all the http/https/www/ and exclude the current urls
    try:
        links = bsObj.findAll("a", href=re.compile("^(http|www|https)((?!"+excludeUrl+").)*$"))
    except Exception as e:
        g_log.error(e)
    for link in links:
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

# splitAddress
def splitAddress(address):
    if address.startswith('http://'):
        addressParts = address.replace('http://', '').split('/')
    elif address.startswith('https://'):
        addressParts = address.replace('https://', '').split('/')
    else:
        addressParts.split('/')
    return addressParts

def open_url(URL):
    '''
    [Description]: open the requested url and return the pure html info
    '''
    try:
        g_log.debug('Connecting the %s' % URL)
        html = urlopen(URL)
        return html
    except Exception as e:
        g_log.error(e)
        return None

def getRandomExternalLink(startingPage):
    html = open_url(startingPage)
    if html == None:
        return None
    bsObj = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(startingPage)
        Nextpage = startingPage+internalLinks[random.randint(0, len(internalLinks)-1)]
        return getRandomExternalLink(Nextpage)
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("random external:" + externalLink)
    followExternalOnly(externalLink)


def main():
    followExternalOnly('http://oreilly.com')

if __name__ == "__main__":
    main()

