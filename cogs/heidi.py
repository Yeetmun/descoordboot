import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, option
import random
import asyncio

class heidi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    heidi = discord.SlashCommandGroup("heidi", "Various things Heidi has asked for")
    guesung = heidi.create_subgroup("guesung", "Various Guesung pictures Heidi demands I add or else I get murdered")
    v = heidi.create_subgroup("v", "Pictures of V from BTS (I think)")
    felix = heidi.create_subgroup("felix", "Pictures of Felix from SKZ")
    minji = heidi.create_subgroup("minji", "Pictures of Minji (whoever they are)")
    lesserafim = heidi.create_subgroup("lesserafim", "Pictures of Lesserafim (who tf are they)")
    blackpink = heidi.create_subgroup("blackpink", "Pictures of blackpink (idk man)")
    nayeon = heidi.create_subgroup("nayeon", "Pictures of Nayeon (who tf are these people)")
    gidle = heidi.create_subgroup("gidle", "Pictures of (G)I-dle (help)")
    jeans = heidi.create_subgroup("jeans", "Pictures of New Jeans (wtf even is that name)")

    @guesung.command(description = "chained by the soul to the will of Heidi")
    async def soccer(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1050624687643824238/unknown.png")

    @guesung.command(description = "Captain... I'm tired")
    async def soccer2(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/1015095527592964096/1054908410849669120/optimize.png")

    @guesung.command(description = "bound by the hand of Heidi")
    async def shirtless(self, ctx):
        if random.randrange(0,501) == 250:
            msg = await ctx.respond("https://media.discordapp.net/attachments/1044471389396144148/1045161635507081237/4164AF86-1478-47EC-8340-52AB2FC48470.jpg?width=890&height=1187")
            msg = await msg.original_response()
            await asyncio.sleep(2.5)
            await msg.delete()
        else:
            await ctx.respond("https://cdn.discordapp.com/attachments/913175848138473543/1054401243918901339/IMG_0969.png")
    
    @guesung.command(description = "there's rope here")
    async def shirtless2(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1055883426466631700/IMG_1006.png?width=548&height=1186")
    
    @v.command(description = "help I'm unpaid")
    async def portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054555387115864064/IMG_0974.jpg?width=680&height=1185")
    
    @felix.command(description = "Please I have friends to care for (actually I don't but whatever)")
    async def portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054555387405279332/IMG_0975.jpg?width=667&height=1185")
    
    @minji.command(description = "Reduced to this, thankless job")
    async def portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054927656812019772/220812-MINJI-NEW-JEANS-documents-4.png?width=790&height=1185")
    
    @lesserafim.command(description = "I just want to be useful")
    async def group_portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054928492963311637/OIP.png")
    
    @blackpink.command(description  = "why does nobody care about me ;-;")
    async def group_portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054928839991631963/AGF-l78bj315XBwm8s56Qi3D3oCUOul_YjWHY8LnWQs900-c-k-c0xffffffff-no-rj-mo.png")
    
    @nayeon.command(description = ":(")
    async def portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054938755275948052/Z.png")
    
    @gidle.command(description = "pain")
    async def group_portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054974548535169024/288037296000201.png")
    
    @gidle.command(description = "nothing but pain")
    async def group_portrait2(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/913175848138473543/1054974733545918484/GIDLE-I-love-Publicity-Photo-2022-billboard-1548.jpg")
    
    @jeans.command(description = "kill me please")
    async def group_portrait(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/9131758481384735343/1073300006041301132/IMG_1498.jpg")

def setup(bot):
    bot.add_cog(heidi(bot))

