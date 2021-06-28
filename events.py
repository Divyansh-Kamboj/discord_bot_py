from discord.ext import commands
import discord

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener() 
    async def on_command_error(self, ctx,error):
        if isinstance(error,commands.MissingPermissions):
            em = discord.Embed(title = ":joy: get some perms nerd", color = discord.Colour.dark_purple())
            await ctx.send(embed = em) 
        elif isinstance(error,commands.MissingRequiredArgument):
            em = discord.Embed(title = ":x: use the correct syntax", description = "use .help to look at the syntax!", color = discord.Colour.dark_purple() )
            await ctx.send(embed = em)
        else:
            raise error


def setup(bot):
    bot.add_cog(events(bot))

