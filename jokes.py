import discord
from discord.commands import slash_command
from discord.ext import commands, tasks
import requests
import traceback
import json
import asyncio

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

def get_joke():
    try:
        url = "https://api.humorapi.com/jokes/random?api-key=39233e46f68e40fc840f887e8089ad0d&include-tags=dark"
        r = requests.get(url = url, headers = headers)
        data = r.json()
        print(data)
        data = data["joke"]
        data.replace("\"", "\\\"")
        data.replace("\'", "'")
        print(fr"{data}")
        file = open("cogs/jokes.json", "r+")
        list = json.load(file)
        list["dark"].append(data)
        jarson = json.dumps(list)
        file.seek(0)
        file.write(jarson)
        file.truncate()
        return data
    except Exception as e:
        print(e)
        traceback.print_exc()
        return "probably daily quota reached"

class jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(description = "some dark jokes for the family")
    async def dark_humor(self, ctx):
        await ctx.respond(fr"{get_joke()}")

def setup(bot):
    bot.add_cog(jokes(bot))