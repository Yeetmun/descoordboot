import discord
from discord.ext import commands, tasks
from discord.commands import slash_command
import time
import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import pandas
# from discord_ui import UI
import matplotlib.pyplot as plt

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"}

nextday = time.mktime(datetime.datetime.strptime(str(datetime.datetime.today().strftime('%d-%m-%Y')),"%d-%m-%Y").timetuple()) + 86400
now = datetime.date.today()
stuff1, nextweek, stuff2 = now.isocalendar()
nextweek = nextweek + 1
daily_open_price = 0
weekly_open_price = 0
daily_difference = 0
weekly_difference = 0


def timeStamp():
  tz = pytz.timezone('US/Eastern')
  time = datetime.datetime.now(tz)
  dateFormatted = time.strftime("%A %d %B %Y")
  timeFormatted = time.strftime("%I:%M %p + %Ss")
  return time, dateFormatted, timeFormatted

def getPrices():
  url = "https://coinmarketcap.com/currencies/ethereum/"
  r = requests.get(url, headers = headers)
  soup = BeautifulSoup(r.text, 'lxml')
  price = soup.find('div', class_ = 'priceValue').findAll('span')[0].text
  
  date, dateFormat, timeFormat = timeStamp()
  return price, date, dateFormat, timeFormat

def getData(id, currency, days, interval):
  cryptoids = check()

  if id in cryptoids:
    url = f'http://api.coingecko.com/api/v3/coins/{id}/market_chart'
    payload = {'vs_currency' : currency, 'days' : days, "interval": interval}
    r = requests.get(url, params = payload, headers = headers)
    data = r.json()
    prices = []
    timestamps = []

    for i in data['prices']:
      prices.append(i[1])
      if interval == "hourly":
        timestamps.append(str(datetime.datetime.fromtimestamp(i[0]/1000)).replace(" ", ", ")[5:14] + "h")
      else:
        timestamps.append(str(datetime.datetime.fromtimestamp(i[0]/1000))[5:10])

    rawData = {
      'Date' : timestamps,
      'Price' : prices
    }

    df = pandas.DataFrame(rawData)
    return df

  else: 
    print('crypto does not exist.')
    return 1

def plotGraph(color='#00E7FF'):
  dayss = [1, 7, 14, 30, 90, 180, 365, 9999]
  intervall = ["hourly", "hourly", "hourly", "hourly", "daily", "daily", "daily", "daily"]
  for i in range(0, len(dayss)):
    ethInfo = getData('ethereum', 'usd', dayss[i], intervall[i])
    ethInfo.plot(x='Date', y='Price', color=color)
    plt.ylabel('Price')
    plt.title('this will never be named properly')
    plt.savefig(f'ethPlot{dayss[i]}.png')

def check():
    url = f'https://api.coingecko.com/api/v3/coins'
    r = requests.get(url, headers = headers)
    data = r.json()
    cryptoids = []
    for i in data:
      cryptoids.append(i['id'])

    return cryptoids 

def price_check():
  global daily_open_price
  global weekly_open_price
  global daily_difference
  global weekly_difference
  global nextday
  global nextweek
  now = datetime.date.today()
  placeholder1, thisweek, placeholder2 = now.isocalendar()
  price, date, dateFormat, timeFormat = getPrices()
  money = float(price[1:].replace(",", ""))
  if thisweek == nextweek:
    weekly_open_price = money
    nextweek += 1
    weekly_difference = money - weekly_open_price
    weekly_difference = "${:0,.2f}".format(weekly_difference)
    weekly_difference = "+" + weekly_difference
  else:
    weekly_difference = money - weekly_open_price
    weekly_difference = "${:0,.2f}".format(weekly_difference)
    if "-" in weekly_difference:
      weekly_difference = weekly_difference.replace("$-", "-$")
    else:
      weekly_difference = "+" + weekly_difference

  if abs(time.time() - nextday) <= 240:
    daily_open_price = money
    nextday += 86400
    daily_difference = money - daily_open_price
    daily_difference = "${:0,.2f}".format(daily_difference)
    daily_difference = "+" + daily_difference
  else:
    daily_difference = money - daily_open_price
    daily_difference = "${:0,.2f}".format(daily_difference)
    if "-" in daily_difference:
      daily_difference = daily_difference.replace("$-", "-$")
    else:
      daily_difference = "+" + daily_difference
  return daily_difference, weekly_difference

def gembed(days):
  price, date, dateFormat, timeFormat = getPrices()
  timestamp = f"Timestamp: {date}"
  daily, weekly = price_check()
  embed = discord.Embed(title = f"Ethereum **{price}, {daily}**", description = f"as of {dateFormat}, {timeFormat} (US/Eastern Time) \n**{weekly}** (weekly)\nDailyprice change is compared to the price at 00:00 UTC \nWeekly price change is compared to price on Monday 00:00 UTC", color = 0xcdb0f9)
  if days > 2 and days != 9999:
    embed.set_footer(text = f"This graph shows {days} days worth of data \nTimestamp: {timestamp}")
  elif days == 9999:
    embed.set_footer(text = f"This graph shows the maximum amount of data \nTimestamp: {timestamp}")
  else:
    embed.set_footer(text = f"This graph shows 1 day of data \nTimestamp: {timestamp}")
  file = discord.File(f"ethPlot{days}.png")
  embed = embed.set_image(url = f"attachment://ethPlot{days}.png")
  return embed, file

class eth_button(discord.ui.View):
     async def on_timeout(self):
         for child in self.children:
             child.disabled = True
         plt.close("all")
         await self.message.edit(view = self)

     @discord.ui.button(label = "1 day", style = discord.ButtonStyle.gray)
     async def button_press1(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(1)[0], file = gembed(1)[1])

     @discord.ui.button(label = "1 week", style = discord.ButtonStyle.gray)
     async def button_press2(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(7)[0], file = gembed(7)[1])

     @discord.ui.button(label="2 weeks", style=discord.ButtonStyle.gray)
     async def button_press3(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(14)[0], file = gembed(14)[1])

     @discord.ui.button(label="1 month", style=discord.ButtonStyle.gray)
     async def button_press4(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(30)[0], file = gembed(30)[1])

     @discord.ui.button(label="3 months", style=discord.ButtonStyle.gray)
     async def button_press5(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(90)[0], file = gembed(90)[1])

     @discord.ui.button(label="6 months", style=discord.ButtonStyle.gray)
     async def button_press6(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(180)[0], file = gembed(180)[1])

     @discord.ui.button(label="1 year", style=discord.ButtonStyle.gray)
     async def button_press7(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(365)[0], file = gembed(365)[1])

     @discord.ui.button(label="All time", style=discord.ButtonStyle.gray)
     async def button_press8(self, button, interaction):
         await interaction.response.edit_message(embed = gembed(9999)[0], file = gembed(9999)[1])

     @discord.ui.button(label = "Kill embed", style=discord.ButtonStyle.danger)
     async def button_press9(self, button, interaction):
         for child in self.children:
             child.disabled = True
         await interaction.response.edit_message(view = self)
  
class ethereum_moniter(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        #self.liveMoniter.start()
        self.count = 0

    def cog_unload(self):
        #self.liveMoniter.cancel()
        pass

    @slash_command(description = "Get the price of ethereum")    
    async def price_check(self, ctx):
      await ctx.respond(price_check())

    # @commands.command()
    @tasks.loop(seconds=300)
    async def liveMoniter(self):
      ethMoniter = self.bot.get_channel(1002742610160517130)
      try:
        price, date, dateFormat, timeFormat = getPrices()
        daily, weekly = price_check()
        timestamp = f"Timestamp: {date}"
        embed = discord.Embed(title = f"Ethereum **{price}, {daily}**", description = f"as of {dateFormat}, {timeFormat} (US/Eastern Time) \n**{weekly}** (weekly)\nDaily price change is compared to the price at 00:00 UTC \nWeekly price change is compared to price on Monday 00:00 UTC", color = 0xcdb0f9)
        
        if self.count % 3 == 0 or self.count == 0:
            plotGraph()
            file = discord.File("ethPlot1.png")
            embed.set_image(url = "attachment://ethPlot1.png")
            embed.set_footer(text = f"This graph shows 1 day of data \nTimestamp: {timestamp}")
            embed.set_thumbnail(url = "https://ethereum.org/static/a183661dd70e0e5c70689a0ec95ef0ba/13c43/eth-diamond-purple.png")
            await ethMoniter.send(embed = embed, file = file, view = eth_button(timeout = 180))
        else:
            embed.set_image(url = "")
            await ethMoniter.send(embed = embed)
        self.count += 1
    
#        if self.count%3 == 0 or self.count == 0:
#          await ethMoniter.send(f"__**ETH**__: **{price}** as of {dateFormat}, {timeFormat} (US/Eastern time)", file=discord.File("ethPlot.png"))
#          await ethMoniter.send(timestamp)
#        else:
#          await ethMoniter.send(f"__**ETH**__: **{price}** as of {dateFormat}, {timeFormat} (US/Eastern time)\nNOTE: add a note later\n{timestamp}")

#        self.count += 1

      except Exception as e:
        await ethMoniter.send(f'ERROR: {e}')
        print(e)
    

      
 
    @liveMoniter.before_loop
    async def beforeMoniter(self):
        print('Waiting for bot...') 
        await self.bot.wait_until_ready()


def setup(bot): 
    bot.add_cog(ethereum_moniter(bot))