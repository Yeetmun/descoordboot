import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, option
import datetime
import time as t
import asyncio
import json

nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def time_resolve(time):
    if (not (False if (time.find("s") < time.find("m") or time.find("s") < time.find("h") or time.find("s") < time.find("d")) or (True if time.find("s") == -1 else False) else True) and (False if time.find("m") < time.find("h") or time.find("m") < time.find("d") or (True if time.find("h") == -1 else False) else True) and (False if time.find("h") < time.find("d") and time.find("h") != -1 else True)) or ("d" not in time and "h" not in time and "m" not in time and "s" not in time):
        return -1
    time = time.lower()
    length = 0
    if time.find("d") != -1:
        temp = time[:time.find("d")]
        length += int(temp)*86400
        time = time[time.find("d")+1:]
    if time.find("h") != -1:
        temp = time[:time.find("h")]
        length += int(temp)*3600
        time = time[time.find("h")+1:]
    if time.find("m") != -1:
        temp = time[:time.find("m")]
        length += int(temp)*60
        time = time[time.find("m")+1:]
    if time.find("s") != -1:
        temp = time[:time.find("s")]
        length += int(temp)
    return length

def make_time_nice(date):
    res = ""
    date = date.replace(" ", "")
    if "d" in date:
        temp = date[:date.find("d")]
        if ((any(num in date[date.find("d") - 2] for num in nums)) or date[date.find("d") - 1] != "1"):
            res = res + temp + " days " 
        else:
            res = res + temp + " day "
        date = date[date.find("d") + 1:]
    if "h" in date:
        temp = date[:date.find("h")]
        if ((any(num in date[date.find("h") - 2] for num in nums)) or date[date.find("h") - 1] != "1"):
            res = res + temp + " hours "
        else:
            res = res + temp + " hour "
        date = date[date.find("h") + 1:]
    if "m" in date:
        temp = date[:date.find("m")]
        if ((any(num in date[date.find("m") - 2] for num in nums)) or date[date.find("m") - 1] != "1"):
            res = res + temp + " minutes and"
        else:
            res = res + temp + " minute and "
        date = date[date.find("m") + 1:]
    if "s" in date:
        temp = date[:date.find("s")]
        if ((any(num in date[date.find("s") - 2] for num in nums)) or date[date.find("s") - 1] != "1"):
            res = res + temp + " seconds"
        else:
            res = res + temp + " second"
        date = date[date.find("s") + 1:]
    return res

def create_embed(place, message, time):
    embed = discord.Embed(title = f"{place}", description = message, color = discord.Color.random())
    embed.set_footer(text = f"Set approximately {time} ago")
    return embed

class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timer.start()

    def cog_unload(self):
        self.timer.cancel()

    reminder = discord.SlashCommandGroup("reminder", "Commands group for reminders")

    @reminder.command(description = "Set a reminder for yourself")
    @option(name = "time", description = "add a d, h, m, or s directly after the time, in that order. for example 2h 5s for 2 hours 5 seconds")
    @option(name = "message", description = "the thing you want to be reminded about")
    async def set(self, ctx, time, message):
        if time_resolve(time) == -1:
            await ctx.respond("I won't be parsing that, please put a `d, h, m, or s` (in that order) directly after the amount of that time you want.\nFor example, `2h 5s` for 2 hours 5 seconds")
            return
        if time_resolve(time) < 60:
            await ctx.respond(f"Sure thing, I'll remind you in about {make_time_nice(time)}")
            await asyncio.sleep(time_resolve(time))
            await ctx.author.send(embed = create_embed(f"Reminder set in {ctx.guild}", message, make_time_nice(time)))
            await ctx.channel.send(content = f"<@{ctx.author.id}>", embed = create_embed(f"Reminder set in {ctx.guild}", message, make_time_nice(time)))
            return
        await ctx.respond(f"Sure thing, I'll remind you in about {make_time_nice(time)}")
        file = open("cogs/reminderdata.json", "r+")
        data = json.load(file)
        data.append({"user": ctx.author.id, "message": message, "server": ctx.guild_id, "channel": ctx.channel_id, "time": time, "abstime": time_resolve(time) + round(t.time())})
        data = json.dumps(data)
        file.seek(0)
        file.write(data)
        file.truncate()
    
    @tasks.loop(seconds = 30)
    async def timer(self):
        file = open("cogs/reminderdata.json", "r+")
        data = json.load(file)
        if data:
            for remind in data:
                if (t.time() - remind["abstime"]) >= -15:
                    channel = await self.bot.fetch_channel(remind["channel"])
                    author = await self.bot.get_or_fetch_user(remind["user"])
                    await author.send(embed = create_embed(f"Reminder set in {remind['server']}", remind['message'], make_time_nice(remind['time'])))
                    await channel.send(content = f"<@{remind['user']}>", embed = create_embed(f"Reminder for {author}", remind['message'], make_time_nice(remind['time'])))
                    index = data.index(remind)
                    del data[index]
        data = json.dumps(data)
        file.seek(0)
        file.write(data)
        file.truncate()

def setup(bot):
    bot.add_cog(reminder(bot))
