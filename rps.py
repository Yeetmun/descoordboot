import discord
from discord.ext import commands, tasks
from discord.commands import slash_command
import traceback
import time
import json
import random
import asyncio

players = []

def find_win(game):
    print(game)
    if game[1] == "Rock" and game[3] == "Scissors":
        return 1
    elif game[1] == "Paper" and game[3] == "Rock":
        return 1
    elif game[1] == "Scissors" and game[3] == "Paper":
        return 1
    elif game[1] == game[3]:
        return -1
    else:
        return 3

def rps_embed(players, winner, bot):
    try:
        choicew = players[winner]
        choicel = players[winner - 2]
        if bot and not winner:
            embed = discord.Embed(title = f"{players[0]} vs. Random Number Generator", description = f"**{players[0]}** Choose your weapon!")
            return embed
        elif bot and winner:
            if winner == 1:
                embed = discord.Embed(title = f"{players[0]} vs. Random Number Generator", description = f"**You won using {choicew}!** \nThe Random Number Generator chose {choicel}", color = 0x0ced48)
                return embed
            elif winner == 3:
                embed = discord.Embed(title = f"{players[0]} vs. Random Number Generator", description = f"**You LOST, how could you let this happen?** \nThe Generator chose {choicew} which absolutely obliterated your puny {choicel} \nget good smh", color = 0xed100c)
                embed.set_footer(text = "You're bad")
                return embed
            else:
                embed = discord.Embed(title = f"{players[0]} vs. Random Number Generator", description = f"**It's a tie!** \nYou both chose {choicew}", color = 0x707070)
                return embed
        else:
            if winner == 1:
                embed = discord.Embed(color = 0xffffff)
    except:
        traceback.print_exc()

class human_rps(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view = self)

class bot_rps(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view = self)

    @discord.ui.button(emoji = "🪨", style = discord.ButtonStyle.blurple)
    async def press_rock(self, button, interaction):

        for child in self.children:
            child.disabled = True
        for list in players:
            if str(interaction.user) in list:
                list[list.index(str(interaction.user)) + 1] = "Rock"
                await interaction.response.edit_message(content = "", embed = rps_embed(list, find_win(list), True), view = self)
                players.remove(list)
                break

    @discord.ui.button(emoji = "📃", style = discord.ButtonStyle.blurple)
    async def press_paper(self, button, interaction):
        for child in self.children:
            child.disabled = True
        for list in players:
            if str(interaction.user) in list:
                list[list.index(str(interaction.user)) + 1] = "Paper"
                await interaction.response.edit_message(content = "", embed = rps_embed(list, find_win(list), True), view = self)
                players.remove(list)
                break
    
    @discord.ui.button(emoji = "✂️", style = discord.ButtonStyle.blurple)
    async def press_scissor(self, button, interaction):
        for child in self.children:
            child.disabled = True
        for list in players:
            if str(interaction.user) in list:
                list[list.index(str(interaction.user)) + 1] = "Scissors"
                await interaction.response.edit_message(content = "", embed = rps_embed(list, find_win(list), True), view = self)
                players.remove(list)
                break

    @discord.ui.button(label = "Abandon game (coward)", style = discord.ButtonStyle.red)
    async def destroy(self, button, interaction):
        for child in self.children:
            child.disabled = True
        for list in players:
            if str(interaction.user) in list:
                players.remove(list)
                break
        await interaction.response.edit_message(content = "You abandoned a game against a bot! What a coward! Be ashamed of yourself.", view = self)


class rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description = "play rock paper scissors with a friend! (or bot)", help = "play rock paper scissors with a friend! Or a bot if you have no friends, to do this just do `_rps bot`")
    async def rps(self, ctx, user):
        try:
            if user == "bot" or user == "<@735365871723085864>":
                bot_choice = random.randrange(1,4)
                if bot_choice == 1:
                    bot_choice = "Rock"
                elif bot_choice == 2:
                    bot_choice = "Paper"
                else:
                    bot_choice = "Scissors"
                
                print(bot_choice)
                await ctx.respond("Choose your weapon!", view = bot_rps(timeout = 30))
                players.append([str(ctx.author), "E", "B", bot_choice])
            elif " " in user:
                await ctx.respond("I don't know how to do multi-way rock paper scissors, ping one person only please.")
            else:
                spaghetti = await self.bot.fetch_user(user[2:len(user)-1])
                if spaghetti.bot:
                    await ctx.respond("That's a bot, they don't know how rock paper scissors works.")
                else:
                    await ctx.respond("God damn fucking had to rewrite the whole god damn file gonna go fucking kms why do ephemerals have to be this hard fucking hell AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                    players.append([ctx.author.id, "E", ctx.message.mentions[0].id, "E"])
        except Exception as e:
            await ctx.send(e)
            traceback.print_exc()

def setup(bot): 
    bot.add_cog(rps(bot))




'''
class rps_challenge(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view = self)
    
    @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green)
    async def accept(self, button, interaction):
        for child in self.children:
            child.disabled = True
        for list in players:
            if interaction.user.id in list:
                names = [interaction.client.get_user(interaction.user.id).display_name, interaction.client.get_user(list[list.index(interaction.user.id) - 2]).display_name]
                break
        await interaction.response.edit_message(content = f"Challenge accepted! \n **{names[1]}** is choosing...", view = rps_button)

    
    @discord.ui.button(label = "Decline", style = discord.ButtonStyle.red)
    async def decline(self, button, interaction):
        for child in self.children:
            child.disabled = True
        for list in players:
            if interaction.user.id in list:
                challenger = list[list.index(interaction.user.id) - 2]
                challenged = interaction.client.get_user(list[list.index(interaction.user.id)]).display_name
                await interaction.response.edit_message(view = self)
                await interaction.channel.send(f"<@{challenger}>, {challenged} declined your rock paper scissors challenge!")
                del list
                break
            
        

class rps_button(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view = self)
        
    @discord.ui.button(emoji = "🪨", style = discord.ButtonStyle.blurple)
    async def press_rock(self, button, interaction):
        
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message("You chose rock!", view = self)
        for list in players:
            if interaction.user in list:
                list[list.index(interaction.user) + 1] = "R"
                break

    @discord.ui.button(emoji = "📃", style = discord.ButtonStyle.blurple)
    async def press_paper(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message("You chose paper!", view = self)
        for list in players:
            if interaction.user in list:
                list[list.index(interaction.user) + 1] = "P"
                break
    
    @discord.ui.button(emoji = "✂️", style = discord.ButtonStyle.blurple)
    async def press_scissor(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message("You chose scissors!", view = self)
        for list in players:
            if interaction.user in list:
                list[list.index(interaction.user) + 1] = "S"
                break
    
    @discord.ui.button(label = "Abandon game (coward)", style = discord.ButtonStyle.red)
    async def destroy(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content = "You abandoned the game, **coward**", view = self)
        for list in players:
            if interaction.user in list:
                list[list.index(interaction.user) + 1] = "A"
                break



class minigames(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def update(self):
        for list in players:
            pass
            #apply logic later

    @commands.command(help = "play rock paper scissors with a friend!")
    async def rps(self, ctx):
        try:
            if len(ctx.message.mentions) < 1:
                await ctx.send("I don't know how to do multi-way rock paper scissors, ping one person only please.")
            elif ctx.message.mentions[0].bot:
                await ctx.send("That's a bot, they don't know how rock paper scissors works.")
            else:
                await ctx.send("paine au chocolat")
                await ctx.send("el test", view = rps_challenge(timeout = 30))
                #await ctx.message.mentions[0].send("el test dos", view = rps_button(timeout = 30))
                players.append([ctx.author.id, "E", ctx.message.mentions[0].id, "E"])
            await ctx.send(ctx.message.author)

        except Exception as e:
            traceback.print_exc()
            await ctx.send(e)
            print(e)
'''