from scrap import getYoutubeURL
import youtube_dl
import discord
import urllib.error
youtube_dl.utils.bug_reports_message = lambda: ''  # hides bug reports

musicqueue = []
titlequeue = []
currentsong = ''
currenttitle = ''


async def queue(voice, message):
    global titlequeue
    if voice is not None and voice.is_playing():
        msg_content = '***1. ' + currenttitle + " <-- current***\n"
        counter = 2
        for title in titlequeue:
            msg_content += str(counter) + ". " + title + "\n"
            counter += 1
        await message.channel.send(content=msg_content, reference=message)
    else:
        await message.channel.send(content="Queue empty.", reference=message)
    return


async def remove(voice, message, songid):
    global titlequeue
    global musicqueue
    if songid == -1:
        voice.stop()
    elif len(musicqueue) >= 1:
        await message.channel.send(content="Removed ***" + titlequeue[songid] + "*** from the queue", reference=message)
        del titlequeue[songid]
        del musicqueue[songid]
    return titlequeue, musicqueue


async def skip(voice, message):
    global currenttitle
    global musicqueue
    if voice is not None and voice.is_playing():
        if len(musicqueue) >= 1:
            await message.channel.send(content="Skipped [***" + currenttitle + "***]")
            voice.stop()
        else:
            await message.channel.send(content="Skipped [***" + currenttitle + "***]")
            voice.stop()
            return


async def stop(voice, message):
    await message.channel.send(content="Music queue has been removed", reference=message)
    voice.stop()
    return


async def pause(voice, message):
    if voice is not None:
        if voice.is_playing():
            await message.channel.send(content="Bot has been paused.", reference=message)
            voice.pause()
            return
        elif voice.is_paused():
            await message.channel.send(content="Bot has been resumed.", reference=message)
            voice.resume()
            return


async def disconnect(voice, message):
    await message.channel.send(content="Bot left the channel.", reference=message)
    if voice is not None:
        await voice.disconnect()


def nextsong(voice, message, client):
    global musicqueue
    global titlequeue
    global currentsong
    global currenttitle
    if len(musicqueue) >= 1:
        currentsong = musicqueue[0]
        currenttitle = titlequeue[0]
        voice.play(musicqueue[0], after=lambda e: nextsong(voice, message, client))
        try:
            client.loop.create_task(message.channel.send(content="Now playing: ***" + titlequeue[0] + "***"))
        except TypeError:
            pass
        del musicqueue[0]
        del titlequeue[0]
    else:
        if not voice.is_playing():
            client.loop.create_task(message.channel.send(content="Queue empty, leaving voice channel."))
            client.loop.create_task(voice.disconnect())
            currentsong = ''
            currenttitle = ''


async def play(voice, message, client):
    global currentsong
    global currenttitle
    global musicqueue
    global titlequeue
    videolink = message.content.split("$play ", 1)[1]
    channel = message.author.voice.channel
    response = await message.channel.send(content="Searching for \'" + videolink + "\'...", reference=message)
    videolink, title = await getYoutubeURL(videolink)

    if voice is None:
        await channel.connect()

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    ydl_opts = {'format': 'bestaudio'}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(videolink, download=False)
        url = info['formats'][0]['url']
    voice = discord.utils.get(client.voice_clients, guild=message.guild)
    song = discord.FFmpegPCMAudio(executable=".\\ffmpeg\\bin\\ffmpeg.exe", source=url, **ffmpeg_options)
    if not voice.is_playing():
        try:
            currenttitle = title
            currentsong = song
            voice.play(song, after=lambda e: nextsong(voice, message, client))
        except urllib.error.HTTPError:
            await response.edit(content="Error downloading a song. Please try again")
        else:
            await response.edit(content="Now playing: ***" + title + "***")
    else:
        await response.edit(content="Added to queue: ***" + title + "***")
        musicqueue.append(song)
        titlequeue.append(title)
