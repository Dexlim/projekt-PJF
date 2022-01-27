# Projekt na PJF
# Zalewski Wojciech WCY19IJ1S1
# pip install discord.py
# pip install PyNaCl to use voice
# pip install youtube_dl

import discord
from discord.ext.commands import Bot
import asyncio
import youtube_dl
from scrap import *
from embed import *

client = discord.Client()
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
CURRENCY = 'us';
AVAILABLE_CURRENCIES = ['USD','EUR','PLN','AUD','BRL','CAD','DKK','NOK','RUB','SEK','CHF','GBP']

youtube_dl.utils.bug_reports_message = lambda: '' # hides bug reports

messagesDict = []
musicQueue = []
titleQueue = []
currentSong = ''
currentTitle = ''

class Display():
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

def nextSong(voice, message):
    global currentSong
    global currentTitle

    if len(musicQueue) >= 1:
        currentSong = musicQueue[0]
        currentTitle = titleQueue[0]
        voice.play(musicQueue[0], after=lambda e:nextSong(voice, message))
        try:
            client.loop.create_task(message.channel.send(content="Now playing: ***" + titleQueue[0]+"***"))
        except TypeError:
            pass
        del musicQueue[0]
        del titleQueue[0]
    else:
        if not voice.is_playing():
            client.loop.create_task(message.channel.send(content="Queue empty, leaving voice channel."))
            client.loop.create_task(voice.disconnect())
            currentSong = ''
            currentTitle = ''
    return

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global messagesDict
    global CURRENCY
    global AVAILABLE_CURRENCIES
    global currentTitle
    global currentSong
    if message.author == client.user:
        return


    if message.content.startswith("$help"):
        msg = message.content.split("$help", 1)[1]
        if msg.startswith(" "):
            msg = msg[1:]
        await message.channel.send(embed=createHelpEmbed(),reference=message)


    if message.content.startswith("$price "):
        msg = message.content.split("$price ", 1)[1]
        response = await message.channel.send(embed=discord.Embed(title="Searching for \""+msg+"\"", color=0xeb5ca0),
                                              reference=message)
        request = await checkPriceRequest(msg, 3,CURRENCY)
        await response.edit(embed=createGameEmbed(request[0], 1, len(request)))
        display = Display(response, request,'game')
        messagesDict.append(display)
        await response.add_reaction(LEFT)
        await response.add_reaction(RIGHT)

    if message.content.startswith("$price-all "):
        msg = message.content.split("$price-all ", 1)[1]
        response = await message.channel.send(embed=discord.Embed(title="Searching for \""+msg+"\"", color=0xeb5ca0),
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

    if message.content == "$blog":
        response = await message.channel.send(embed=discord.Embed(title="Checking blog...",color=BLOG_COLOR), reference=message)
        request = await checkBlog()
        await response.edit(embed=createInfoEmbed(request[0], 1, len(request),BLOG_ICON,BLOG_COLOR))
        display = Display(response,request,'blog')
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


    if message.content == "$play":
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice is None:
            return
        if voice.is_paused():
            await message.channel.send(content="Bot has been resumed.", reference=message)
            voice.resume()
            return

    if message.content.startswith("$play "):
        video_link = message.content.split("$play ", 1)[1]
        channel = message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        response = await message.channel.send(content="Searching for \'" + video_link + "\'...", reference=message)
        video_link, title = await getYoutubeURL(video_link)

        if voice == None:
            await channel.connect()

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        ydl_opts = {'format': 'bestaudio'}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=False)
            URL = info['formats'][0]['url']
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        song = discord.FFmpegPCMAudio(executable=".\\ffmpeg\\bin\\ffmpeg.exe", source=URL, **FFMPEG_OPTIONS)
        if not voice.is_playing():
            try:
                currentTitle = title
                currentSong = song
                voice.play(song, after=lambda e: nextSong(voice, message))
            except:
                await response.edit(content="Error downloading a song. Please try again")
            else:
                await response.edit(content="Now playing: ***" + title+"***")
        else:
            await response.edit(content="Added to queue: ***" + title+"***")
            musicQueue.append(song)
            titleQueue.append(title)

    if message.content == "$disconnect":
        await message.channel.send(content="Bot left the channel.", reference=message)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if not voice == None:
            await voice.disconnect()

    if message.content == "$pause":
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice != None:
            if voice.is_playing():
                await message.channel.send(content="Bot has been paused.", reference=message)
                voice.pause()
                return
            elif voice.is_paused():
                await message.channel.send(content="Bot has been resumed.", reference=message)
                voice.resume()
                return

    if message.content == "$stop":
        await message.channel.send(content="Music queue has been removed", reference=message)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        voice.stop()

    if message.content == "$skip":
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice != None and voice.is_playing():
            if len(musicQueue) >= 1:
                    await message.channel.send(content="Skipped [***"+currentTitle+"***]")
                    voice.stop()
            else:
                await message.channel.send(content="Skipped [***" + currentTitle + "***]")
                voice.stop()
                return

    if message.content == "$queue":
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice != None and voice.is_playing():
            msg_content='***1. '+currentTitle+" <-- current***\n"
            counter = 2
            for title in titleQueue:
                msg_content+= str(counter) + ". "+title+"\n"
                counter+=1
            await message.channel.send(content=msg_content, reference=message)
        else:
            await message.channel.send(content="Queue empty.", reference=message)

    if message.content.startswith("$remove "):
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        id = int(message.content.split("$remove ", 1)[1])-2
        if id == -1:
            voice.stop()
        elif len(musicQueue) >= 1:
            await message.channel.send(content="Removed ***"+titleQueue[id]+"*** from the queue", reference=message)
            del titleQueue[id]
            del musicQueue[id]



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
                                                             results.maxPage,FREEBIE_ICON,FREEBIE_COLOR))
        elif results.type == 'bundle':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, BUNDLE_ICON, BUNDLE_COLOR))
        elif results.type == 'deal':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, DEALS_ICON, DEALS_COLOR))
        elif results.type == 'blog':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, BLOG_ICON, BLOG_COLOR))
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
        elif results.type == 'blog':
            await results.message.edit(embed=createInfoEmbed(results.request[results.page - 1], results.page,
                                                             results.maxPage, BLOG_ICON, BLOG_COLOR))
        return


client.run('OTMwMDgyMzAwMDc3NjcwNDYy.YdwspA.GWhFT0o997OFLFgSPrmoghsWjvw') # change to env variable later
