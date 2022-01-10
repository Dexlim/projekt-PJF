import discord                           # pip install discord.py
from scrap import checkPriceRequest

client = discord.Client()
left = '⬅'
right = '➡'

class Display:
    def __init__(self, message, result):
        self.message = message
        self.result = result
        self.page = 1
        self.maxPage = len(result)
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
        result = checkPriceRequest(msg)
        response = await message.channel.send(result[0]+"Page 1/"+str(len(result)), reference=message)
        global messagesDict
        display = Display(response,result)
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
        await results.message.edit(content=results.result[results.page-1]+"Page "+str(results.page)+"/"+str(len(results.result)))
        return
    if reaction.emoji == right:
        results.changePage(1)
        await results.message.remove_reaction(right, user)
        await results.message.edit(content=results.result[results.page-1]+"Page "+str(results.page)+"/"+str(len(results.result)))
        return


client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw')
