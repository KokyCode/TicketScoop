import os
import requests
import json
from bs4 import BeautifulSoup
import time

print('TicketScoop V1.0.0 launched!')
print('Developed by BennyB and Koky')


eventLink = input("Please paste the TicketSwap URL you would like to scoop: ")

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
    res = x.find(id="__NEXT_DATA__").text
    ticketinfojson = json.loads(res)
    availabletickets = ticketinfojson['props']['pageProps']['event']['entranceTypes']['edges']
    for x in availabletickets:
        title = x['node']['title'] 
        count = str(x['node']['availableTicketsCount'])
        id = x['node']['id']
        #print(title + ' - ' + count + ' available tickets. ' + '(' + id + ')')

        #if(int(count) > 0 ):
            #print('Found ' + count + ' tickets available for ' + title + '. Grabbing listings for ' + id)

    y = x.select("li a")
    print(y)


    #print(response.text)
   #if(count > 0):
        #print(str(availabletickets) + ' tickets available!')
        # Check listings available, grab all ID's and add em to the cart! Find out what hashing ID is
        
    #if(availabletickets == 0):
       # print('No tickets found... searching again...')
        #time.sleep(2)
        #getEventLinkInfo()

    #print(ticketinfojson)


getEventLinkInfo()



