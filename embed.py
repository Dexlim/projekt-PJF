import discord
from scrap import Request
from scrap import Freebie

def createGameEmbed(Request,page,pagemax):
    if(Request.link==''):
        embed = discord.Embed(title=Request.title, color=0xeb5ca0)
    else:
        embed = discord.Embed(title=Request.title, url=Request.link, color=0xeb5ca0)

    embed.set_author(name="DealsBot", icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")

    if(Request.officialPrice!=''):
        embed.add_field(name="Official stores: ", value=Request.officialPrice, inline=True)
    if (Request.keyshopPrice != ''):
        embed.add_field(name="Keyshops: ", value=Request.keyshopPrice, inline=True)

    embed.set_image(url=Request.image)

    if(pagemax>1):
        embed.set_footer(text="Page " + str(page) + "/" + str(pagemax))
    return embed

def createInfoEmbed(Freebie,page,pagemax,icon_url):
    embed = discord.Embed(title=Freebie.title, description=Freebie.info,url=Freebie.link, color=0x7526a6)
    embed.set_author(name="DealsBot", icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")
    embed.set_image(url=Freebie.image)
    embed.set_thumbnail(url='https://i.imgur.com/jWvycKR.png')
    if(pagemax>1):
        embed.set_footer(text="Page " + str(page) + "/" + str(pagemax))
    return embed