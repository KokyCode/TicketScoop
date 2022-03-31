import os
import requests
import json
from bs4 import BeautifulSoup
import time

print('TicketScoop V1.0.0 launched!')
print('Developed by BennyB and Koky')


eventLink = input("Please paste the TicketSwap URL you would like to scoop: ")

def slugify(text):
    '''Join with dashes, eliminate punction, clip to maxlen, lowercase.

        >>> ToSeoFriendly("The quick. brown4 fox jumped", 14)
        'the-quick-brow'

    '''
    t = '-'.join(text.split())                                # join words with dashes
    u = ''.join([c for c in t if c.isalnum() or c=='-'])   # remove punctation   
    return u.rstrip('-').lower()      

def getEventLinkInfo():
    headers = {
        'Host': 'www.ticketswap.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    response = requests.get(eventLink,headers=headers)
    x = BeautifulSoup(response.text, 'html.parser')
    y = x 
    res = x.find(id="__NEXT_DATA__").string
    ticketinfojson = json.loads(res)
    ticketinfo = ticketinfojson['props']['pageProps']['event']['entranceTypes']['edges']
    totalcount = 0

    links = y.select("li a")
        
    valid_links = []
    titles = []
    for l in links:
        href = l.get('href')
        if 'event' in href:
            valid_links.append(href)

    for x in ticketinfo:
        title = (x['node']['title'])
        count = str(x['node']['availableTicketsCount'])
        slug = x['node']['slug']
        totalcount = totalcount + int(count)
        id = x['node']['id']
        if(int(count) > 0):
           print('Found ' + count + ' tickets available for ' + title + '. Grabbing listings for ' + id) 
           for v in valid_links:
               m = v.split('/')    
               if slug == m[5]:
                   getListingInfo(v)

    if(totalcount == 0):
        print('No tickets found, searching again...')
        #time.sleep(2)
        #getEventLinkInfo()

def getListingInfo(url):
    headers = {
        'Host': 'www.ticketswap.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    response = requests.get(url,headers=headers)
    x = BeautifulSoup(response.text, 'html.parser')
    res = x.find(id="__NEXT_DATA__").string
    listings = []
    ticketinfojson = json.loads(res)
    ticketinfo = ticketinfojson['props']['pageProps']['initialApolloState']
    for key, value in ticketinfo.items():
        if 'PublicListing:' in str(key):
            listings.append(key)
            #print(key)

    print(listings)


getEventLinkInfo()


