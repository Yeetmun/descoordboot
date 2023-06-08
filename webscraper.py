import discord
from discord.ext import commands
from discord.commands import slash_command, option
# from discord import app_commands
from bs4 import BeautifulSoup
import requests
import os

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

class webscraper(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description = "what's the weather like today?")
    async def weather(self, ctx, units = discord.Option(name = "unit", choices = ["Imperial", "Metric", "Standard"], description = "The unit of measurement duh", required = True), city = discord.Option(name = "city", description = "The city duh", required = False)):
      #raspberry pi token key is "WEATHER"
      try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ['WEATHER']}&units={units}"
      except:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ['weather_token']}&units={units}"
      #await ctx.send(f"{url}")
      r = requests.get(url, headers = headers)
      data = r.json()
      print(data)
      try:
        sky = data['weather'][0]['main']
        skyDesc = data['weather'][0]['description']
        temp = data['main']['temp']
        feelTemp = data['main']['feels_like']
        # weather = data['weather'][1]['main']
        # weatherDesc = data['weather'][1]['description']
        humidity = data['main']['humidity']
        country = data['sys']['country']
        windspeed = data['wind']['speed']
        degreeSign = ""
        if units.lower() == 'imperial':
          degreeSign = "℉"
        elif units.lower() == 'metric':
          degreeSign = "℃" 
        elif units.lower() == 'standard':
          degreeSign = "K"
        else:
          await ctx.respond('**ERROR: use actual valid unit. The three ones are imperial ||(fahrenheit)||, metric ||(celsius)||, and standard ||(kelvin)||.**')
          return
        await ctx.respond(f"""__**City**__: {city.capitalize()} ({country})
__**Units**__: {units.capitalize()} system
It is {sky.lower()} ({skyDesc.lower()}), temperature is {temp}{degreeSign} but feels like {feelTemp}{degreeSign}. The humidity is {humidity}%, and for those of you going surfing, the wind speed is {windspeed}.
      """)
      except KeyError:
        await ctx.respond(f'thats not a city <:thinking1:892138392953958460>')

  
    @slash_command(description = "see how much money you've lost today!", help = " - _stonks {stonck symbol} #Example: _stonks AMZN")
    async def stonks(self, ctx, symbol):
        url = f'https://finance.yahoo.com/quote/{symbol}'
        r = requests.get(url, headers = headers)
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            # findAll always returns in a list form, so we can index it.
            price = soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)').text
            growth = soup.find('div', class_ = 'D(ib) Mend(20px)').findAll('span')[1].text
            await ctx.respond(f'{symbol.upper()}: ${price}, {growth}')
            
        except AttributeError:
            await ctx.send('You have an invalid stock symbol. Try putting in one that exists.')

    @slash_command(description = "see how much money the energy wasters are earning!", help = " - Example: _crypto dogecoin #checks dogecoin prices")
    async def crypto(self, ctx, crypto):
      URL = f"https://coinmarketcap.com/currencies/{crypto}/"
      r = requests.get(URL, headers = headers)

      try:
        soup = BeautifulSoup(r.text, 'lxml')
        price = soup.find('div', class_ = 'priceValue').findAll('span')[0].text
        await ctx.respond(f'{crypto.capitalize()}: {price}')
      except AttributeError:
        await ctx.respond('argument should have valid ALL LOWERCASE crypto name. Example: _crypto dogecoin, _crypto ethereum')


def setup(bot): 
    bot.add_cog(webscraper(bot))
