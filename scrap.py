from bs4 import BeautifulSoup
import requests
import asyncio
from functools import partial, wraps

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
def checkPriceRequest(title,maxCounter,currency):
    page = requests.get("https://gg.deals/"+currency+"/games/",params=[('title',title)])
    soup = BeautifulSoup(page.content, "lxml")
    counter = 0
    requestList = []
    soup = soup.select_one("div.game-section.section-row.init-dynamicSidebar")
    for game in soup.select("div.game-details-wrapper"):

        title = game.select_one('div.game-info-title.title').get_text()
        link = "https://gg.deals" + \
               game.select_one('a.action-ext.action-desktop-btn.always-active.action-btn.cta-label-desktop')['href']
        image = game.find_parent('div').select_one('a.main-image > img')['srcset']
        image = image[image.find(',')+1:image.find('460w')]

        officialPrice = game.select_one('div.shop-price-wrapper.inline.shop-price-retail')
        officialPrice = officialPrice.select_one('a.price-content')
        if (officialPrice is None):
            officialPrice = "UNAVAILABLE"
        else:
            officialPrice = officialPrice.select_one('span.numeric').get_text()
        if (officialPrice.startswith('~')):
            officialPrice = officialPrice[1:]

        keyshopPrice = game.select_one('div.shop-price-wrapper.inline.shop-price-keyshops')
        keyshopPrice = keyshopPrice.select_one('a.price-content')
        if (keyshopPrice is None):
            keyshopPrice = "UNAVAILABLE"
        else:
            keyshopPrice = keyshopPrice.select_one('span.numeric').get_text()

        if (keyshopPrice.startswith('~')):
            keyshopPrice = keyshopPrice[1:]

        request = Request(title, officialPrice, keyshopPrice, image, link)
        requestList.append(request)

        counter = counter + 1
        if (counter >= maxCounter):
            return requestList
    if len(requestList) < 1:
        request = Request("Not found", '', '',
                          'https://is5-ssl.mzstatic.com/image/thumb/Music114/v4/9b/77/16/9b771654-42cf-de94-6e7d-90ccb3587f4f/artwork.jpg/1200x1200bf-60.jpg',
                          '')
        requestList.append(request)
    return requestList

@to_thread
def checkFreebies():
    page_url = "https://gg.deals/news/freebies/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    freebiesList = []
    soup = soup.select_one('div.list-items.news-list')
    for freebie in soup.select('div.item.news-item.news-list-item.init-trimNewsLead.news-cat-freebie.active'):
        link = "https://gg.deals" + freebie.select_one('a.full-link')['href']
        image = freebie.select_one('div.news-image-wrapper > img')['src']
        title =  freebie.select_one('h3.news-title > a').get_text()
        info = freebie.select_one('div.news-lead').get_text()
        freebie = Info(link, image, title, info)
        freebiesList.append(freebie)
    return freebiesList

@to_thread
def checkBundles():
    page_url = "https://gg.deals/news/bundles/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    bundlesList = []
    soup = soup.select_one('div.list-items.news-list')
    for bundle in soup.select('div.item.news-item.news-list-item.init-trimNewsLead.news-cat-bundle.active'):
        link = "https://gg.deals" + bundle.select_one('a.full-link')['href']
        image = bundle.select_one('div.news-image-wrapper > img')['src']
        title = bundle.select_one('h3.news-title > a').get_text()
        info = bundle.select_one('div.news-lead').get_text()
        bundle = Info(link, image, title, info)
        bundlesList.append(bundle)
    return bundlesList

@to_thread
def checkDeals():
    page_url = "https://gg.deals/news/deals/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    dealsList = []
    soup = soup.select_one('div.list-items.news-list')
    for deal in soup.select('div.item.news-item.news-list-item.init-trimNewsLead.news-cat-deal.active'):
        link = "https://gg.deals" + deal.select_one('a.full-link')['href']
        image = deal.select_one('div.news-image-wrapper > img')['src']
        title = deal.select_one('h3.news-title > a').get_text()
        info = deal.select_one('div.news-lead').get_text()
        deal = Info(link, image, title, info)
        dealsList.append(deal)
    return dealsList


