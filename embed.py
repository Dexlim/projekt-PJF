import discord

def createEmbed(title,bot,offprice,keyshprice,gameimage,page,pagemax):
  embed = discord.Embed(title="GAME_TITLE", color=0xeb5ca0)
  embed.set_author(name="BOT_NAME", icon_url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")

  embed.set_thumbnail(url="https://i.pinimg.com/originals/b2/20/9f/b2209f5436079a03492468a177dccda3.jpg")

  embed.add_field(name="Official stores: ", value="OFFICIAL_PRICE", inline=True)
  embed.add_field(name="Keyshops: ", value="KEYSHOP_PRICE", inline=True)

  embed.set_image(url="GAME_IMAGE_URL")

  embed.set_footer(text="Page 1/5")
  return embed


