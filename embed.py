import discord


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


def createInfoEmbed(Freebie,page,pagemax,icon_url,color):
    embed = discord.Embed(title=Freebie.title, description=Freebie.info,url=Freebie.link, color=color)
    embed.set_author(name="DealsBot", icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")
    embed.set_image(url=Freebie.image)
    embed.set_thumbnail(url=icon_url)
    if(pagemax>1):
        embed.set_footer(text="Page " + str(page) + "/" + str(pagemax))
    return embed

def createHelpEmbed():
    embed = discord.Embed(title="Command List",color=0x0dbd10)
    embed.set_author(name="DealsBot", icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")
    embed.add_field(name="$price [game]",value="Looks for and displays lowest prices of the game in official stores and keyshops ( 3 results )",inline=False)
    embed.add_field(name="$price-all [game]", value="Looks for and displays lowest prices of the game in official stores and keyshops ( all results )",inline=False)
    embed.add_field(name="$free", value="Displays posts about new freebies games to claim",inline=False)
    embed.add_field(name="$bundles", value="Displays posts about new game bundles",inline=False)
    embed.add_field(name="$deals", value="Displays posts about new deals",inline=False)
    embed.add_field(name="$blog", value="Displays posts from game news blog",inline=False)
    embed.add_field(name="$currency [currency]", value="Change displayed currency, "
                                                       "available currencies:\nUSD EUR PLN AUD BRL CAD\nDKK "
                                                       "NOK RUB SEK CHF GBP")
    embed.set_image(url="https://promocja.wat.edu.pl/wp-content/uploads/2014/03/Godlo_z-nazwa-w-kontaktach-zagranicznych_monochromatyczne.jpg")
    embed.set_footer(text="Bot made as a final project for MUT\nWojciech Zalewski WCY19IJ1S1")
    return embed

