import asyncio
import aiofiles
import discord
from discord.ext import commands
import hostbot 
from hostbot import keep_alive

import asyncio
import praw
import random




reddit = praw.Reddit(client_id = "lYjD6I6YFiaLLw",
                     client_secret = "T8ZS-R8yjfBwvgsFK48di9wPQW3_sA",
                     username = "prawpythondiscordbot",   
                     password = "python123",
                     user_agent = "pythonpraw")

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
                break 
    print(f"{bot.user.name} is ready.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="everyone"))

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
    
    if msg.content == "forby":
        forby = msg.content
        await msg.channel.send(str(forby+" is gae"))

    if '@' == msg.content[0] and 'e' == msg.content[-1]:
        em = discord.Embed(title="stop pinging!! :anger:", color=discord.Colour.dark_purple())
        em.set_image(url='https://media1.tenor.com/images/13cf3dabb07b449ac3a2fbddc34d51dd/tenor.gif?itemid=16343688')
        await msg.channel.send(embed = em)

    await bot.process_commands(msg)



@bot.command()
async def configure_ticket(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None):
    if msg is None or category is None:
        await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.")
        return

    bot.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id] 

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
        embed = discord.Embed(title="Ticket system Configurations", color=discord.Colour.dark_purple())
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

    em = discord.Embed(title = name, color=discord.Colour.dark_purple())

    em.set_image(url = url)

    await ctx.send(embed = em)
        
@bot.command()
@commands.has_permissions(kick_members=True)
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            em = discord.Embed(title = ":white_check_mark:"  '"' + args + '" sent to: '  + target.name, color = discord.Colour.dark_purple())
            await ctx.channel.send(embed=em)

        except:
            emb = discord.Embed(title = ':x: could not dm the given user', description = '*this could be beacause the user has their dms closed*', color = discord.Colour.dark_purple())
            await ctx.channel.send(embed = emb)    
    else:
        embed = discord.Embed(title = ':x: wrong syntax', description = '*use .help dm to view the syntax*', color = discord.Colour.dark_purple())
        await ctx.channel.send(embed=embed)



bot.load_extension('cogs.events')
bot.load_extension('cogs.Help')
bot.load_extension('cogs.admin')
bot.load_extension('cogs.misc')
keep_alive()
bot.run("Your bot token")
