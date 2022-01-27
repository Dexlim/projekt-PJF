from bs4 import BeautifulSoup
import requests
import asyncio
from functools import partial, wraps
import urllib.request
import re
import json
import urllib


def to_thread(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        callback = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, callback)

    return wrapper


class Request:
    def __init__(self, title, officialprice, keyshopprice, image, link):
        self.title = title
        self.officialPrice = officialprice
        self.keyshopPrice = keyshopprice
        self.image = image
        self.link = link


class Info:
    def __init__(self, link, image, title, info):
        self.link = link
        self.image = image
        self.title = title
        self.info = info


@to_thread
def checkPriceRequest(title, maxcounter, currency):
    page = requests.get("https://gg.deals/" + currency + "/games/", params=[('title', title)])
    soup = BeautifulSoup(page.content, "lxml")
    counter = 0
    request_list = []
    soup = soup.select_one("div.game-section.section-row.init-dynamicSidebar")
    for game in soup.select("div.game-details-wrapper"):

        title = game.select_one('div.game-info-title.title').get_text()
        link = "https://gg.deals" + \
               game.select_one('a.action-ext.action-desktop-btn.always-active.action-btn.cta-label-desktop')['href']
        image = game.find_parent('div').select_one('a.main-image > img')['srcset']
        image = image[image.find(',') + 1:image.find('460w')]

        official_price = game.select_one('div.shop-price-wrapper.inline.shop-price-retail')
        official_price = official_price.select_one('a.price-content')
        if official_price is None:
            official_price = "UNAVAILABLE"
        else:
            official_price = official_price.select_one('span.numeric').get_text()
        if official_price.startswith('~'):
            official_price = official_price[1:]

        keyshop_price = game.select_one('div.shop-price-wrapper.inline.shop-price-keyshops')
        keyshop_price = keyshop_price.select_one('a.price-content')
        if keyshop_price is None:
            keyshop_price = "UNAVAILABLE"
        else:
            keyshop_price = keyshop_price.select_one('span.numeric').get_text()

        if keyshop_price.startswith('~'):
            keyshop_price = keyshop_price[1:]

        request = Request(title, official_price, keyshop_price, image, link)
        request_list.append(request)

        counter = counter + 1
        if counter >= maxcounter:
            return request_list
    if len(request_list) < 1:
        request = Request("Not found", '', '',
                          'https://is5-ssl.mzstatic.com/image/thumb/Music114/v4/9b/77/16/9b771654-42cf-de94-6e7d'
                          '-90ccb3587f4f/artwork.jpg/1200x1200bf-60.jpg',
                          '')
        request_list.append(request)
    return request_list


def checkPost(post, post_list):
    link = "https://gg.deals" + post.select_one('a.full-link')['href']
    image = post.select_one('div.news-image-wrapper > img')['src']
    title = post.select_one('h3.news-title > a').get_text()
    info = post.select_one('div.news-lead').get_text()
    freebie = Info(link, image, title, info)
    post_list.append(freebie)
    return post_list


@to_thread
def checkFreebies():
    page_url = "https://gg.deals/news/freebies/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    freebies_list = []
    soup = soup.select_one('div.list-items.news-list')
    for freebie in soup.select('div.item.news-item.news-list-item.init-trimNewsLead.news-cat-freebie.active'):
        freebies_list = checkPost(freebie, freebies_list)
    return freebies_list


@to_thread
def checkBundles():
    page_url = "https://gg.deals/news/bundles/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    bundles_list = []
    soup = soup.select_one('div.list-items.news-list')
    for bundle in soup.select('div.item.news-item.news-list-item.init-trimNewsLead.news-cat-bundle.active'):
        bundles_list = checkPost(bundle, bundles_list)
    return bundles_list


@to_thread
def checkDeals():
    page_url = "https://gg.deals/news/deals/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    deals_list = []
    soup = soup.select_one('div.list-items.news-list')
    for deal in soup.select('div.item.news-item.news-list-item.init-trimNewsLead.news-cat-deal.active'):
        deals_list = checkPost(deal, deals_list)
    return deals_list


@to_thread
def checkBlog():
    page_url = "https://gg.deals/news/blog/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    blog_list = []
    soup = soup.select_one('div.list-items.news-list')
    for blog in soup.select('div.item.news-item.news-list-item.init-trimNewsLead.news-cat-blog.active'):
        blog_list = checkPost(blog, blog_list)
    return blog_list


@to_thread
def getYoutubeURL(text):
    page_url = "https://youtube.com/results"
    if text.startswith("https://www.youtube.com/watch?v="):
        video_id = text.split("https://www.youtube.com/watch?v=")[1]
        video_id = video_id[0:video_id.find("&ab_channel=")]
    else:
        page = requests.get(page_url, params=[('search_query', text)])
        html = urllib.request.urlopen(page.url)
        video_id = re.search(r"watch\?v=(\S{11})", html.read().decode())
        video_id = video_id.group(0).replace("watch?v=", "")

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        print(data['title'])

    return ("https://youtube.com/watch?v=" + video_id), data['title']
