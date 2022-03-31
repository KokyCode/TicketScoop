import os
import requests
import json
from bs4 import BeautifulSoup
import time

print('TicketScoop V1.0.0 launched!')
print('Developed by BennyB and Koky')


eventLink = input("Please paste the TicketSwap URL you would like to scoop: ")


def getEventLinkInfoMobile():
    headers = {
        'Accept': 'application/json',
        'X-APOLLO-OPERATION-ID': '93c02f4d01c0db3c281e4055a6722973cd92fd29f5e55088e19afaa941f06455',
        'X-APOLLO-OPERATION-NAME': 'GetEvent',
        'X-APOLLO-CACHE-KEY': '987135bac87dd4a227889c8b250c32fb',
        'X-APOLLO-CACHE-FETCH-STRATEGY': 'NETWORK_ONLY',
        'X-APOLLO-EXPIRE-TIMEOUT': '0',
        'X-APOLLO-EXPIRE-AFTER-READ': 'false',
        'X-APOLLO-PREFETCH': 'false',
        'X-APOLLO-CACHE-DO-NOT-STORE': 'false',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '9999',
        'Host': 'api.ticketswap.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.9.0',
        'Accept-Language': 'en_IE',
        'mobile-app-version': '22.02.6414',
        'mobile-app-build-number': '6414',
        'mobile-app-os': 'Android'

    }

    url = 'https://api.ticketswap.com/graphql/public?flow=discovery'
    data = '{"operationName":"GetEvent","variables":{"id":"RXZlbnQ6Y2Y2ZWYzYzktZmI1Ny00NjFkLWFlYWMtNzMwMzMxMzUyNDJi"},"query":"query GetEvent($id: ID!) { node(id: $id) { __typename ...Event } } fragment Event on Event { __typename ...EventItemFields ticketShopUrl category soldTicketsCount ticketAlertsCount isHighlighted uri { __typename ...Uri } createListingUri { __typename ...Uri } isSellingBlocked isBuyingBlocked types(first: 99) { __typename pageInfo { __typename ...PageInfo } edges { __typename node { __typename ...EventTypeFields } } } organizerBrands { __typename id isFollowedByViewer name logoUrl } closedLoopInformation { __typename ... ClosedLoopInformation } eventVideo { __typename videoUrl thumbnailUrl } uploadWarning { __typename ... EventUploadWarning } facebookEventWalls { __typename facebookUrl } cancellationReason } fragment EventItemFields on Event { __typename id name description country { __typename ...Country } location { __typename ...LocationFields } imageUrl startDate endDate category availableTicketsCount lowestPrice { __typename ...Money } maximumPercentage status warning { __typename title message url { __typename text url } } } fragment Uri on Uri { __typename url path trackingUrl } fragment ClosedLoopInformation on ClosedLoopEventInformation { __typename ticketProviderName findYourTicketsUrl } fragment EventUploadWarning on EventUploadWarning { __typename message position } fragment PageInfo on PageInfo { __typename hasNextPage endCursor } fragment EventTypeFields on EventType { __typename id title availableTicketsCount soldTicketsCount ticketAlertsCount startDate endDate isSellingBlocked isRaffleEnabled isOngoing originalTicketPrice { __typename ... Money } lowestPrice { __typename ... Money } maximumAllowedPrice { __typename ... Money } isExpired organizerProduct { __typename ... OrganizerProduct } bundledTickets { __typename ... BundledTickets } seatingOptions { __typename ... SeatingOptions } uploadWarning { __typename ... EventTypeUploadWarning } } fragment Money on Money { __typename amount currency } fragment OrganizerProduct on OrganizerProduct { __typename id displayPrice { __typename ... Money } shop { __typename organizerBranding { __typename name image } } } fragment BundledTickets on EventTypeBundledTickets { __typename amount } fragment SeatingOptions on SeatingOptions { __typename entrance row seat section } fragment EventTypeUploadWarning on EventTypeUploadWarning { __typename message position } fragment Country on Country { __typename name } fragment LocationFields on Location { __typename id name city { __typename ...CityFields } image uri { __typename ...Uri } geoInfo { __typename latitude longitude } supportsAttachments amountOfActiveUpcomingEvents } fragment CityFields on City { __typename id name country { __typename ...Country } imageUrl uri { __typename ...Uri } geoInfo { __typename latitude longitude } }"}'
    response = requests.post(url, data=data, headers=headers)

    if '403 Forbidden' in response.text:
        print('Possible ban detected. Pausing for 5 minutes.')
        time.sleep(300)
        getEventLinkInfoMobile()

    jsonresp = response.json()
    availabletickets = jsonresp['data']['node']['availableTicketsCount']
    ticketinfo = jsonresp['data']['node']['types']['edges']

    if(availabletickets > 0):
        for x in ticketinfo:
            tickettitle = x['node']['title']
            ticketid = x['node']['id']
            ticketamount = x['node']['availableTicketsCount']
            # print(str(ticketamount) + ' tickets available. Type: ' +
            #      tickettitle + '. Grabbing listing info.')
            getListingInfoMobile(ticketid)

    if(availabletickets == 0):
        print('No tickets available, searching again.')
        getEventLinkInfoMobile()

def getListingInfoMobile(id):
    headers = {
        'Accept': 'application/json',
        'X-APOLLO-OPERATION-ID': '93c02f4d01c0db3c281e4055a6722973cd92fd29f5e55088e19afaa941f06455',
        'X-APOLLO-OPERATION-NAME': 'GetEvent',
        'X-APOLLO-CACHE-KEY': '987135bac87dd4a227889c8b250c32fb',
        'X-APOLLO-CACHE-FETCH-STRATEGY': 'NETWORK_ONLY',
        'X-APOLLO-EXPIRE-TIMEOUT': '0',
        'X-APOLLO-EXPIRE-AFTER-READ': 'false',
        'X-APOLLO-PREFETCH': 'false',
        'X-APOLLO-CACHE-DO-NOT-STORE': 'false',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '9999',
        'Host': 'api.ticketswap.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.9.0',
        'Accept-Language': 'en_IE',
        'mobile-app-version': '22.02.6414',
        'mobile-app-build-number': '6414',
        'mobile-app-os': 'Android'

    }

    url = 'https://api.ticketswap.com/graphql/public?flow=discovery '
    data = '{"operationName":"GetFilteredListingsForEventType","variables":{"eventTypeId":"RXZlbnRUeXBlOjE4NjU0MjM=","first":4,"after":null,"status":"AVAILABLE","dateRange":null},"query":"query GetFilteredListingsForEventType($eventTypeId: ID!, $first: Int!, $after: String, $status: ListingStatus!, $dateRange: DateRangeInput) { node(id: $eventTypeId) { __typename ... on EventType { listings: listings(first: $first, after: $after, filter: {listingStatus: $status, dateRange: $dateRange}) { __typename pageInfo { __typename endCursor hasNextPage } edges { __typename node { __typename id hash seller { __typename avatar } price { __typename totalPriceWithTransactionFee { __typename amount currency } } tickets(first: 99) { __typename edges { __typename node { __typename status } } } description dateRange { __typename startDate endDate } } } } } } }"}'
    response = requests.post(url, data=data, headers=headers)
    jsonresp = response.json()
    listinginfo = jsonresp['data']['node']['listings']['edges']
    for i in listinginfo:
        ticketid = i['node']['id']
        tickethash = i['node']['hash']
        ticketprice = i['node']['price']['totalPriceWithTransactionFee']['amount']
        ticketcurrency = i['node']['price']['totalPriceWithTransactionFee']['currency']
        # print('TID:' + ticketid + ' HASH:' + tickethash +
        #      ' ' + ticketcurrency + ' ' + str(ticketprice))
        addToCartMobile(ticketid, tickethash)


def addToCartMobile(ticketid, tickethash):
    headers = {
        'Accept': 'application/json',
        'X-APOLLO-OPERATION-ID': '93c02f4d01c0db3c281e4055a6722973cd92fd29f5e55088e19afaa941f06455',
        'X-APOLLO-OPERATION-NAME': 'AddTicketsToCart',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '9999',
        'Host': 'api.ticketswap.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.9.0',
        'Accept-Language': 'en_IE',
        'Authorization': 'Bearer OThlMDFkMmNkYjJhOWE1MTdjMTQ3MzMxMWQ2OWUwZjQ1YWU5ZDYwOTAyMDk3OGViZDYwYTQ5ZDEwOWIwN2Q4OQ',
        'mobile-app-version': '22.02.6414',
        'mobile-app-build-number': '6414',
        'mobile-app-os': 'Android'

    }

    url = 'https://api.ticketswap.com/graphql/public?flow=discovery '
    data = '{"operationName":"AddTicketsToCart","variables":{"listingId":"' + ticketid + '","listingHash":"' + tickethash + \
        '","amountOfTickets":1},"query":"mutation AddTicketsToCart($listingId: ID!, $listingHash: String!, $amountOfTickets: Int, $ticketIds: [ID]) { addTicketsToCart(input: {listingId: $listingId, listingHash: $listingHash, amountOfTickets: $amountOfTickets, ticketIds: $ticketIds}) { __typename numberOfRequestedTickets numberOfReservedTickets errors { __typename code message } } }"}'
    response = requests.post(url, data=data, headers=headers)
    jsonresp = response.json()
    responseinfo = jsonresp['data']['addTicketsToCart']['errors']
    print(responseinfo)
    if not responseinfo:
        print('Ticket added to cart, nice one mate!')
    elif responseinfo[0]['code'] == 'CART_CURRENCY_MISMATCH':
        print('You cannot have multiple currencies in your checkout. For example a GBP ticket and a EUR ticket. Please empty the cart.')
    elif responseinfo[0]['code'] == 'NO_TICKETS_COULD_BE_RESERVED':
        print('Someone else grabbed the ticket in time, searching again')
        getEventLinkInfoMobile()


getEventLinkInfoMobile()
