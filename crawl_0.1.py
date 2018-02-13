#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from log_ctl import g_log

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

def filter_rule(Dict):
    return 'href' in Dict and Dict['href'].startswith('/wiki/')
    
def get_links(domain, URI):
    '''
    [Description]: open the uri with domain and get all the links in it
    '''
    global pages
    html = open_url(domain+URI)
    if html == None:
        return
    bsObj = BeautifulSoup(html, 'html.parser')
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print('Some attribute lost, continue')
    for link in bsObj.findAll(lambda tag: filter_rule(tag.attrs)):
        if link.attrs['href'] not in pages:
            newPage = link.attrs['href']
            print("--------------------------\n" + newPage)
            pages.add(newPage)
            get_links(domain, newPage)


pages = set()
Dom = 'http://en.wikipedia.org'

get_links(Dom, '')

'''
html = open_url(url)
if html != None:
    bsObj = BeautifulSoup(html, 'html.parser')
    for link in bsObj.find("div", {"id": "bodyContent"}).findAll(lambda tag: filter_rule(tag.attrs)):
        if 'href' in link.attrs:
            print(link.attrs['href'])
'''
