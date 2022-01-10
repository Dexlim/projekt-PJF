import discord

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$help"):
        msg = message.content.split("$help",1)[1]
        if msg.startswith(" "):
            msg = msg[1:]
        await message.channel.send("Available commands:", reference=message)


client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw')
