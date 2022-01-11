from bs4 import BeautifulSoup
import requests

class Request():
    def __init__(self,title,officialPrice,keyshopPrice,image,link):
        self.title = title
        self.officialPrice = officialPrice
        self.keyshopPrice = keyshopPrice
        self.image = image
        self.link = link


def checkPriceRequest(title,maxCounter):
    page_url = "https://gg.deals/games/?title=" + title
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, features="html.parser")
    counter = 0
    requestList = []
    soup = soup.find('div',{'class':'game-section section-row init-dynamicSidebar'})
    for game in soup.findAll('div', {'class': 'game-details-wrapper'}):

        title = game.find('div', {'class': 'game-info-title title'}).get_text()
        link = "https://gg.deals" + \
               game.find('a', {'class': 'action-ext action-desktop-btn always-active action-btn cta-label-desktop'})[
                   'href']
        image_page = requests.get(link)
        soup2 = BeautifulSoup(image_page.content, features="html.parser")
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
