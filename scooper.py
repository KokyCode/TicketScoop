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
        getEventLinkInfo()

def getListingInfo(url):
    print('Grabbing listing info...')
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
    #print(ticketinfo)
    for l in listings:
        tickethash = ticketinfo[l]['hash']
        ticketid = ticketinfo[l]['id']
        ticketstatus = ticketinfo[l]['status']
        if(ticketstatus == 'AVAILABLE'):
            addToCart(tickethash, ticketid)
            

def addToCart(tickethash, ticketid):
    headers = {
        'Host': 'api.ticketswap.com',
        'Connection': 'keep-alive',
        'Content-Length': '9999',
        'authorization': 'Bearer YzA5YjkzOGJmMzQxNTY3NDY1NWYxZWQwYjhiY2U3NTkxNGJmZmJlYWM1NDg4NTI4MjA3ZWZiYmU5ZTFhNGY3Yw',
        'content-type': 'application/json',
        'accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'sec-ch-ua-platform': "macOS",
        'Origin': 'https://www.ticketswap.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.ticketswap.com/',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    url = 'https://api.ticketswap.com/graphql/public?'
    post = {
        "operationName": "addTicketsToCart",
        "variables": {
        "input": {
            "listingId": ticketid,
            "listingHash": tickethash,
            "amountOfTickets": 1
        }
        },
        "query": "mutation addTicketsToCart($input: AddTicketsToCartInput!) {\n  addTicketsToCart(input: $input) {\n    user {\n      id\n      cart {\n        ...cart\n        __typename\n      }\n      checkout {\n        rows {\n          id\n          title\n          totalPrice {\n            ...money\n            __typename\n          }\n          quantity\n          isMandatory\n          ... on CheckoutTicketRow {\n            id\n            quantity\n            isSecureSwap\n            totalPrice {\n              ...money\n              __typename\n            }\n            eventType {\n              ...eventTypeCheckout\n              __typename\n            }\n            ticketGroups {\n              ...ticketGroups\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    errors {\n      ...cartError\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment cartError on Error {\n  code\n  message\n  __typename\n}\n\nfragment cart on Cart {\n  id\n  isExpired\n  currency\n  __typename\n}\n\nfragment ticketGroups on CheckoutTicketGroup {\n  quantity\n  listing {\n    id\n    dateRange {\n      startDate\n      endDate\n      __typename\n    }\n    description\n    seller {\n      id\n      avatar\n      firstname\n      __typename\n    }\n    __typename\n  }\n  price {\n    ...money\n    __typename\n  }\n  totalPrice {\n    ...money\n    __typename\n  }\n  tickets {\n    id\n    hasAttachment\n    seating {\n      id\n      entrance\n      section\n      row\n      seat\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n\nfragment eventTypeCheckout on EventType {\n  id\n  slug\n  title\n  startDate\n  endDate\n  isOngoing\n  seatingOptions {\n    entrance\n    section\n    row\n    seat\n    __typename\n  }\n  buyerWarning {\n    message\n    __typename\n  }\n  event {\n    id\n    name\n    startDate\n    endDate\n    timeZone\n    location {\n      id\n      name\n      __typename\n    }\n    closedLoopInformation {\n      ...closedLoopInformation\n      __typename\n    }\n    types(first: 99) {\n      edges {\n        node {\n          id\n          slug\n          availableListings: listings(first: 1, filter: {listingStatus: AVAILABLE}) {\n            edges {\n              node {\n                id\n                hash\n                price {\n                  totalPriceWithTransactionFee {\n                    ...money\n                    __typename\n                  }\n                  __typename\n                }\n                numberOfTicketsStillForSale\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment closedLoopInformation on ClosedLoopEventInformation {\n  ticketProviderName\n  findYourTicketsUrl\n  __typename\n}\n"
    }
    response = requests.post(url, json=post, headers=headers)
    if 'totalPriceWithTransactionFee' in response.text:
        print('Sucessfully added ticket to cart')
    else:
        print('Failed to add ticket to cart. Searching again.')
        getEventLinkInfo()

getEventLinkInfo()


