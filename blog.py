from scrap import checkFreebies, checkBlog, checkDeals, checkBundles
import discord
from embed import createInfoEmbed

LEFT = '⬅'
RIGHT = '➡'
FREEBIE_ICON = "https://i.imgur.com/jWvycKR.png"
FREEBIE_COLOR = 0x7526a6
BUNDLE_ICON = "https://i.imgur.com/EryWDBN.png"
BUNDLE_COLOR = 0xfca503
DEALS_ICON = "https://i.imgur.com/KMura7R.png"
DEALS_COLOR = 0x03b1fc
BLOG_ICON = "https://i.imgur.com/Nu4d5lx.png"
BLOG_COLOR = 0xc91818


class Display:
    def __init__(self, message, request, displaytype):
        self.message = message
        self.request = request
        self.page = 1
        self.maxPage = len(request)
        self.displaytype = displaytype

    def changePage(self, numb):
        self.page += numb
        if self.page < 1:
            self.page = self.maxPage
        if self.page > self.maxPage:
            self.page = 1


async def getInfo(message, info_type):
    if info_type == 'free':
        icon = FREEBIE_ICON
        color = FREEBIE_COLOR
        response = await message.channel.send(embed=discord.Embed(title="Checking freebies...", color=color),
                                              reference=message)
        request = await checkFreebies()

    elif info_type == 'bundle':
        icon = BUNDLE_ICON
        color = BUNDLE_COLOR
        response = await message.channel.send(embed=discord.Embed(title="Checking bundles...", color=color),
                                              reference=message)
        request = await checkBundles()

    elif info_type == 'deal':
        icon = DEALS_ICON
        color = DEALS_COLOR
        response = await message.channel.send(embed=discord.Embed(title="Checking deals...", color=color),
                                              reference=message)
        request = await checkDeals()

    elif info_type == 'blog':
        icon = BLOG_ICON
        color = BLOG_COLOR
        response = await message.channel.send(embed=discord.Embed(title="Checking blog...", color=color),
                                              reference=message)
        request = await checkBlog()

    else:
        return

    await response.edit(embed=createInfoEmbed(request[0], 1, len(request), icon, color))
    display = Display(response, request, info_type)
    await response.add_reaction(LEFT)
    await response.add_reaction(RIGHT)
    return display
