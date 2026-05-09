import os
import logging
from datetime import timedelta
import discord
import dotenv
from discord.ext import commands
from discord import app_commands
import random
import emoji
import platform
import time
import asyncio
from urllib.parse import urlparse
from pathlib import Path
import yt_dlp

dotenv.load_dotenv()

token = os.getenv("discord_token")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

reaction_role_messages = {}

start_time = time.time()

brilliance_count = 0
replied_on_cooldown = False
cooldown_end_time = 0

_safe_emojis = None

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    global brilliance_count, replied_on_cooldown, cooldown_end_time

    if message.author.bot:
        return

    content = message.content
    if len(content) <= 20 and content.lower().strip() == "actually brilliant":
        current_time = time.time()

        if current_time < cooldown_end_time:
            if not replied_on_cooldown:
                replied_on_cooldown = True
                await message.reply("im on cooldown for a bit, dont want the mods removing me for spam")
            return

        url = "https://cdn.discordapp.com/attachments/1466849815194505525/1499113206688383037/actuallybriliant-kirk.png?ex=69f98c38&is=69f83ab8&hm=f93ad4a5a6c5787f0e65e42735c96cfbdb8afb2af3693578f7475f86aafefd1c"
        await message.reply(url)
        brilliance_count += 1

        if brilliance_count >= 3:
            cooldown_end_time = current_time + 10
            brilliance_count = 0
            replied_on_cooldown = False

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1466850499604254740)
    if not channel:
        return

    member_count = member.guild.member_count

    embed = discord.Embed(
        title=f"Welcome {member.display_name}!",
        description=f"Welcome {member.mention} to **{member.guild.name}**!\nYou are the **{member_count}th** member!",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.display_avatar.url)

    await channel.send(
        content=f"Welcome {member.mention} to **{member.guild.name}**! You are the {member_count}th member!",
        embed=embed
    )

SYNC_ROLE_IDS = {
    1480054058210562110,
    1480053527509471375,
    1480056423000838145,
    1466855469325750547
}

@bot.tree.command(name="sync", description="syncs slash commands")
async def sync(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("server only.", ephemeral=True)
        return

    if not any(role.id in SYNC_ROLE_IDS for role in interaction.user.roles):
        await interaction.response.send_message("you don't have permission to use this.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    synced = await bot.tree.sync()
    await interaction.followup.send(f"synced {len(synced)} commands.", ephemeral=True)

@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
    link = "https://imgur.com/a/NrympkO.gif"
    gifembed = discord.Embed(title="test", color=discord.Color.blue())
    gifembed.set_image(url=link)
    await interaction.response.send_message(embed=gifembed)

@bot.tree.command(name="emote", description="luna breaks it down")
@app_commands.choices(emote=[
    app_commands.Choice(name="Dance of Ice and Fire", value="Dance_of_Ice_and_Fire"),
    app_commands.Choice(name="Frosty Fortress", value="Frosty_Fortress"),
    app_commands.Choice(name="Cocoa Conjuring", value="Cocoa_Conjuring"),
    app_commands.Choice(name="Disco", value="Disco"),
    app_commands.Choice(name="Cyber Tunes", value="Cyber_Tunes"),
    app_commands.Choice(name="Rehearsal Rhythm", value="Rehearsal_Rhythm"),
    app_commands.Choice(name="Little Oopsie", value="Little_Oopsie"),
    app_commands.Choice(name="Default", value="Default"),
    app_commands.Choice(name="BRAIN BLAST", value="BRAIN_BLAST"),
    app_commands.Choice(name="Take A Seat", value="Take_A_Seat")
])
async def emote(interaction: discord.Interaction, emote: app_commands.Choice[str]):
    emotes = {
        "Dance_of_Ice_and_Fire": "https://static.wikia.nocookie.net/marvel-rivals/images/d/dc/Luna_Snow_Emote_-_Dance_of_Ice_and_Fire_Full.mp4",
        "Frosty_Fortress": "https://static.wikia.nocookie.net/marvel-rivals/images/2/26/Luna_Snow_Emote_-_Frosty_Fortress_Full.mp4",
        "Cocoa_Conjuring": "https://static.wikia.nocookie.net/marvel-rivals/images/3/3a/Luna_Snow_Emote_-_Cocoa_Conjuring_Full.mp4",
        "Disco": "https://static.wikia.nocookie.net/marvel-rivals/images/e/eb/Luna_Snow_Emote_-_Disco_Anniversary_Full.mp4",
        "Cyber_Tunes": "https://static.wikia.nocookie.net/marvel-rivals/images/9/95/Luna_Snow_Emote_-_Cyber_Tunes_Full.mp4",
        "Rehearsal_Rhythm": "https://static.wikia.nocookie.net/marvel-rivals/images/3/3a/Luna_Snow_Emote_-_Rehearsal_Rhythm_Full.mp4",
        "Little_Oopsie": "https://static.wikia.nocookie.net/marvel-rivals/images/1/1b/Luna_Snow_Emote_-_Little_Oopsie_Full.mp4",
        "Default": "https://static.wikia.nocookie.net/marvel-rivals/images/0/00/Luna_Snow_Emote_-_DEFAULT_Full.mp4",
        "BRAIN_BLAST": "https://static.wikia.nocookie.net/marvel-rivals/images/e/ed/Luna_Snow_Emote_-_BRAIN_BLAST_Full.mp4",
        "Take_A_Seat": "https://static.wikia.nocookie.net/marvel-rivals/images/e/ed/Luna_Snow_Emote_-_Take_A_Seat_Full.mp4",
        "ballin":"https://cdn.discordapp.com/attachments/1466849815194505525/1502761690574360586/image.png?ex=6a00e362&is=69ff91e2&hm=0c069f1051fc6aff79c8bf148cfd84e443caf3df849b4a1900b315b6181baf29"
    }

    lines = {
        "Dance_of_Ice_and_Fire": "i love you!",
        "Frosty_Fortress": "im making my own one after my teammates couldnt push dracula's one in comp",
        "Cocoa_Conjuring": "yummy",
        "Disco": "소문 겨벼!",
        "Cyber_Tunes": "ooh yeah!",
        "Rehearsal_Rhythm": "im breaking it down baby",
        "Little_Oopsie": "'no clue what to make this line' - devan",
        "Default": "hi!",
        "BRAIN_BLAST": "'no clue what to make this line' - devan",
        "Take_A_Seat": "I've been standing for so long!",
        "ballin": "LEBRONNN",
    }

    await interaction.response.send_message(f"[{lines[emote.value]}]({emotes[emote.value]})")

@bot.tree.command(name="lie-detect", description="determines whether a message is true or not")
async def lie_detect(interaction: discord.Interaction, statement: str = ""):
    if not statement.strip():
        await interaction.response.send_message("What lie do you want me to detect? If you showered today~ 💅(include a message)")
        return

    if random.choice([True, False]):
        await interaction.response.send_message(f"'{statement}', is definitely true!")
    else:
        await interaction.response.send_message(f"'{statement}', is a lie, shall i freeze the evidence?")

def get_safe_emojis():
    global _safe_emojis
    if _safe_emojis is None:
        _safe_emojis = [e for e in emoji.EMOJI_DATA if len(e) <= 2]
    return _safe_emojis

@bot.tree.command(name="role", description="sends a reaction role message")
@app_commands.describe(roles="roles NOT to include, separated by commas")
async def role(interaction: discord.Interaction, roles: str = ""):
    if interaction.guild is None:
        await interaction.response.send_message("this only works in a server", ephemeral=True)
        return

    excluded_ids = []
    for item in roles.split(","):
        item = item.strip()
        if not item:
            continue
        if item.startswith("<@&") and item.endswith(">"):
            excluded_ids.append(int(item[3:-1]))
        else:
            found = discord.utils.get(interaction.guild.roles, name=item)
            if found:
                excluded_ids.append(found.id)

    allowed_roles = [
        r for r in interaction.guild.roles
        if not r.is_default() and not r.managed and r.id not in excluded_ids
    ]

    server_emojis = [str(e) for e in interaction.guild.emojis]
    normal_emojis = get_safe_emojis()
    emojis = list(set(server_emojis + normal_emojis))
    random.shuffle(emojis)

    if len(allowed_roles) > len(emojis):
        await interaction.response.send_message("not enough emojis", ephemeral=True)
        return

    CHUNK_SIZE = 20
    role_emoji_pairs = list(zip(allowed_roles, emojis))
    chunks = [role_emoji_pairs[i:i + CHUNK_SIZE] for i in range(0, len(role_emoji_pairs), CHUNK_SIZE)]

    await interaction.response.send_message(f"Preparing to send {len(chunks)} reaction role message(s)...", ephemeral=True)

    for i, chunk in enumerate(chunks):
        embed = discord.Embed(
            title=f"Reaction Roles" + (f" (Part {i + 1})" if len(chunks) > 1 else ""),
            description="React below to get a role.",
            color=discord.Color.blue()
        )

        role_map = {}
        lines = []

        for role_obj, emoji_obj in chunk:
            lines.append(f"{emoji_obj} — {role_obj.mention}")
            role_map[str(emoji_obj)] = role_obj.id

        embed.description = "\n".join(lines)

        try:
            msg = await interaction.channel.send(embed=embed)
            reaction_role_messages[msg.id] = role_map

            for emoji_obj in role_map:
                try:
                    await msg.add_reaction(emoji_obj)
                except:
                    pass
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to send messages here.", ephemeral=True)
            break

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot or reaction.message.id not in reaction_role_messages:
        return

    role_id = reaction_role_messages[reaction.message.id].get(str(reaction.emoji))
    role_obj = reaction.message.guild.get_role(role_id)
    member = reaction.message.guild.get_member(user.id)

    if role_obj and member:
        await member.add_roles(role_obj)

@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot or reaction.message.id not in reaction_role_messages:
        return

    role_id = reaction_role_messages[reaction.message.id].get(str(reaction.emoji))
    role_obj = reaction.message.guild.get_role(role_id)
    member = reaction.message.guild.get_member(user.id)

    if role_obj and member:
        await member.remove_roles(role_obj)

music_queues = {}

YTDL_OPTIONS = {
    "format": "bestaudio[abr<=128]/bestaudio/best",
    "quiet": True,
    "noplaylist": True,
    "default_search": "ytsearch1"
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

def get_queue(guild_id):
    return music_queues.setdefault(guild_id, [])

async def get_song(query):
    def extract():
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]
            return {
                "title": info.get("title", "Unknown title"),
                "url": info["url"],
                "webpage_url": info.get("webpage_url", query)
            }
    return await asyncio.to_thread(extract)

async def play_next(guild):
    queue = get_queue(guild.id)
    vc = guild.voice_client

    if not vc or not queue:
        return

    song = queue.pop(0)

    def after_playing(error):
        if error:
            print("Player error:", error)
        asyncio.run_coroutine_threadsafe(play_next(guild), bot.loop)

    vc.play(discord.FFmpegPCMAudio(song["url"], **FFMPEG_OPTIONS), after=after_playing)

@bot.tree.command(name="play", description="adds music to the queue")
@app_commands.describe(query="song name or yt-dlp supported url")
async def play(interaction: discord.Interaction, query: str):
    if not interaction.user.voice:
        await interaction.response.send_message("Join a voice channel first.")
        return

    await interaction.response.defer()

    vc = interaction.guild.voice_client or await interaction.user.voice.channel.connect(timeout=10.0)

    try:
        song = await get_song(query)
        queue = get_queue(interaction.guild.id)
        queue.append(song)

        if vc.is_playing() or vc.is_paused():
            await interaction.followup.send(f"Added to queue: **{song['title']}**\nPosition: `{len(queue)}`")
        else:
            await interaction.followup.send(f"Now playing: **{song['title']}**")
            await play_next(interaction.guild)
    except Exception as e:
        await interaction.followup.send(f"yt-dlp couldn't play that: `{type(e).__name__}: {e}`")

@bot.tree.command(name="queue", description="shows the queue")
async def queue_cmd(interaction: discord.Interaction):
    queue = get_queue(interaction.guild.id)
    if not queue:
        await interaction.response.send_message("The queue is empty.")
        return
    await interaction.response.send_message("\n".join(f"`{i}.` {s['title']}" for i, s in enumerate(queue, 1)))

@bot.tree.command(name="remove", description="removes a song from queue")
@app_commands.describe(index="queue index")
async def remove(interaction: discord.Interaction, index: int):
    queue = get_queue(interaction.guild.id)
    if index < 1 or index > len(queue):
        await interaction.response.send_message("That queue index doesn't exist.")
        return
    song = queue.pop(index - 1)
    await interaction.response.send_message(f"Removed: **{song['title']}**")

@bot.tree.command(name="skip", description="skips the current song")
async def skip(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc or not vc.is_playing():
        await interaction.response.send_message("Nothing is playing.")
        return
    vc.stop()
    await interaction.response.send_message("Skipped.")

@bot.tree.command(name="clear", description="clears the queue")
async def clear(interaction: discord.Interaction):
    get_queue(interaction.guild.id).clear()
    await interaction.response.send_message("Queue cleared.")

@bot.tree.command(name="pause", description="pauses the current song")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc or not vc.is_playing():
        await interaction.response.send_message("Nothing is playing.")
        return
    vc.pause()
    await interaction.response.send_message("Paused.")

@bot.tree.command(name="resume", description="resumes the current song")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc or not vc.is_paused():
        await interaction.response.send_message("Nothing is paused.")
        return
    vc.resume()
    await interaction.response.send_message("Resumed.")

@bot.tree.command(name="leave", description="Ends the concert :(")
async def leave(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc:
        await interaction.response.send_message("I'm not in a voice channel.")
        return
    get_queue(interaction.guild.id).clear()
    await vc.disconnect()
    await interaction.response.send_message("It was a good concert!")

@bot.tree.command(name="status", description="shows the bot status")
async def status(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        uptime = int(time.time() - start_time)
        hours, rem = divmod(uptime, 3600)
        minutes, seconds = divmod(rem, 60)

        guilds = []
        users = 0
        for guild in bot.guilds:
            guilds.append(f"{guild.name}\n")
            users += guild.member_count or 0

        latency = round(bot.latency * 1000)

        vc = interaction.guild.voice_client if interaction.guild else None
        voice_status = "Not connected"
        if vc:
            voice_status = f"Connected to {vc.channel.name}"
            if vc.is_playing():
                voice_status += " | Playing"
            elif vc.is_paused():
                voice_status += " | Paused"
            else:
                voice_status += " | Idle"

        embed = discord.Embed(
            title="Luna Bot Status",
            description="Hmph~ system check complete.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Bot", value=f"{bot.user}", inline=True)
        embed.add_field(name="Latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
        embed.add_field(name="Servers", value="".join(guilds) or "None", inline=True)
        embed.add_field(name="people i know!", value=str(users), inline=True)
        embed.add_field(name="Commands", value=str(len(bot.tree.get_commands())), inline=True)

        queue_len = len(get_queue(interaction.guild.id)) if interaction.guild else 0
        embed.add_field(name="Music", value=f"Queue: {queue_len}", inline=True)
        embed.add_field(name="Voice", value=voice_status, inline=False)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="OS", value=platform.system(), inline=True)
        embed.add_field(
            name="Intents",
            value=(
                f"Message Content: {bot.intents.message_content}\n"
                f"Members: {bot.intents.members}\n"
                f"Voice States: {bot.intents.voice_states}"
            ),
            inline=False
        )

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"status crashed: `{type(e).__name__}: {e}`")
        raise

bot.run(token, log_handler=handler, log_level=logging.INFO)
