from discord.colour import Colour
from discord.ext import commands
import discord

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['c'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx,amount=2):
        await ctx.channel.purge(limit = amount)
        em = discord.Embed(title = '**messages have been purged :white_check_mark:**', color = discord.Colour.dark_purple())
        await ctx.send(embed = em)

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx,member : discord.Member,*,reason= "No reason given"):
            em = discord.Embed(title = member.name +" has been kicked from the server :white_check_mark:", description = reason)
            await ctx.send(embed = em)
            await member.kick(reason=reason)

    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx,member : discord.Member,*,reason= "No reason given"):
        try:
            em = discord.Embed(title = member.name + " has been banned from the server :white_check_mark:", description = reason)
            await ctx.send(embed = em)
        except:
            await member.ban(reason=reason)
            await member.kick(reason=reason)


    @commands.command(aliases=['ub'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,*,member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for banned_entry in banned_users:
            user = banned_entry.user

            if(user.name, user.discriminator)==(member_name,member_disc):

                await ctx.guild.unban(user)
                em = discord.Embed(title = member_name +' has been unbanned :white_check_mark:', color = discord.Colour.dark_purple())
                await ctx.send(embed = em)
                return
        eme = discord.Embed(title = member + ' was not found :x:')
        await ctx.send(embed = eme)

    @commands.command(aliases=['m'])
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx,member : discord.Member):
        muted_role = ctx.guild.get_role(852432593969610754)

        await member.add_roles(muted_role)
        
        em = discord.Embed(title = member.name + ' has been unmuted :white_check_mark:', color = discord.Colour.dark_purple())
        await ctx.send(embed = em)

    @commands.command(aliases=['um'])
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx,member : discord.Member):
        muted_role = ctx.guild.get_role(852432593969610754)

        await member.remove_roles(muted_role)
        
        em = discord.Embed(title = member.name + " has been umuted :white_check_mark:", color = discord.Colour.dark_purple())
        await ctx.send(embed = em)



def setup(bot):
    bot.add_cog(admin(bot))