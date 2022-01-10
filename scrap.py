from bs4 import BeautifulSoup
import requests


def checkPriceRequest(title):
    page_url = "https://gg.deals/games/?title=" + title
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, features="html.parser")
    counter = 0
    resultList = []

    for game in soup.findAll('div',{'class':'game-details-wrapper'}):

        title = game.find('div',{'class':'game-info-title title'}).get_text()
        link = "https://gg.deals"+ game.find('a',{'class':'action-ext action-desktop-btn always-active action-btn cta-label-desktop'})['href']

        officialPrice = game.find('div', {'class': 'shop-price-wrapper inline shop-price-retail'})
        officialPrice = officialPrice.find('a', {'class': 'price-content'})
        if(officialPrice is None):
            officialPrice = "UNAVAILABLE"
        else:
            officialPrice = officialPrice.find('span', {'class': 'numeric'}).get_text()
        if (officialPrice.startswith('~')):
            officialPrice = officialPrice[1:]

        keyshopPrice = game.find('div', {'class': 'shop-price-wrapper inline shop-price-keyshops'})
        keyshopPrice = keyshopPrice.find('a', {'class': 'price-content'})
        if(keyshopPrice is None):
            keyshopPrice = "UNAVAILABLE"
        else:
            keyshopPrice = keyshopPrice.find('span', {'class': 'numeric'}).get_text()

        if (keyshopPrice.startswith('~')):
            keyshopPrice = keyshopPrice[1:]

        result = ("\n__**"+title+"**__\nOfficial stores: \t" + officialPrice + "\nKeyshops: \t\t\t" + keyshopPrice+"\n"+link+"\n")
        resultList.append(result)
        counter = counter + 1
        if(counter>=5):
            return resultList
    return resultList

