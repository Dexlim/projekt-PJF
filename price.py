import scrap
from embed import createGameEmbed
import discord

LEFT = '⬅'
RIGHT = '➡'
CURRENCY = 'pl'
AVAILABLE_CURRENCIES = ['USD', 'EUR', 'PLN', 'AUD', 'BRL', 'CAD', 'DKK', 'NOK', 'RUB', 'SEK', 'CHF', 'GBP']


class Display:
    def __init__(self, message, request, displaytype):
        self.message = message
        self.request = request
        self.page = 1
        self.maxPage = len(request)
        self.displaytype = displaytype

    def changePage(self, numb):
        self.page += numb
        if self.page < 1:
            self.page = self.maxPage
        if self.page > self.maxPage:
            self.page = 1


async def price(message, amount, msg):
    response = await message.channel.send(embed=discord.Embed(title="Searching for \"" + msg + "\"", color=0xeb5ca0),
                                          reference=message)
    request = await scrap.checkPriceRequest(msg, amount, CURRENCY)
    await response.edit(embed=createGameEmbed(request[0], 1, len(request)))
    display = Display(response, request, 'game')
    await response.add_reaction(LEFT)
    await response.add_reaction(RIGHT)
    return display


async def currency(message):
    global CURRENCY
    msg = message.content.split("$currency ", 1)[1]
    msg = msg.upper()
    if msg in AVAILABLE_CURRENCIES:
        CURRENCY = AVAILABLE_CURRENCIES[AVAILABLE_CURRENCIES.index(msg)]
        CURRENCY = CURRENCY[:-1].lower()
        await message.channel.send(embed=discord.Embed(title="Changed currency to " + msg, color=0x0dbd10))
    else:
        await message.channel.send(embed=discord.Embed(title="Could not find currency \"" + msg +
                                                             "\", write $help to check for available currencies",
                                                       color=0xc70e2d))
