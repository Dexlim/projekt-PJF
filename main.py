import discord  # pip install discord.py
from discord.ext.commands import Bot
from scrap import checkPriceRequest
from scrap import checkFreebies
from embed import createGameEmbed
from  embed import createInfoEmbed


client = Bot("!")
LEFT = '⬅'
RIGHT = '➡'
FREEBIE_ICON = "https://i.imgur.com/jWvycKR.png"
BUNDLE_ICON = "https://i.imgur.com/EryWDBN.png"
DEALS_ICON = "https://i.imgur.com/KMura7R.png"

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
    if message.author == client.user:
        return
    if message.content.startswith("$help"):
        msg = message.content.split("$help", 1)[1]
        if msg.startswith(" "):
            msg = msg[1:]
        await message.channel.send("Available commands:\n" +
                                   "$price [name] - shows lowest prices of [name] game ( 3 top searches )\n" +
                                   "$price-all [name] - shows lowest prices of [name] game ( all searches )\n"+
                                   "$free - shows current free games",
                                   reference=message)

    if message.content.startswith("$price "):
        msg = message.content.split("$price", 1)[1]
        response = await message.channel.send(embed=discord.Embed(title="Searching for \""+msg+" \"", color=0xeb5ca0),
                                              reference=message)
        request = await checkPriceRequest(msg, 3)
        await response.edit(embed=createGameEmbed(request[0], 1, len(request)))
        display = Display(response, request,'game')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)

    if message.content.startswith("$price-all "):
        msg = message.content.split("$price-all", 1)[1]
        response = await message.channel.send(embed=discord.Embed(title="Searching for \""+msg+" \"", color=0xeb5ca0),
                                              reference=message)
        request = await checkPriceRequest(msg, 50)
        await response.edit(embed=createGameEmbed(request[0], 1, len(request)))
        display = Display(response, request,'game')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)
    if message.content == "$free":
        response = await message.channel.send(embed=discord.Embed(title="Checking freebies...",color=0x8223e8), reference=message)
        request = await checkFreebies()
        await response.edit(embed=createInfoEmbed(request[0], 1, len(request),FREEBIE_ICON))
        display = Display(response,request,'freebie')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)
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
        elif results.type == 'freebie':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage,FREEBIE_ICON))
        return

    if reaction.emoji == RIGHT:
        results.changePage(1)
        await results.message.remove_reaction(RIGHT, user)
        if results.type == 'game':
            await results.message.edit(
                embed=createGameEmbed(results.request[results.page-1], results.page, results.maxPage))
        elif results.type == 'freebie':
            await results.message.edit(
                embed=createInfoEmbed(results.request[results.page - 1], results.page, results.maxPage,FREEBIE_ICON))
        return


client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw')
