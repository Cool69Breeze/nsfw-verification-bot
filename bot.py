import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_NAME = os.getenv("ROLE_NAME")
EMOJI = os.getenv("EMOJI")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != CHANNEL_ID or str(payload.emoji.name) != EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    member = guild.get_member(payload.user_id)
    if not member or member.bot:
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    if role:
        await member.add_roles(role)
        print(f"Added role to {member.display_name}")

bot.run(TOKEN)
