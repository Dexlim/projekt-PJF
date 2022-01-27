from embed import createInfoEmbed, createGameEmbed
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


async def react(reaction, results, user):
    if reaction.emoji == LEFT:
        results.changePage(-1)
        await results.message.remove_reaction(LEFT, user)
    elif reaction.emoji == RIGHT:
        results.changePage(1)
        await results.message.remove_reaction(RIGHT, user)
    else:
        return
    if results.displaytype == 'game':
        await results.message.edit(
            embed=createGameEmbed(results.request[results.page - 1], results.page, results.maxPage))
    elif results.displaytype == 'free':
        await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                         results.maxPage, FREEBIE_ICON, FREEBIE_COLOR))
    elif results.displaytype == 'bundle':
        await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                         results.maxPage, BUNDLE_ICON, BUNDLE_COLOR))
    elif results.displaytype == 'deal':
        await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                         results.maxPage, DEALS_ICON, DEALS_COLOR))
    elif results.displaytype == 'blog':
        await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                         results.maxPage, BLOG_ICON, BLOG_COLOR))
    return
