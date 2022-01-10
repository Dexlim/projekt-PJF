import discord                           # pip install discord.py
from scrap import checkPriceRequest

client = discord.Client()


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
        await message.channel.send("Available commands:", reference=message)

    if message.content.startswith("$price "):
        msg = message.content.split("$price", 1)[1]
        await message.channel.send(checkPriceRequest(msg)[0], reference=message)



client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw')
