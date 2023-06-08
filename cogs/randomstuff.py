import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, option
import requests
import random as rand

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"}

class randomstuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    random = discord.commands.SlashCommandGroup("random", "Various random things")

    @random.command(description = "a random number within a specified range (default 0-10)")
    async def number(self, ctx, start: discord.Option(int, "Minimum value", default = 0), stop: discord.Option(int, "Maximum value", default = 10)):
        await ctx.respond(rand.randrange(start, stop + 1))

    @random.command(description = "Get a random food, why? idk man Heidi asked for it")
    async def food(self, ctx):
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        data = requests.get(url = url, headers = headers)
        data = data.json()
        data = data["meals"][0]["strMeal"]
        await ctx.respond(data)

def setup(bot):
    bot.add_cog(randomstuff(bot))
    
