import asyncio
import aiofiles
import discord
from discord.ext import commands
import asyncio
import praw
import random




reddit = praw.Reddit(client_id = "client id",
                     client_secret = "client secret",
                     username = "reddit username",   
                     password = "reddit password",
                     user_agent = "user agent")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = ".", intents=intents)
bot.warnings = {}
bot.ticket_configs = {}
bot.sniped_messages = {}
bot.remove_command("help")


@bot.event 
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)



@bot.event
async def on_ready():
    async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
        pass

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]
            break

        for guild in bot.guilds:
         bot.warnings[guild.id] = {}
        
        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 

    print(f"{bot.user.name} is ready.")

@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.id != bot.user.id and str(payload.emoji) == u"\U0001F3AB":
        msg_id, channel_id, category_id = bot.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = bot.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)

            ticket_channel = await category.create_text_channel(f"ticket-{payload.member.display_name}", topic=f"A ticket for {payload.member.display_name}.", permission_synced=True)
            
            await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

            message = await channel.fetch_message(msg_id)
            await message.remove_reaction(payload.emoji, payload.member)

            await ticket_channel.send(f"{payload.member.mention} Thank you for creating a ticket! Use **'-close'** to close your ticket.")

            try:
                await bot.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member and m.content == "-close", timeout=3600)

            except asyncio.TimeoutError:
                await ticket_channel.delete()

            else:
                await ticket_channel.delete()

@bot.event
async def on_message(msg):
    if ":" == msg.content[0] and ":" == msg.content[-1]:
        emoji_name = msg.content[1:-1]
        for emoji in msg.guild.emojis:
            if emoji_name == emoji.name:
                await msg.channel.send(str(emoji))
                await msg.delete()
                break
    
    await bot.process_commands(msg)
    
@bot.event 
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("Get some perms XD")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Use the correct syntax :|")
    else:
        raise error

@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use .help <command> for more information on the command!",color = ctx.author.color )

    em.add_field(name = "Moderation", value = "kick,ban,warn,unmute,mute,configure_ticket, warnings,clear,unban")
    em.add_field(name = "Miscellaneous", value = "whois,expose,dm,dm_all,meme")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)



@bot.command()
async def configure_ticket(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None):
    if msg is None or category is None:
        await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.")
        return

    bot.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id] # this resets the configuration

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("ticket_configs.txt", mode="w") as file:
        await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)
                
    await msg.add_reaction(u"\U0001F3AB")
    await ctx.channel.send("Succesfully configured the ticket system.")

@bot.command()
async def ticket_config(ctx):
    try: 
        msg_id, channel_id, category_id = bot.ticket_configs[ctx.guild.id]

    except KeyError:
        await ctx.channel.send("You have not configured the ticket system yet.")

    else: 
        embed = discord.Embed(title="Ticket system Configurations", color=discord.Color.dark_purple())
        embed.description =f"**Reaction Message ID** : {msg_id}\n"
        embed.description += f"**Ticket Category ID : {category_id}\n\n"

        await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
        
    if reason is None:
        return await ctx.send("Please provide a reason for warning this user.")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = bot.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

@bot.command()
@commands.has_permissions(administrator=True)
async def warnings(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.dark_purple())
    try:
        i = 1
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: 
        await ctx.send("This user has no warnings.")

@bot.command()
async def expose(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)


@bot.command()
async def meme(ctx, subred = "memes"):
    subreddit = reddit.subreddit(subred)
    all_subs = []

    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title = name)

    em.set_image(url = url)

    await ctx.send(embed = em)
        
@bot.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount)

@bot.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason given"):
    await ctx.send(member.name + " has been kicked from the server, Because:"+reason)
    await member.kick(reason=reason)

@bot.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason given"):
    try:
        await ctx.send(member.name + " has been banned from the server, Because:"+reason)
    except:
        await member.ban(reason=reason)

    await member.kick(reason=reason)

@bot.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):

            await ctx.guild.unban(user)
            await ctx.send(member_name +" has been unbanned!")
            return

    await ctx.send(member+" was not found")

@bot.command(aliases=['m'])
@commands.has_permissions(kick_members=True)
async def mute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(814102587245985792)

    await member.add_roles(muted_role)

    await ctx.send(member.mention + " has been muted")

@bot.command(aliases=['um'])
@commands.has_permissions(kick_members=True)
async def unmute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(814102587245985792)

    await member.remove_roles(muted_role)

    await ctx.send(member.mention + " has been unmuted")

@bot.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx,member : discord.Member):
    embed = discord.Embed(title = member.name , description = member.mention, color = discord.Colour.red())
    embed.add_field(name = "ID", value= member.id , inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' sent to: " + target.name)

        except:
            await ctx.channel.send("Sorry...I Couldn't dm the given user.")
        

    else:
        await ctx.channel.send("You didn't provide a user's id and/or a message.")

@bot.command() 
@commands.has_permissions(kick_members=True)
async def dm_all(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members 
        for member in members:
            try:
                await member.send(args)
                print("'" + args + "' sent to: " + member.name)

            except:
                print("Couldn't send '" + args + "' to " + member.name)

    else:
        await ctx.channel.send("You didn't provide the required arguments.")

@help.command()
async def Kick(ctx):

    em = discord.Embed(title = "kick", description = "Kicks a member from the server", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".kick <member> [reason]")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em) 

@help.command()
async def Ban(ctx):

    em = discord.Embed(title = "ban", description = "Bans a member from the server", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".ban <member> [reason]")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em) 

@help.command()
async def Clear(ctx):

    em = discord.Embed(title = "clear", description = "Clears a certain amount of messages", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".clear <amount of messages>")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em) 

@help.command()
async def Warn(ctx):

    em = discord.Embed(title = "Warn", description = "Gives the member a warning", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".warn <member>")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em) 

@help.command()
async def Warnings(ctx):

    em = discord.Embed(title = "Warn", description = "Shows the warnings given to a member", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".warn <member>")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em) 

@help.command()
async def Configure_ticket(ctx):

    em = discord.Embed(title = "Configure_ticket", description = "Configures the ticket system", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".configure_ticket <message id> <category id>")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)

@help.command()
async def Mute(ctx):

    em = discord.Embed(title = "Mute", description = "Mutes a member", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".mute <member> [reason]")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)

@help.command()
async def Unmute(ctx):

    em = discord.Embed(title = "Unmute", description = "Unmutes a member", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".unmute <member>")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)

@help.command()
async def Unban(ctx):

    em = discord.Embed(title = "Unbans", description = "Unbans a member from the server", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".unban <member id>")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)

@help.command()
async def Whois(ctx):

    em = discord.Embed(title = "Whois", description = "Gives information about a member", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".whois <member>")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)

@help.command()
async def Dm(ctx):

    em = discord.Embed(title = "Dm", description = "Dms a single member", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".dm <member id> [context of dm]")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)

@help.command()
async def Dm_all(ctx):

    em = discord.Embed(title = "Dm_all", description = "Dms every member in the server", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = ".dm_all [context of dm]")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/733639347621855232/829739720811610173/WhatsApp_Image_2021-04-08_at_8.38.39_PM.jpg")

    await ctx.send(embed = em)


bot.run("Your bot token")
