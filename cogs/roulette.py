import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, option
import random
import traceback

games = []

def generate_gun():
    chamber = [0, 0, 0, 0, 0, 0]
    """"
    for i in range(6):
        if 0 == random.randrange(0, 5):
            chamber.append(1)
            length = len(chamber)
            for l in range(6-length):
                chamber.append(0)
            return chamber
        else:
            chamber.append(0)
    chamber[-1] = 1
    """
    chamber[random.randrange(6)] = 1
    return chamber

def gun_embed(game):
    field = [f"<@{user.id}>\n" for user in game["fools"]]
    visualize_gun = []
    embed = discord.Embed(title = "Russian Fucking Roulette!", color = discord.Color.random())
    embed.add_field(name = "**__Players__**", value = ("".join(field)))
    for round in game["gun"]:
        if round == -1:
            visualize_gun.append("🔳")
        elif round == 2:
            visualize_gun.append("🟥")
        else:
            visualize_gun.append("⬜")
    embed.add_field(name = "__Current gun__", value = (" ".join(visualize_gun)))
    return embed

class le_gun(discord.ui.View):
    dead = False
    async def on_timeout(self):
        global games
        for child in self.children:
            child.disabled = True
        roulette_id = self.message.embeds[0].fields[0].value[2:20]
        print(roulette_id)
        for game in games:
            for person in game["fools"]:
                if person.id == roulette_id:
                    del game
                print(person.id)
        await self.message.edit(view = self)

    @discord.ui.button(label = "Pull the Trigger!", style = discord.ButtonStyle.danger)
    async def pull_trigger(self, button, interaction):
        global games
        dead = False
        game = interaction.message.embeds[0].fields
        game = game[0].value[:21][2:-1]
        try:
            for gaem in games:
                for person in gaem["fools"]:
                    if str(game) in str(person.id):
                        game = gaem
                        game_id = games.index(game)
            trig = game["fools"][0]
            if interaction.user.id != trig.id:
                await interaction.response.send_message("***__Not your turn__***", ephemeral = True)
            else:
                for i in game["gun"]:
                    if i == 0 or i == 1:
                        if i == 0:
                            game["gun"][game["gun"].index(0)] = -1
                            game["fools"].append(game["fools"].pop(0))
                            break
                        else:
                            dead = True
                            game["gun"][game["gun"].index(1)] = 2
                            break
                if dead:
                    await interaction.response.edit_message(content = f"**<@{trig.id}> died!**", embed = gun_embed(game))
                    del games[game_id]
                else:
                    await interaction.response.edit_message(content = f"<@{game['fools'][0].id}>'s turn!", embed = gun_embed(game))
        except Exception as e:
            await interaction.response.send_message(content = "Not your game", ephemeral = True)
            traceback.print_exc()
        
    @discord.ui.button(label = "dump data", style = discord.ButtonStyle.green)
    async def debug(self, button, interaction):
        await interaction.response.send_message(f"{games}", ephemeral = True)


class roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description = "die simulator (but randomly)")
    @option(name = "user2", type = discord.Member, required = True)
    @option(name = "user3", type = discord.Member, required = False)
    @option(name = "user4", type = discord.Member, required = False)
    @option(name = "user5", type = discord.Member, required = False)
    @option(name = "user6", type = discord.Member, required = False)
    async def russian_roulette(self, ctx, user2, user3 = None, user4 = None, user5 = None, user6 = None):
        global games
        participants = {"fools": [ctx.author, user2, user3, user4, user5, user6], "gun": generate_gun()}
        participants["fools"] = [user for user in participants["fools"] if user]
        if len(set(participants["fools"])) < len(participants["fools"]):
            await ctx.respond("A person cannot play more than once in a game!")
            return
        if games:
            for challenged in participants["fools"]:
                for round in games:
                    for person in round["fools"]:
                        if challenged.id != person.id:
                            pass
                        else:
                            await ctx.respond("You and/or one or more of the people you challenged are already in a game of russian roulette!")
                            return            
        games.append(participants)
        await ctx.respond(content = f"<@{ctx.author.id}>'s Turn!", embed = gun_embed(participants), view = le_gun(timeout = 120))
    
    @slash_command(description = "sex")
    async def dump(self, ctx):
        await ctx.respond(f"{games}")

def setup(bot):
    bot.add_cog(roulette(bot))
