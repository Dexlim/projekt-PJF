import discord


def createGameEmbed(request, page, pagemax):
    if request.link == '':
        embed = discord.Embed(title=request.title, color=0xeb5ca0)
    else:
        embed = discord.Embed(title=request.title, url=request.link, color=0xeb5ca0)

    embed.set_author(name="DealsBot",
                     icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")

    if request.officialPrice != '':
        embed.add_field(name="Official stores: ", value=request.officialPrice, inline=True)
    if request.keyshopPrice != '':
        embed.add_field(name="Keyshops: ", value=request.keyshopPrice, inline=True)

    embed.set_image(url=request.image)

    if pagemax > 1:
        embed.set_footer(text="Page " + str(page) + "/" + str(pagemax))
    return embed


def createInfoEmbed(freebie, page, pagemax, icon_url, color):
    embed = discord.Embed(title=freebie.title, description=freebie.info, url=freebie.link, color=color)
    embed.set_author(name="DealsBot",
                     icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")
    embed.set_image(url=freebie.image)
    embed.set_thumbnail(url=icon_url)
    if pagemax > 1:
        embed.set_footer(text="Page " + str(page) + "/" + str(pagemax))
    return embed


def createHelpEmbed():
    embed = discord.Embed(title="Command List", color=0x0dbd10)
    embed.set_author(name="DealsBot",
                     icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")
    embed.add_field(name="$price [game]",
                    value="Looks for and displays lowest prices of the game in official stores and keyshops ( 3 "
                          "results )",
                    inline=False)
    embed.add_field(name="$price-all [game]",
                    value="Looks for and displays lowest prices of the game in official stores and keyshops ( all "
                          "results )",
                    inline=False)
    embed.add_field(name="$free", value="Displays posts about new freebies games to claim", inline=False)
    embed.add_field(name="$bundles", value="Displays posts about new game bundles", inline=False)
    embed.add_field(name="$deals", value="Displays posts about new deals", inline=False)
    embed.add_field(name="$blog", value="Displays posts from game news blog", inline=False)
    embed.add_field(name="$currency [currency]", value="Change displayed currency, "
                                                       "available currencies:\nUSD EUR PLN AUD BRL CAD\nDKK "
                                                       "NOK RUB SEK CHF GBP")
    embed.add_field(name="$play [song]", value="Adds song to music queue", inline=False)
    embed.add_field(name="$pause", value="Pauses music", inline=False)
    embed.add_field(name="$stop", value="Clears music queue", inline=False)
    embed.add_field(name="$disconnect", value="Disconnects bot from voice chat", inline=False)
    embed.add_field(name="$skip", value="Skips current song", inline=False)
    embed.add_field(name="$queue", value="Shows current song queue", inline=False)
    embed.add_field(name="$remove [id]", value="Remove song with given id from queue, to check id use $queue",
                    inline=False)

    embed.set_footer(text="Bot made as a final project for MUT\nWojciech Zalewski WCY19IJ1S1")
    embed.set_image(url="https://www.wojsko-polskie.pl/wat/u/fe/79/fe7940a2-19bf-49e9-adb8-22bae104a288/logo_wcy_bg")
    return embed
