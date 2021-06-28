from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title = "Help", description = "Use .help <command> for more information on the command!",color = discord.Colour.dark_purple())

        em.add_field(name = "Moderation", value = "kick,ban,warn,unmute,mute,configure_ticket, warnings,clear,unban")
        em.add_field(name = "Miscellaneous", value = "whois,expose,dm,dm_all,meme")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em)

    @help.command()
    async def kick(self, ctx):

        em = discord.Embed(title = "kick", description = "Kicks a member from the server", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".kick <member> [reason]")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em) 

    @help.command()
    async def ban(self, ctx):

        em = discord.Embed(title = "ban", description = "Bans a member from the server", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".ban <member> [reason]")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em) 

    @help.command()
    async def clear(self, ctx):

        em = discord.Embed(title = "clear", description = "Clears a certain amount of messages", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".clear <amount of messages>")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em) 

    @help.command()
    async def warn(self, ctx):

        em = discord.Embed(title = "Warn", description = "Gives the member a warning", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".warn <member>")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em) 

    @help.command()
    async def warnings(self, ctx):

        em = discord.Embed(title = "Warn", description = "Shows the warnings given to a member", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".warn <member>")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em) 

    @help.command()
    async def configure_ticket(self, ctx):

        em = discord.Embed(title = "Configure_ticket", description = "Configures the ticket system", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".configure_ticket <message id> <category id>")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em)

    @help.command()
    async def mute(self, ctx):

        em = discord.Embed(title = "Mute", description = "Mutes a member", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".mute <member> [reason]")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em)

    @help.command()
    async def unmute(self, ctx):

        em = discord.Embed(title = "Unmute", description = "Unmutes a member", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".unmute <member>")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em)

    @help.command()
    async def unban(self, ctx):

        em = discord.Embed(title = "Unbans", description = "Unbans a member from the server", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".unban <member id>")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em)

    @help.command()
    async def whois(self, ctx):

        em = discord.Embed(title = "Whois", description = "Gives information about a member", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".whois <member>")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em)

    @help.command()
    async def dm(self, ctx):

        em = discord.Embed(title = "Dm", description = "Dms a single member", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".dm <member id> [context of dm]")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

        await ctx.send(embed = em)

    @help.command()
    async def dm_all(self, ctx):

        em = discord.Embed(title = "Dm_all", description = "Dms every member in the server", color = discord.Colour.dark_purple())

        em.add_field(name = "**Syntax**", value = ".dm_all [context of dm]")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")
        em.set_footer(text='*Note: this command can only be used by the creator of this bot (fragz)*')
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Help(bot))

