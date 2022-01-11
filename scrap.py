from bs4 import BeautifulSoup
import requests
import asyncio
from functools import partial, wraps
import lxml

def to_thread(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        callback = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, callback)
    return wrapper

class Request():
    def __init__(self,title,officialPrice,keyshopPrice,image,link):
        self.title = title
        self.officialPrice = officialPrice
        self.keyshopPrice = keyshopPrice
        self.image = image
        self.link = link

class Info():
    def __init__(self,link,image,title,info):
        self.link = link
        self.image = image
        self.title = title
        self.info = info


@to_thread
def checkPriceRequest(title,maxCounter):
    page = requests.get("https://gg.deals/games/",params=[('title',title)])
    soup = BeautifulSoup(page.content, "lxml")
    counter = 0
    requestList = []
    soup = soup.find('div',{'class':'game-section section-row init-dynamicSidebar'})
    for game in soup.findAll('div', {'class': 'game-details-wrapper'}):

        title = game.find('div', {'class': 'game-info-title title'}).get_text()
        link = "https://gg.deals" + \
               game.find('a', {'class': 'action-ext action-desktop-btn always-active action-btn cta-label-desktop'})[
                   'href']
        image_page = requests.get(link)
        soup2 = BeautifulSoup(image_page.content, "lxml")
        image = soup2.find('div',{'class':'game-info-image'}).find('img')['src']

        officialPrice = game.find('div', {'class': 'shop-price-wrapper inline shop-price-retail'})
        officialPrice = officialPrice.find('a', {'class': 'price-content'})
        if (officialPrice is None):
            officialPrice = "UNAVAILABLE"
        else:
            officialPrice = officialPrice.find('span', {'class': 'numeric'}).get_text()
        if (officialPrice.startswith('~')):
            officialPrice = officialPrice[1:]

        keyshopPrice = game.find('div', {'class': 'shop-price-wrapper inline shop-price-keyshops'})
        keyshopPrice = keyshopPrice.find('a', {'class': 'price-content'})
        if (keyshopPrice is None):
            keyshopPrice = "UNAVAILABLE"
        else:
            keyshopPrice = keyshopPrice.find('span', {'class': 'numeric'}).get_text()

        if (keyshopPrice.startswith('~')):
            keyshopPrice = keyshopPrice[1:]

        request = Request(title,officialPrice,keyshopPrice,image,link)
        requestList.append(request)

        counter = counter + 1
        if (counter >= maxCounter):
            return requestList
    if len(requestList) < 1:
        request = Request("Not found",'','','https://is5-ssl.mzstatic.com/image/thumb/Music114/v4/9b/77/16/9b771654-42cf-de94-6e7d-90ccb3587f4f/artwork.jpg/1200x1200bf-60.jpg','')
        requestList.append(request)
    return requestList

@to_thread
def checkFreebies():
    page_url = "https://gg.deals/news/freebies/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    freebiesList = []
    soup = soup.find('div', {'class': 'list-items news-list'})
    for freebie in soup.findAll('div', {'class': 'item news-item news-list-item init-trimNewsLead news-cat-freebie active'}):
        link = "https://gg.deals" + freebie.find('a',{'class':'full-link'})['href']
        image = freebie.find('div',{'class':'news-image-wrapper'}).find('img')['src']
        title =  freebie.find('h3',{'class':'news-title'}).find('a').get_text()
        info = freebie.find('div',{'class':'news-lead'}).get_text()
        freebie = Info(link, image, title, info)
        freebiesList.append(freebie)
    return freebiesList

@to_thread
def checkBundles():
    page_url = "https://gg.deals/news/bundles/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    bundlesList = []
    soup = soup.find('div', {'class': 'list-items news-list'})
    print(soup)
    for bundle in soup.findAll('div', {'class': 'item news-item news-list-item init-trimNewsLead news-cat-bundle active'}):
        link = "https://gg.deals" + bundle.find('a',{'class':'full-link'})['href']
        image = bundle.find('div',{'class':'news-image-wrapper'}).find('img')['src']
        title = bundle.find('h3',{'class':'news-title'}).find('a').get_text()
        info = bundle.find('div',{'class':'news-lead'}).get_text()
        bundle = Info(link, image, title, info)
        bundlesList.append(bundle)
    return bundlesList

@to_thread
def checkDeals():
    page_url = "https://gg.deals/news/deals/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    dealsList = []
    soup = soup.find('div', {'class': 'list-items news-list'})
    print(soup)
    for deal in soup.findAll('div', {'class': 'item news-item news-list-item init-trimNewsLead news-cat-deal active'}):
        link = "https://gg.deals" + deal.find('a',{'class':'full-link'})['href']
        image = deal.find('div',{'class':'news-image-wrapper'}).find('img')['src']
        title = deal.find('h3',{'class':'news-title'}).find('a').get_text()
        info = deal.find('div',{'class':'news-lead'}).get_text()
        deal = Info(link, image, title, info)
        dealsList.append(deal)
    return dealsList


