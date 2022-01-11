import discord                           # pip install discord.py
from scrap import checkPriceRequest
from embed import createEmbed

client = discord.Client()
left = '⬅'
right = '➡'

class Display:
    def __init__(self, message, request):
        self.message = message
        self.request = request
        self.page = 1
        self.maxPage = len(request)
    def changePage(self,numb):
        self.page+=numb
        if self.page<1:
            self.page = self.maxPage
        if self.page > self.maxPage:
            self.page = 1

messagesDict = []

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$help"):
        msg = message.content.split("$help", 1)[1]
        if msg.startswith(" "):
            msg = msg[1:]
        await message.channel.send("Available commands:\n$price [name] - shows lowest prices of [name] game\n", reference=message)

    if message.content.startswith("$price "):
        msg = message.content.split("$price", 1)[1]
        response = await message.channel.send(embed=discord.Embed(title="Please wait", color=0xeb5ca0),reference=message)
        request = checkPriceRequest(msg)
        await response.edit(embed=createEmbed(request[0],1,len(request)))
        global messagesDict
        display = Display(response,request)
        messagesDict.append(display)
        await response.add_reaction(left)
        await response.add_reaction(right)


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    global messagesDict
    for display in messagesDict:
        if display.message == reaction.message:
            results = display
    if reaction.emoji == left:
        results.changePage(-1)
        await results.message.remove_reaction(left, user)
        await results.message.edit(embed=createEmbed(results.request[results.page-1],results.page,results.maxPage))
        return
    if reaction.emoji == right:
        results.changePage(1)
        await results.message.remove_reaction(right, user)
        await results.message.edit(embed=createEmbed(results.request[results.page-1],results.page,results.maxPage))
        return


client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw')
