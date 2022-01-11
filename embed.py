import discord


def createEmbed(title, bot, offprice, keyshprice, gameimage, page, pagemax):
    embed = discord.Embed(title=title, color=0xeb5ca0)
    embed.set_author(name=bot, icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")

    embed.set_thumbnail(url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")

    embed.add_field(name="Official stores: ", value=offprice, inline=True)
    embed.add_field(name="Keyshops: ", value=keyshprice, inline=True)

    embed.set_image(url=gameimage)

    embed.set_footer(text="Page" + str(page) + "/" + str(pagemax))
    return embed
