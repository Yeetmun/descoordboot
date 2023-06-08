import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, option
import wolframalpha as wolf
import traceback
import math

api_key = "8ER9HR-U4YX4KEX2G"
wolfram = wolf.Client(api_key)

def img_embed(link1, link2, prompt):
    result = discord.Embed(title = prompt, color = discord.Color.random())
    result.set_thumbnail(url = link2)
    result.set_image(url = link1)
    return result

def mathify(eq):
    if eq:
        eq = str(eq)
        eq = eq.replace("sqrt", "√")
        eq = eq.replace("integral", "∫ ")
        #print(eq)
        return eq
    else:
        raise Exception

class calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    math = discord.SlashCommandGroup("math", "math things")
    formula = math.create_subgroup("formula", "various math formula solvers")

    @formula.command(description = "Law of Cosines")
    @option(name = "side a", type = int, required = False)
    @option(name = "side b", type = int, required = False)
    @option(name = "side c", type = int, required = False)
    @option(name = "angle opposite a", type = int, required = False)
    @option(name = "angle opposite c", type = int, required = False)
    @option(name = "angle opposite b", type = int, required = False)
    async def law_of_cosines(self, ctx, side_a = None, side_b = None, side_c = None, angle_a = None, angle_b = None, angle_c = None, is_radians = discord.Option(name = "is_radians", description = "Whether or not the angle is in radians", default = "True", choices = ["True", "False"], required = False)):
        if not ((side_a and side_c and angle_b) or (side_b and side_c and angle_a) or (side_a and side_b and angle_c) or (side_a and side_b and side_c)):
            await ctx.respond("Insufficient information, to solve for a side you need the opposite angle, and both of the other side lengths, to solve for angle you need all three side lengths")
            return
        if is_radians == "False":
            angle_a, angle_b, angle_c = angle_a / 57.29577951, angle_b / 57.29577951, angle_c / 57.29577951 
            is_radians = False
        else:
            is_radians = True
        try:
            side_a = round(math.sqrt(side_b**2 + side_c**2 - (2 * side_b * side_c * math.cos(angle_a))) if (side_b and side_c and angle_a) else side_a, 4) if not side_a else side_a
            side_b = round(math.sqrt(side_a**2 + side_c**2 - (2 * side_a * side_c * math.cos(angle_b))) if (side_a and side_c and angle_b) else side_b, 4) if not side_b else side_b
            side_c = round(math.sqrt(side_a**2 + side_b**2 - (2 * side_a * side_b * math.cos(angle_c))) if (side_a and side_b and angle_c) else side_c, 4) if not side_c else side_c
            if is_radians == "False":
                angle_a = round(math.acos((side_b**2 + side_c**2 - side_a**2) / (2 * side_b * side_c)) * 57.29577951, 4) if not angle_a else angle_a
                angle_b = round(math.acos((side_c**2 + side_a**2 - side_b**2) / (2 * side_c * side_a)) * 57.29577951, 4) if not angle_b else angle_b
                angle_c = round(math.acos((side_a**2 + side_b**2 - side_c**2) / (2 * side_a * side_b)) * 57.29577951, 4) if not angle_c else angle_c
            else:
                angle_a = round(math.acos((side_b**2 + side_c**2 - side_a**2) / (2 * side_b * side_c)), 4) if not angle_a else angle_a
                angle_b = round(math.acos((side_c**2 + side_a**2 - side_b**2) / (2 * side_c * side_a)), 4) if not angle_b else angle_b
                angle_c = round(math.acos((side_a**2 + side_b**2 - side_c**2) / (2 * side_a * side_b)), 4) if not angle_c else angle_c
            await ctx.send(f"side a: {side_a} \nside b: {side_b} \nside c: {side_c} \nangle a: {angle_a} \nangle b: {angle_b} \nangle c: {angle_c} \n{'angles are in **radians**' if is_radians else 'angles are in **degrees**'}")
        except Exception as e:
            print(e)
            await ctx.respond("This is not a valid triangle")

    @formula.command(description = "Law of Sines")
    @option(name = "side a", type = int, required = False)
    @option(name = "side b", type = int, required = False)
    @option(name = "side c", type = int, required = False)
    @option(name = "angle opposite a", type = int, required = False)
    @option(name = "angle opposite b", type = int, required = False)
    @option(name = "angle opposite c", type = int, required = False)
    async def law_of_sines(self, ctx, side_a = None, side_b = None, side_c = None, angle_a = None, angle_b = None, angle_c = None, is_radians = discord.Option(name = "is_radians", description = "Whether or not the angle is in radians", default = "True", choices = ["True", "False"], required = False)):
        if not ((side_a and angle_a) or (side_b and angle_b) or (side_c and angle_c)):
            await ctx.respond("Insufficient information, you need at least one side angle pair")
            return
        if not (not side_a and not angle_a) or (not side_b and not angle_a) or (not side_c and not angle_c):
            await ctx.respond("Missing information, you must have data for each side, whether it be angle or side length")
            return
        if is_radians == "False":
            angle_a, angle_b, angle_c = angle_a / 57.29577951, angle_b / 57.29577951, angle_c / 57.29577951    
            is_radians == False
        else:
            is_radians = True
        if side_a and angle_a:
            ratio = side_a/angle_a
            aratio = angle_a/side_a
        elif side_b and angle_b:
            ratio = side_b/angle_b
            aratio = angle_b/side_b
        else:
            ratio = side_c/angle_c
            aratio = angle_c/side_c
        side_a = round(ratio * math.sin(angle_a) if not side_a else side_a, 4) 
        angle_a = round(aratio * side_a if not angle_a else angle_a, 4)
        side_b = round(ratio * math.sin(angle_b) if not side_b else side_b, 4)
        angle_b = round(aratio * side_b if not angle_b else angle_b, 4)
        side_c = round(ratio * math.sin(angle_c) if not angle_c else angle_c, 4)
        angle_c = round(aratio * side_c if not angle_c else angle_c, 4)
        if angle_a * 57.29577951 + angle_b * 57.29577951 + angle_c * 57.29577951 == 180:
            await ctx.respond(f"side a: {side_a} \nside b: {side_b} \nside c: {side_c} \n angle a: {angle_a} \n angle b: {angle_b} \n angle c: {angle_c} \n{'**Angles are in degrees**' if not is_radians else '**Angles are in radians**'}")
        else:
            await ctx.respond("Invalid Triangle")

    @formula.command(description = "Pythagorean Theorem")
    @option(name = "side a", type = int, required = False)
    @option(name = "side b", type = int, required = False)
    @option(name = "side c", type = int, required = False)
    async def pythagorean_thereom(ctx, side_a = None, side_b = None, side_c = None):
        if side_a and side_b:
            result = round(math.sqrt(side_a**2 + side_b**2), 4)
        else:
            result = round(math.sqrt(side_b**2 + side_c**2), 4) if (side_b and side_c) else round(math.sqrt(side_a**2 + side_c**2), 4)
        await ctx.respond("third side: " + result)
    
    @slash_command(description = "do some math")
    async def calc(self, ctx, expression):
        await ctx.defer()
        results = []
        res_obj = None
        result = wolfram.query(expression)
        print("_______________________SPLIT_______________________")
        print(result)

        try:
            for i in result.pod:
                if i["@title"] == "Solutions":
                    res_obj = i
                    print(res_obj)

            for i in res_obj.subpod:
                results.append(mathify(i["plaintext"]))
            #print(result.pod[5].subpod)
            await ctx.respond(", ".join(results))
            #await ctx.respond("brok")
        except:
            try:
                results.append(mathify(next(result.results).text))
                results.append("Approx. " + str(round(float(result.pod[2].subpod["plaintext"][:-3]), 4)))
                await ctx.respond("Results: " + ", ".join(results))
            except:
                try:
                    await ctx.respond("Result: " + mathify(next(result.results).text))
                except:
                    try:
                        await ctx.respond(embed = img_embed(result.pod[1].subpod.img["@src"], result.pod[2].subpod.img["@src"], expression))
                    except:
                        await ctx.respond("Something went wrong, probably an invalid prompt, i'll look into it soon")
                        traceback.print_exc()

def setup(bot):
    bot.add_cog(calculator(bot))
