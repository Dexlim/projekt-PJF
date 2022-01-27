# Projekt na PJF
# Zalewski Wojciech WCY19IJ1S1

import discord
import price
import music
import blog
import reactions
from embed import createHelpEmbed


client = discord.Client()
messagesDict = []


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    voice = discord.utils.get(client.voice_clients, guild=message.guild)

    if message.author == client.user:
        return

    if message.content == "$help":
        await message.channel.send(embed=createHelpEmbed(), reference=message)

    if message.content.startswith("$price "):
        msg = message.content.split("$price ", 1)[1]
        messagesDict.append(await price.price(message, 3, msg))

    if message.content.startswith("$price-all "):
        msg = message.content.split("$price-all ", 1)[1]
        messagesDict.append(await price.price(message, 50, msg))

    if message.content.startswith("$currency "):
        await price.currency(message)

    if message.content == "$free":
        messagesDict.append(await blog.getInfo(message, 'free'))

    if message.content == "$bundles":
        messagesDict.append(await blog.getInfo(message, 'bundle'))

    if message.content == "$deals":
        messagesDict.append(await blog.getInfo(message, 'deal'))

    if message.content == "$blog":
        messagesDict.append(await blog.getInfo(message, 'blog'))

    if message.content == "$play":
        if voice is None:
            return
        if voice.is_paused():
            await message.channel.send(content="Bot has been resumed.", reference=message)
            voice.resume()
            return

    if message.content.startswith("$play "):
        await music.play(voice, message, client)

    if message.content == "$disconnect":
        await music.disconnect(voice, message)

    if message.content == "$pause":
        await music.pause(voice, message)

    if message.content == "$stop":
        await music.stop(voice, message)

    if message.content == "$skip":
        await music.skip(voice, message)

    if message.content == "$queue":
        await music.queue(voice, message)

    if message.content.startswith("$remove "):
        songid = int(message.content.split("$remove ", 1)[1])-2
        await music.remove(voice, message, songid)


@client.event
async def on_reaction_add(reaction, user):
    results = ''
    if user == client.user:
        return
    global messagesDict

    for display in messagesDict:
        if display.message == reaction.message:
            results = display
    if results == '':
        return

    await reactions.react(reaction, results, user)


client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw')  # change to env variable later
