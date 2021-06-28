from discord.ext import commands
import discord

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['user','info'])
    @commands.has_permissions(kick_members=True)
    async def whois(self, ctx,member : discord.Member):
        embed = discord.Embed(title = member.name , description = member.mention, color = discord.Colour.dark_purple())
        embed.add_field(name = "ID", value= member.id , inline = True)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        em = discord.Embed(title = 'Invite me to your server!!', description = 'https://discord.com/api/oauth2/authorize?client_id=827862289561419836&permissions=8&scope=bot', color = discord.Colour.dark_purple())
    
def setup(bot):
    bot.add_cog(misc(bot))