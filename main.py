import discord
from discord.ext import commands, tasks
from discord.commands import option
import os
import sys
import asyncio
import math
import random
import pathlib
import traceback
import time

bot = discord.Bot(prefix = "_", intents = discord.Intents.all())
stuff_to_do = ["make dark humor command (done, must collect jokes now)", "make dice gambling", "finish rps", "make graph creator", "roulette (+ russian (done (kinda)))"]

# ---------------------------------------------------------------------------------------

def file_solver(extension):
  filename = extension + ".py"
  for root, dirs, files in os.walk(os.getcwd()):
    for name in files:
      if filename in name:
        filepath = os.path.abspath(os.path.join(root, name))
        path = filepath.find("cogs")
        filepath = filepath[path:-3]
        filepath = filepath.replace("\\", ".") if "\\" in filepath else filepath.replace("/", ".")
        return filepath

@bot.event
async def on_ready():
  await bot.change_presence(activity = discord.Activity(name = "Schlop schlop schlop schlop"))
  print("ready")

@bot.command(description = "literally the credits", help = "really?")
async def credits(ctx):
  await ctx.respond("YEET#5381: Owner, current maintainer and dev")

@bot.command(description = "Hey how's the dev doing today?")
async def dev_status(ctx):
  await ctx.respond("FINALS")

@bot.command(description = "is today a snowday?", help = "honestly come on")
async def snowday(ctx):
  msg = await ctx.respond("Fetching data...")
  msg = await msg.original_response()
  await asyncio.sleep(2.5)
  await msg.edit(content = "Just kidding! There will be no more snowdays due to Global Warming. Happy suffering!")

@bot.command(description = "i dont know what the hell im doing", help = "idk man")
async def ping(ctx):
  await ctx.respond(f"Pong! {round(bot.latency*1000, 4)}ms")

@bot.command(description = "Admin command that terminates main.py", help = "no.")
async def kill(ctx):
    if str(ctx.author) == "YEET#5381":
      await ctx.respond("He's fuckin' dead!")
      sys.exit("till death do us part")

'''
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
'''

@bot.command(description = "reload a cog so that it runs updated code")
async def reload(ctx, extension):
  if str(ctx.author) == "YEET#5381":
    msg = await ctx.respond("working...")
    msg = await msg.original_response()
    filepath = file_solver(extension)
    bot.unload_extension(f'{filepath}')
    time.sleep(0.5)
    bot.load_extension(f'{filepath}')
    await msg.edit(f'Reloaded {extension}')
  else:
    await ctx.respond("Unauthorized")

@bot.command(description = "literally just yeet a cog out of existence")
async def unload(ctx, extension):
  if str(ctx.author) == "YEET#5381":
    filepath = file_solver(extension)
    bot.unload_extension(f"{filepath}")
    await ctx.respond(f"unloaded {extension}")
  else:
    await ctx.respond("Unauthorized")
  
@bot.command(description = "add or unyeet a cog")
async def load(ctx, extension):
  if str(ctx.author) == "YEET#5381":
    filepath = file_solver(extension)
    bot.load_extension(f"{filepath}")
    await ctx.respond(f"loaded {extension}")
  else:
    await ctx.respond("Unauthorized")

@bot.command(description = "see how much shit you have to do!")
async def backlog(ctx):
  await ctx.respond("\n".join(stuff_to_do))

@bot.command(description = "reload main because im too lazy to stop the process manually")
async def reset(ctx):
  if str(ctx.author) == "YEET#5381":
    await ctx.respond("whee!")
    os.system("python3.10 reload_main.py")
    sys.exit("reset")
  else:
    await ctx.respond("Unauthorized")

@bot.command(description = "pull from GitHub (no, no rizz, it won't happen ever, never...)")
async def pull(ctx):
  if str(ctx.author) == "YEET#5381":
    msg = await ctx.respond("Pulling... (no not people, code, from GitHub)")
    msg = await msg.original_response()
    os.system("git pull")
    await msg.edit(content = "done")

@bot.command(description = "le ded")
async def kms(ctx):
  await ctx.respond("You're dead! Now what?")

bot.load_extension(f"cogs.reddit")
bot.load_extension(f"cogs.ethereum_moniter")
bot.load_extension(f"cogs.webscraper")
bot.load_extension(f"cogs.jokes")
bot.load_extension(f"cogs.minigames.rps")
bot.load_extension(f"cogs.gambling")
bot.load_extension(f"cogs.calculator")
bot.load_extension(f"cogs.misc.randomstuff")
bot.load_extension(f"cogs.heidi")
bot.load_extension(f"cogs.minigames.roulette")
bot.load_extension(f"cogs.moderation.channel")
bot.load_extension(f"cogs.chat")
bot.load_extension(f"cogs.misc.dictionary")
bot.load_extension(f"cogs.reminder")

try:
  bot.run(os.environ['STELLATOKEN'])
except:
  bot.run(os.environ['stellatoken'])
bot.close()