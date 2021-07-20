import discord
import json
from discord.ext import commands

client = commands.Bot(command_prefix="-", case_insensitive=True)

@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")

@client.command(aliases=['perms'])
async def permissions(ctx):
	await ctx.send("```Permissions: \n Ban = Ban Members \n kick = Kick Members \n clear = Manage Messages \n dm = Manage Messages \n announce = administrator \n mute/unmute = Manage Messages \n reactrole = Manage Roles \n poll = Manage Messages```")

@client.command()
async def uwu(ctx):
    await ctx.send("**UwU**")

@client.command()
async def support(ctx):
    await ctx.send("**https://discord.gg/ApPBGuKnxh**")

@client.command(aliases=['cl','delete'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount)

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No Reason Provided"):
    await ctx.send(member.name + " was kicked from " + ctx.guild.name)
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No Reason Provided"):
    await ctx.send(member.name + " was banned from " + ctx.guild.name)
    await member.ban(reason=reason)

@client.command()
async def owo(ctx):
    await ctx.send("**OwO**")


@client.command()
async def ping(ctx):
    await ctx.channel.send(f"Returned in {round(client.latency * 1000)} ms")

@commands.command()
async def join(self, ctx):
    if ctx.author.voice is None:
        return await ctx.send("You are not connected to a voice channel, please connect to the channel you want the bot to join.")

    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

    await ctx.author.voice.channel.connect()

@commands.command()
async def leave(self, ctx):
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()

    await ctx.send("I am not connected to a voice channel.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def dm(ctx, user: discord.User,*, msg):
    await ctx.send("Message Sent")
    await user.send(f'{msg}')

@client.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: discord.TextChannel,*, msg):
    await ctx.send('Message Sent')
    await channel.send(f'{msg}')

@client.command()
@commands.has_permissions(manage_messages = True)
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

@client.command()
@commands.has_permissions(administrator=True)
async def embed(ctx, name, channel: discord.TextChannel,*,msg):
    user = ctx.author

    emb = discord.Embed(title=f"{name}", description=f"{msg}", colour=user.colour)
    msg = await channel.send(embed=emb)



@client.command(aliases=['whois', 'about'])
async def userinfo(ctx, member : discord.Member):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {member.mention}", colour=member.colour)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="NAME", value=member.name, inline=True)
    embed.add_field(name="NICKNAME", value=member.nick, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="STATUS", value=member.status, inline=True)
    embed.add_field(name="TOP ROLE", value=member.top_role.name, inline=True)
    await ctx.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):
    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name,
                          'role_id': role.id,
                          'emoji': emoji,
                          'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

client.run("ODUxMjAxMjg5OTAzNDA3MTQ0.YL00-g.bJmvbvp-6HOrjj4a60lXRg3fwOQ")