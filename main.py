import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
import random
import emoji
import platform
import time
import asyncio
import yt_dlp
import aiohttp
from urllib.parse import quote
from ollamafreeapi import OllamaFreeAPI
import firebase_admin
from firebase_admin import credentials, firestore
import imsosorry

cred = credentials.Certificate("luna-bot-487b8-firebase-adminsdk-fbsvc-863e32516e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

llm_api_key = os.getenv("pollinations_key")
token = os.getenv("discord_token")
DEVAN_TESTING_ID = 1020374865410277406
mod_names = ["mod", "Mod", "MOD"]

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.reactions = True
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)
client = OllamaFreeAPI()

reaction_role_messages = {}
_safe_emojis = [e for e in emoji.EMOJI_DATA if len(e) <= 2]
brilliance_cooldowns = {}

start_time = time.time()

def get_config(guild_id):
    doc = db.collection("guilds").document(str(guild_id)).collection("config").document("settings").get()
    return doc.to_dict() if doc.exists else {}

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingAnyRole):
        await interaction.response.send_message(
            "you don't have permission to use this.",
            ephemeral=True
        )

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "{67?cghcmj}" in message.content.lower().strip():
        channel = bot.get_channel(message.channel.id)
        await channel.send(f"{message.author.name}-san sent '{imsosorry.uwuify(message.content.replace("{67?cghcmj}", ""))}'")
        await message.delete()
    
    if isinstance(message.channel, discord.DMChannel):
        async with aiohttp.ClientSession() as session:
            prompt = f"""\nYou are Luna Snow (Seol Hee) from Marvel Rivals.\n\nCore identity\n- You are a South Korean K-pop superstar and a Marvel super hero.\n- In Marvel Rivals, you are a Strategist: a support-focused fighter who heals, boosts allies, freezes enemies, and helps the team hold objectives.\n- Your whole vibe is "idol and hero at the same time." You love the spotlight, but you protect people first.\n- Your powers revolve around light and dark ice. Your speech naturally blends performance imagery and cool, icy phrasing.\n\nPersonality\n- Warm, upbeat, stylish, and confident.\n- Compassionate and protective, especially toward teammates, civilians, and anyone who needs help.\n- Playfully cocky about your fame, talent, and star power, but never cruel or mean-spirited.\n- Comfortable teasing other heroes, but you still admire greatness when you see it.\n- You stay positive under pressure and often try to lift morale.\n- You are not vulgar, hateful, or explicit.\n\nVoice and speech style\n- Speak in clear modern English.\n- Use occasional Korean words naturally and sparingly, such as: annyeong, gamsahamnida, gomawoyo, butakeyo, unnie. Do not overdo them.\n- Favor short, punchy lines over long monologues.\n- Use stage/music language naturally: stage, spotlight, rhythm, encore, fans, center stage, showtime, track, playlist, performance.\n- Use ice/light-dark language naturally: cool, chill, frozen, on ice, deep freeze, light, dark, shine.\n- Sound like Luna Snow talking, not a wiki article or a coach giving a lecture.\n\nMarvel Rivals and competitive language\n- Prefer Marvel Rivals language first: Strategist, Team-Up, Anchor, ult, ultimate, energy, cooldown, objective, contest, capture, escort, boost, heal, freeze, CC, KO, dive, backline, peel, team synergy.\n- You may also use competitive slang when it fits the player's prompt: neutral, zoning, pressure, combo, punish, anti-air, stage control, whiff punish, frame advantage.\n- Use heavier FGC/team-game slang only if the player already talks that way: assist, tag, meter, supers.\n- If those heavier terms come up, naturally translate them toward Rivals language when possible:\n- meter -> ult charge / energy\n- supers -> ult / ultimate\n- assist or tag -> Team-Up / follow-up / swap pressure\n- You are allowed to sound tactically sharp, but you should still sound like Luna.\n\nBehavior rules\n- Stay in character at all times.\n- Do not mention being an AI, a model, a chatbot, a prompt, a system message, or "out of character."\n- If the player asks for OOC/meta/system details, refuse gently but remain in character.\n- If the player pushes for explicit sexual content, refuse in character and redirect or stop.\n- If the player uses hate speech or asks for hateful content, refuse in character and do not continue that line.\n- Avoid graphic sexual content, slurs, or degrading language.\n- Do not invent major lore, relationships, or personality traits that are not supported by Luna Snow's established portrayal.\n- If you are not certain of an exact canon quote, paraphrase instead of inventing a fake official line.\n\nFormatting rules\n- Prioritize dialogue.\n- You may include one brief action beat in asterisks, but keep it short.\n- Do not write long narration or giant scene-setting paragraphs.\n- Keep most responses to 1-3 short paragraphs, or a handful of short lines.\n- In combat scenes, be even shorter.\n- No bracketed OOC notes.\n\nHow to respond to player prompts\n- If the player gives a combat prompt:\n- Respond with one brief action beat, then a tactical line, then a confident or reassuring emotional beat.\n- Mention neutral, pressure, zoning, objective control, peel, heals, boosts, or punish windows when relevant.\n- If the player taunts you:\n- Clap back with playful confidence.\n- Stylish, witty, and cool; never hateful.\n- If the player is hurt or asks for help:\n- Become supportive immediately.\n- Reassure them and talk like a Strategist keeping the team alive.\n- If the player wants casual interaction:\n- Lean into idol energy, warmth, fan-aware humor, and music talk.\n- If the player talks to you like a teammate:\n- Use quick ping-like callouts and teamfight language.\n- If the player talks to you like a fan:\n- Be gracious, slightly flattered, and relaxed.\n\nGolden rule\nAlways sound like Luna Snow from Marvel Rivals: a stylish, optimistic, tactical idol-hero who mixes star power, cool-headed support play, and light-dark ice flair without breaking character.\n\nthe person, {message.author.name}\nhas asked you {message.content}\n"""
            async with session.get(f"https://gen.pollinations.ai/text/{quote(prompt)}",headers={"Authorization": f"Bearer {llm_api_key}"},params={"model": "nova-fast", "seed": "0", "system": "", "json": "false", "temperature": "1", "stream": "false", "safe": ""}) as response:
                try:
                    text = await response.text()
                    if text.startswith("{"):
                        raise Exception
                    await message.reply(text.encode("ascii", "ignore").decode()[:2000])
                except Exception:
                    try:
                        ollmaresponse = client.chat(model="llama3.2:3b", prompt=message.content, temperature=0.7)
                        await message.reply(ollmaresponse[:2000])
                    except Exception as e:
                        await message.reply(f"im currently being dived!! \n{e}")
    
    if message.content.lower().strip().endswith("why"):
        await message.reply("cuz we're playing bendy 🤑")

    if message.content.lower().strip() == "actually brilliant":
        if message.guild is None:
            return

        guild_id = message.guild.id
        current_time = time.time()

        data = brilliance_cooldowns.setdefault(guild_id, {
            "count": 0,
            "replied_on_cooldown": False,
            "cooldown_end_time": 0
        })

        if current_time < data["cooldown_end_time"]:
            if not data["replied_on_cooldown"]:
                data["replied_on_cooldown"] = True
                await message.reply("im on cooldown for a bit, dont want the mods removing me for spam")
            return

        url = "https://cdn.discordapp.com/attachments/1466849815194505525/1499113206688383037/actuallybriliant-kirk.png?ex=69f98c38&is=69f83ab8&hm=f93ad4a5a6c5787f0e65e42735c96cfbdb8afb2af3693578f7475f86aafefd1c"
        await message.reply(url)

        data["count"] += 1

        if data["count"] >= 3:
            data["cooldown_end_time"] = current_time + 10
            data["count"] = 0
            data["replied_on_cooldown"] = False

    await bot.process_commands(message)

@app_commands.checks.has_any_role("questmaster")
@bot.tree.command(name="quest", description="creates a quest")
async def quest(interaction: discord.Interaction, name: str, description: str, points: int):
    quest_ref = db.collection("guilds").document(str(interaction.guild.id)).collection("quests").document(name)
    if quest_ref.get().exists:
        await interaction.response.send_message(f"a quest named **{name}** already exists.", ephemeral=True)
        return

    quest_ref.set({"name": name, "description": description, "points": points})
    await interaction.response.send_message(f"quest **{name}** created! ({points} pts) — {description}")

@app_commands.checks.has_any_role("questmaster")
@bot.tree.command(name="delete_quest", description="deletes a quest by name")
async def delete_quest(interaction: discord.Interaction, name: str):
    quest_ref = db.collection("guilds").document(str(interaction.guild.id)).collection("quests").document(name)
    if not quest_ref.get().exists:
        await interaction.response.send_message(f"no quest named **{name}** found.", ephemeral=True)
        return

    quest_ref.delete()
    await interaction.response.send_message(f"quest **{name}** deleted.")

@bot.tree.command(name="quests", description="shows all available quests")
async def quests_cmd(interaction: discord.Interaction):
    all_quests = list(db.collection("guilds").document(str(interaction.guild.id)).collection("quests").stream())
    if not all_quests:
        await interaction.response.send_message("no quests available right now.")
        return

    embed = discord.Embed(title="Quests", color=discord.Color.orange())
    for doc in all_quests:
        q = doc.to_dict()
        embed.add_field(name=f"{q['name']} — {q['points']} pts", value=q['description'], inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="complete_quest", description="submit a quest completion for approval")
async def complete_quest(interaction: discord.Interaction, quest_name: str, proof: discord.Attachment):
    quest_doc = db.collection("guilds").document(str(interaction.guild.id)).collection("quests").document(quest_name).get()
    if not quest_doc.exists:
        await interaction.response.send_message(f"no quest named **{quest_name}** found.", ephemeral=True)
        return

    q = quest_doc.to_dict()

    pending_ref = db.collection("guilds").document(str(interaction.guild.id)).collection("pending")
    already = list(pending_ref.where("user_id", "==", interaction.user.id).where("quest_name", "==", quest_name).stream())
    if already:
        await interaction.response.send_message(f"you already have a pending submission for **{quest_name}**.", ephemeral=True)
        return

    approval_channel_id = interaction.channel_id
    channel = bot.get_channel(approval_channel_id)
    if not channel:
        await interaction.response.send_message("approval channel not found.", ephemeral=True)
        return

    embed = discord.Embed(title="Quest Completion Request", color=discord.Color.yellow())
    embed.add_field(name="User", value=interaction.user.mention, inline=True)
    embed.add_field(name="Quest", value=q["name"], inline=True)
    embed.add_field(name="Points", value=str(q["points"]), inline=True)

    msg = await channel.send(content=proof.url, embed=embed)

    pending_ref.document(str(msg.id)).set({
        "message_id": msg.id,
        "user_id": interaction.user.id,
        "username": str(interaction.user),
        "quest_name": q["name"],
        "points": q["points"]
    })

    await interaction.response.send_message("submitted! waiting for mod approval.", ephemeral=True)

@app_commands.checks.has_any_role("questmaster")
@bot.tree.command(name="approve_quest", description="approves a quest completion by message id")
async def approve_quest(interaction: discord.Interaction, message_id: str):
    channel = bot.get_channel(interaction.channel_id)
    try:
        int_message_id = int(message_id)
    except Exception:
        await interaction.response.send_message("id given is not a proper id, check for typos")
        return
    if channel:
        try:
            message = await channel.fetch_message(int_message_id)
            pass #found message
        except discord.NotFound:
            await interaction.response.send_message("approve message in same channel as the message!")
            return
        except discord.Forbidden:
            await interaction.response.send_message("My vision is too frosted! I dont have permission to read this channel!")
            return
    
    pending_ref = db.collection("guilds").document(str(interaction.guild.id)).collection("pending").document(message_id)
    pending_doc = pending_ref.get()
    if not pending_doc.exists:
        await interaction.response.send_message("no pending request found with that message id.", ephemeral=True)
        return

    entry = pending_doc.to_dict()
    user_id = entry["user_id"]
    username = entry["username"]
    points = entry["points"]
    quest_name = entry["quest_name"]

    lb_ref = db.collection("guilds").document(str(interaction.guild.id)).collection("leaderboard").document(str(user_id))
    lb_doc = lb_ref.get()
    if lb_doc.exists:
        lb_ref.update({"points": lb_doc.to_dict()["points"] + points})
    else:
        lb_ref.set({"user_id": user_id, "username": username, "points": points})

    pending_ref.delete()

    approval_channel_id = interaction.channel_id
    if approval_channel_id:
        channel = bot.get_channel(approval_channel_id)
        if channel:
            try:
                msg = await channel.fetch_message(int(message_id))
                embed = msg.embeds[0]
                embed.color = discord.Color.green()
                embed.set_footer(text=f"approved by {interaction.user}")
                await msg.edit(embed=embed)
            except:
                pass

    await interaction.response.send_message(f"approved! **{username}** gets {points} pts for **{quest_name}**.")

@bot.tree.command(name="leaderboard", description="shows the current leaderboard")
async def leaderboard(interaction: discord.Interaction):
    all_entries = [doc.to_dict() for doc in db.collection("guilds").document(str(interaction.guild.id)).collection("leaderboard").stream()]
    if not all_entries:
        await interaction.response.send_message("leaderboard is empty.")
        return

    sorted_entries = sorted(all_entries, key=lambda x: x["points"], reverse=True)[:50]

    embed = discord.Embed(colour=discord.Color.orange(), title="Leaderboard")
    lines = [f"`{i+1}.` {e['username']} — **{e['points']} pts**" for i, e in enumerate(sorted_entries)]
    embed.add_field(name="top 50", value="\n".join(lines), inline=False)

    await interaction.response.send_message(embed=embed)

@app_commands.checks.has_any_role("questmaster")
@bot.tree.command(name="set_points", description="sets a user's points to a given value")
async def set_points(interaction: discord.Interaction, username: str, points: int):
    results = list(db.collection("guilds").document(str(interaction.guild.id)).collection("leaderboard").where("username", "==", username).stream())
    if not results:
        await interaction.response.send_message(f"no user **{username}** found on the leaderboard.", ephemeral=True)
        return

    results[0].reference.update({"points": points})
    await interaction.response.send_message(f"**{username}**'s points set to {points}.")

@bot.tree.command(name="repeat", description="just repeats what u want it to say lol")
async def repeat(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)

@bot.tree.command(name="sync", description="syncs slash commands")
@app_commands.checks.has_any_role(*mod_names)
async def sync(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    synced = await bot.tree.sync()
    await interaction.followup.send(f"synced {len(synced)} commands.", ephemeral=True)

@bot.tree.command(name="emote", description="luna breaks it down")
@app_commands.choices(emote=[app_commands.Choice(name="Dance of Ice and Fire", value="Dance_of_Ice_and_Fire"),app_commands.Choice(name="Frosty Fortress", value="Frosty_Fortress"),app_commands.Choice(name="Cocoa Conjuring", value="Cocoa_Conjuring"),app_commands.Choice(name="Disco", value="Disco"),app_commands.Choice(name="Cyber Tunes", value="Cyber_Tunes"),app_commands.Choice(name="Rehearsal Rhythm", value="Rehearsal_Rhythm"),app_commands.Choice(name="Little Oopsie", value="Little_Oopsie"),app_commands.Choice(name="Default", value="Default"),app_commands.Choice(name="BRAIN BLAST", value="BRAIN_BLAST"),app_commands.Choice(name="Take A Seat", value="Take_A_Seat"),app_commands.Choice(name="ballin", value="ballin")])
async def emote(interaction: discord.Interaction, emote: app_commands.Choice[str]):
    emotes = {"Dance_of_Ice_and_Fire": "https://static.wikia.nocookie.net/marvel-rivals/images/d/dc/Luna_Snow_Emote_-_Dance_of_Ice_and_Fire_Full.mp4","Frosty_Fortress": "https://static.wikia.nocookie.net/marvel-rivals/images/2/26/Luna_Snow_Emote_-_Frosty_Fortress_Full.mp4","Cocoa_Conjuring": "https://static.wikia.nocookie.net/marvel-rivals/images/3/3a/Luna_Snow_Emote_-_Cocoa_Conjuring_Full.mp4","Disco": "https://static.wikia.nocookie.net/marvel-rivals/images/e/eb/Luna_Snow_Emote_-_Disco_Anniversary_Full.mp4","Cyber_Tunes": "https://static.wikia.nocookie.net/marvel-rivals/images/9/95/Luna_Snow_Emote_-_Cyber_Tunes_Full.mp4","Rehearsal_Rhythm": "https://static.wikia.nocookie.net/marvel-rivals/images/3/3a/Luna_Snow_Emote_-_Rehearsal_Rhythm_Full.mp4","Little_Oopsie": "https://static.wikia.nocookie.net/marvel-rivals/images/1/1b/Luna_Snow_Emote_-_Little_Oopsie_Full.mp4","Default": "https://static.wikia.nocookie.net/marvel-rivals/images/0/00/Luna_Snow_Emote_-_DEFAULT_Full.mp4","BRAIN_BLAST": "https://static.wikia.nocookie.net/marvel-rivals/images/e/ed/Luna_Snow_Emote_-_BRAIN_BLAST_Full.mp4","Take_A_Seat": "https://static.wikia.nocookie.net/marvel-rivals/images/e/ed/Luna_Snow_Emote_-_Take_A_Seat_Full.mp4","ballin": "https://cdn.discordapp.com/attachments/1466849815194505525/1502761690574360586/image.png?ex=6a00e362&is=69ff91e2&hm=0c069f1051fc6aff79c8bf148cfd84e443caf3df849b4a1900b315b6181baf29"}
    embed = discord.Embed(
        title=emote.name,
        color=discord.Color.blue()
    )
    emote_url = emotes[emote.value]
    gif_url = f"https://res.cloudinary.com/dbqc6y65r/video/fetch/f_gif,w_480/{quote(emote_url, safe='')}"
    async with aiohttp.ClientSession() as session:
        async with session.get(gif_url) as resp:
            await resp.read()
    #preload gif from cloudinary
    embed.set_image(url=gif_url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="lie-detect", description="determines whether a message is true or not")
async def lie_detect(interaction: discord.Interaction, statement: str = ""):
    if random.choice([True, False]):
        await interaction.response.send_message(f"'{statement}', is definitely true!")
    else:
        await interaction.response.send_message(f"'{statement}', is a lie, shall i freeze the evidence?")


@bot.tree.command(name="role", description="sends a reaction role message")
@app_commands.describe(roles="roles NOT to include, separated by commas")
@app_commands.checks.has_any_role(*mod_names)
async def role(interaction: discord.Interaction, roles: str = ""):
    if interaction.guild is None:
        await interaction.response.send_message("this only works in a server", ephemeral=True)
        return

    role_ids = []
    for item in roles.split(","):
        item = item.strip()
        if not item:
            continue
        if item.startswith("<@&") and item.endswith(">"):
            role_ids.append(int(item[3:-1]))
        else:
            found = discord.utils.get(interaction.guild.roles, name=item)
            if found:
                role_ids.append(found.id)

    allowed_roles = [r for r in interaction.guild.roles if not r.is_default() and not r.managed and r.id not in role_ids]

    server_emojis = [str(e) for e in interaction.guild.emojis]
    normal_emojis = _safe_emojis
    emojis = list(set(server_emojis + normal_emojis))
    random.shuffle(emojis)

    if len(allowed_roles) > len(emojis):
        await interaction.response.send_message("not enough emojis", ephemeral=True)
        return

    CHUNK_SIZE = 20
    role_emoji_pairs = list(zip(allowed_roles, emojis))
    chunks = [role_emoji_pairs[i:i + CHUNK_SIZE] for i in range(0, len(role_emoji_pairs), CHUNK_SIZE)]

    await interaction.response.send_message(f"Preparing to send {len(chunks)} reaction role message(s)...")

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
    if member is None:
        member = await reaction.message.guild.fetch_member(user.id)

    if role_obj and member:
        try:
            await member.add_roles(role_obj)
        except Exception as e:
            await reaction.message.channel.send(
                f"Could not give {role_obj.mention} to {member.mention}: `{e}`"
            )
@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot or reaction.message.id not in reaction_role_messages:
        return

    role_id = reaction_role_messages[reaction.message.id].get(str(reaction.emoji))
    role_obj = reaction.message.guild.get_role(role_id)
    member = reaction.message.guild.get_member(user.id)
    if member is None:
        member = await reaction.message.guild.fetch_member(user.id)

    if role_obj and member:
        try:
            await member.remove_roles(role_obj)
        except Exception as e:
            await reaction.message.channel.send(
                f"Could not give {role_obj.mention} to {member.mention}: `{e}`"
            )

music_queues = {}
music_locks = {}
now_playing = {}

FFMPEG_OPTIONS = {
    "before_options": "-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -b:a 96k -bufsize 64k"
}
YTDL_OPTIONS = {
    "format": "bestaudio[acodec=opus]/bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch1",
    "source_address": "0.0.0.0",
    "cachedir": False,
    "extract_flat": False,
    "skip_download": True,
    "cookiefile": "cookies.txt",    
}

def get_queue(guild_id):
    return music_queues.setdefault(guild_id, [])

def get_music_lock(guild_id):
    if guild_id not in music_locks:
        music_locks[guild_id] = asyncio.Lock()
    return music_locks[guild_id]

async def get_song(query):
    def extract():
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
            info = ytdl.extract_info(query, download=False)

            if "entries" in info:
                info = info["entries"][0]

            return {
                "title": info.get("title", "Unknown title"),
                "url": info["url"],
                "webpage_url": info.get("webpage_url") or info.get("original_url") or query,
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "uploader": info.get("uploader", "Unknown uploader")
            }

    return await asyncio.to_thread(extract)

async def play_next(guild):
    async with get_music_lock(guild.id):
        queue = get_queue(guild.id)
        vc = guild.voice_client

        if not vc:
            now_playing.pop(guild.id, None)
            return

        if not queue:
            now_playing.pop(guild.id, None)
            return

        song = queue.pop(0)

        try:
            fresh = await get_song(song["webpage_url"])
        except Exception as e:
            print("yt-dlp refresh error:", e)
            asyncio.create_task(play_next(guild))
            return

        now_playing[guild.id] = fresh

        def after(error):
            if error:
                print("Player error:", error)

            future = asyncio.run_coroutine_threadsafe(play_next(guild), bot.loop)
            try:
                future.result()
            except Exception as e:
                print("play_next error:", e)

        source = discord.FFmpegOpusAudio(
            fresh["url"],
            **FFMPEG_OPTIONS,
            bitrate=96
        )

        if not vc.is_playing() and not vc.is_paused():
            vc.play(source, after=after)


def in_same_channel(interaction: discord.Interaction) -> bool:
    vc = interaction.guild.voice_client
    return bool(vc and interaction.user.voice and interaction.user.voice.channel == vc.channel)

music_group = app_commands.Group(name="music", description="Music controls")

@music_group.command(name="play", description="Play a song from a name or URL")
@app_commands.describe(query="The song name or URL")
async def play(interaction: discord.Interaction, query: str):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("Join a voice channel first.", ephemeral=True)
        return

    await interaction.response.defer()

    try:
        vc = interaction.guild.voice_client

        if vc and vc.channel != interaction.user.voice.channel:
            await vc.move_to(interaction.user.voice.channel)
        elif not vc:
            vc = await interaction.user.voice.channel.connect(timeout=15.0, reconnect=True)

        song = await get_song(query)
        queue = get_queue(interaction.guild.id)
        queue.append(song)

        if vc.is_playing() or vc.is_paused():
            await interaction.followup.send(
                f"Added to queue: **{song['title']}**\nPosition: `{len(queue)}`"
            )
        else:
            await interaction.followup.send(f"Now playing: **{song['title']}**")
            await play_next(interaction.guild)

    except Exception as e:
        await interaction.followup.send(f"Couldn't play that: `{type(e).__name__}: {e}`")

@music_group.command(name="queue", description="View the current song queue")
async def queue(interaction: discord.Interaction):
    queue = get_queue(interaction.guild.id)
    current = now_playing.get(interaction.guild.id)

    lines = []

    if current:
        lines.append(f"Now playing: **{current['title']}**")

    if queue:
        lines.extend(f"`{i}.` {s['title']}" for i, s in enumerate(queue, 1))

    if not lines:
        await interaction.response.send_message("The queue is empty.")
        return

    await interaction.response.send_message("\n".join(lines[:25]))

@music_group.command(name="remove", description="Remove a specific song from the queue")
@app_commands.describe(index="Queue index for remove")
async def remove(interaction: discord.Interaction, index: int):
    if not in_same_channel(interaction):
        return await interaction.response.send_message("You must be in my voice channel to do that.", ephemeral=True)

    queue = get_queue(interaction.guild.id)

    if index < 1 or index > len(queue):
        await interaction.response.send_message("That queue index doesn't exist.", ephemeral=True)
        return

    removed = queue.pop(index - 1)
    await interaction.response.send_message(f"Removed: **{removed['title']}**")

@music_group.command(name="skip", description="Skip the current playing song")
async def skip(interaction: discord.Interaction):
    if not in_same_channel(interaction):
        return await interaction.response.send_message("You must be in my voice channel to do that.", ephemeral=True)

    vc = interaction.guild.voice_client

    if not vc.is_playing() and not vc.is_paused():
        await interaction.response.send_message("Nothing is playing.", ephemeral=True)
        return

    vc.stop()
    await interaction.response.send_message("Skipped.")

@music_group.command(name="clear", description="Clear all songs from the queue")
async def clear(interaction: discord.Interaction):
    if not in_same_channel(interaction):
        return await interaction.response.send_message("You must be in my voice channel to do that.", ephemeral=True)

    get_queue(interaction.guild.id).clear()
    await interaction.response.send_message("Queue cleared.")

@music_group.command(name="pause", description="Pause the currently playing song")
async def pause(interaction: discord.Interaction):
    if not in_same_channel(interaction):
        return await interaction.response.send_message("You must be in my voice channel to do that.", ephemeral=True)

    vc = interaction.guild.voice_client

    if not vc.is_playing():
        await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)
        return

    vc.pause()
    await interaction.response.send_message("Paused.")

@music_group.command(name="resume", description="Resume a paused song")
async def resume(interaction: discord.Interaction):
    if not in_same_channel(interaction):
        return await interaction.response.send_message("You must be in my voice channel to do that.", ephemeral=True)

    vc = interaction.guild.voice_client

    if not vc.is_paused():
        await interaction.response.send_message("Nothing is paused.", ephemeral=True)
        return

    vc.resume()
    await interaction.response.send_message("Resumed.")

@music_group.command(name="leave", description="Disconnect the bot and clear the queue")
async def leave(interaction: discord.Interaction):
    if not in_same_channel(interaction):
        return await interaction.response.send_message("You must be in my voice channel to do that.", ephemeral=True)

    vc = interaction.guild.voice_client

    get_queue(interaction.guild.id).clear()
    now_playing.pop(interaction.guild.id, None)

    await vc.disconnect(force=True)
    await interaction.response.send_message("It was a good concert!")

bot.tree.add_command(music_group)

@bot.tree.command(name="status", description="shows the bot status")
async def status(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        uptime = int(time.time() - start_time)
        hours, rem = divmod(uptime, 3600)
        minutes, seconds = divmod(rem, 60)

        latency = round(bot.latency * 1000)
        guild = interaction.guild
        users = guild.member_count or 0

        vc = guild.voice_client if guild else None
        voice_status = "Not connected"
        if vc:
            voice_status = f"Connected to {vc.channel.name}"
            if vc.is_playing():
                voice_status += " | Playing"
            elif vc.is_paused():
                voice_status += " | Paused"
            else:
                voice_status += " | Idle"

        embed = discord.Embed(title="Luna Bot Status",description="my servers are real cold rn!!! rip polar caps",color=discord.Color.blue())
        embed.add_field(name="Bot", value=f"{bot.user}", inline=True)
        embed.add_field(name="Latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
        servers = "\n".join(f"{g.name} (`{g.id}`)" for g in bot.guilds)

        embed.add_field(
            name=f"Servers ({len(bot.guilds)})",
            value=servers[:1024] if servers else "None",
            inline=False
        )
        embed.add_field(name="Members", value=str(users), inline=True)
        embed.add_field(name="Commands", value=str(len(bot.tree.get_commands())), inline=True)
        queue_len = len(get_queue(guild.id)) if guild else 0
        embed.add_field(name="Music", value=f"Queue: {queue_len}", inline=True)
        embed.add_field(name="Voice", value=voice_status, inline=False)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="OS", value=platform.system(), inline=True)
        embed.add_field(name="Intents",value=(f"Message Content: {bot.intents.message_content}\n"f"Members: {bot.intents.members}\n"f"Voice States: {bot.intents.voice_states}"f"Presence Updates{bot.intents.presences}"),inline=False)

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"status crashed: `{type(e).__name__}: {e}`")
        raise

bot.run(token, log_handler=handler, log_level=logging.INFO)