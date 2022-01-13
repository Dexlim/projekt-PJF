import discord  # pip install discord.py
from discord.ext.commands import Bot
from scrap import checkPriceRequest
from scrap import checkFreebies
from scrap import checkBundles
from scrap import checkDeals
from embed import createGameEmbed
from embed import createInfoEmbed
from embed import createHelpEmbed

client = Bot("!")
LEFT = '⬅'
RIGHT = '➡'
FREEBIE_ICON = "https://i.imgur.com/jWvycKR.png"
FREEBIE_COLOR = 0x7526a6
BUNDLE_ICON = "https://i.imgur.com/EryWDBN.png"
BUNDLE_COLOR = 0xfca503
DEALS_ICON = "https://i.imgur.com/KMura7R.png"
DEALS_COLOR = 0x03b1fc
CURRENCY = 'us';
AVAILABLE_CURRENCIES = ['USD','EUR','PLN','AUD','BRL','CAD','DKK','NOK','RUB','SEK','CHF','GBP']

class Display:
    def __init__(self, message, request,type):
        self.message = message
        self.request = request
        self.page = 1
        self.maxPage = len(request)
        self.type = type

    def changePage(self, numb):
        self.page += numb
        if self.page < 1:
            self.page = self.maxPage
        if self.page > self.maxPage:
            self.page = 1



messagesDict = []


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global messagesDict
    global CURRENCY
    global AVAILABLE_CURRENCIES
    if message.author == client.user:
        return


    if message.content.startswith("$help"):
        msg = message.content.split("$help", 1)[1]
        if msg.startswith(" "):
            msg = msg[1:]
        await message.channel.send(embed=createHelpEmbed(),reference=message)


    if message.content.startswith("$price "):
        msg = message.content.split("$price ", 1)[1]
        response = await message.channel.send(embed=discord.Embed(title="Searching for \""+msg+" \"", color=0xeb5ca0),
                                              reference=message)
        request = await checkPriceRequest(msg, 3,CURRENCY)
        await response.edit(embed=createGameEmbed(request[0], 1, len(request)))
        display = Display(response, request,'game')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)

    if message.content.startswith("$price-all "):
        msg = message.content.split("$price-all ", 1)[1]
        response = await message.channel.send(embed=discord.Embed(title="Searching for \""+msg+" \"", color=0xeb5ca0),
                                              reference=message)
        request = await checkPriceRequest(msg, 50,CURRENCY)
        await response.edit(embed=createGameEmbed(request[0], 1, len(request)))
        display = Display(response, request,'game')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)


    if message.content == "$free":
        response = await message.channel.send(embed=discord.Embed(title="Checking freebies...",color=FREEBIE_COLOR), reference=message)
        request = await checkFreebies()
        await response.edit(embed=createInfoEmbed(request[0], 1, len(request),FREEBIE_ICON,FREEBIE_COLOR))
        display = Display(response,request,'freebie')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)


    if message.content == "$bundles":
        response = await message.channel.send(embed=discord.Embed(title="Checking bundles...",color=BUNDLE_COLOR), reference=message)
        request = await checkBundles()
        await response.edit(embed=createInfoEmbed(request[0], 1, len(request),BUNDLE_ICON,BUNDLE_COLOR))
        display = Display(response,request,'bundle')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)


    if message.content == "$deals":
        response = await message.channel.send(embed=discord.Embed(title="Checking deals...",color=DEALS_COLOR), reference=message)
        request = await checkDeals()
        await response.edit(embed=createInfoEmbed(request[0], 1, len(request),DEALS_ICON,DEALS_COLOR))
        display = Display(response,request,'deal')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)

    if message.content.startswith("$currency "):
        msg = message.content.split("$currency ", 1)[1]
        msg = msg.upper()
        if msg in AVAILABLE_CURRENCIES:
            CURRENCY = AVAILABLE_CURRENCIES[AVAILABLE_CURRENCIES.index(msg)]
            CURRENCY = CURRENCY[:-1].lower()
            await message.channel.send(embed=discord.Embed(title="Changed currency to "+msg,color=0x0dbd10))
        else:
            await message.channel.send(embed=discord.Embed(title="Could not find currency \"" + msg+
                                                            "\", write $help to check for available currencies", color=0xc70e2d))

    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    global messagesDict

    for display in messagesDict:
        if display.message == reaction.message:
            results = display


    if reaction.emoji == LEFT:
        results.changePage(-1)
        await results.message.remove_reaction(LEFT, user)
        if results.type == 'game':
            await results.message.edit(embed=createGameEmbed(results.request[results.page - 1], results.page, results.maxPage))
        elif results.type == 'game-low':
            await results.message.edit(embed=createGameLowEmbed(results.request[results.page - 1], results.page, results.maxPage))
        elif results.type == 'freebie':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage,FREEBIE_ICON,FREEBIE_COLOR))
        elif results.type == 'bundle':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, BUNDLE_ICON, BUNDLE_COLOR))
        elif results.type == 'deal':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, DEALS_ICON, DEALS_COLOR))
        return

    if reaction.emoji == RIGHT:
        results.changePage(1)
        await results.message.remove_reaction(RIGHT, user)
        if results.type == 'game':
            await results.message.edit(
                embed=createGameEmbed(results.request[results.page-1], results.page, results.maxPage))
        elif results.type == 'freebie':
            await results.message.edit(
                embed=createInfoEmbed(results.request[results.page - 1], results.page, results.maxPage,FREEBIE_ICON,FREEBIE_COLOR))
        elif results.type == 'bundle':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, BUNDLE_ICON, BUNDLE_COLOR))
        elif results.type == 'deal':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, DEALS_ICON, DEALS_COLOR))
        return


client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw')
