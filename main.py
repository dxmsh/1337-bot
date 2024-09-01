import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import json
import os
import asyncio

with open("config.json", 'r') as f:
    config = json.load(f)
load_dotenv()

PREFIX = config["prefix"]

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

@bot.event
async def on_ready():
    await load()
    print(f"""
-----READY-----
Logged in as: {bot.user.name}
---------------
""")

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and not message.author.bot:
        await message.channel.send(f"Hi <@{message.author.id}>, my prefix is **{PREFIX}**")

async def load():
    print("Loading cogs...")
    await bot.load_extension('jishaku')
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f"Loading {filename}...")
            await bot.load_extension(f"cogs.{filename[:-3]}")
    print("Syncing command tree...")
    await bot.tree.sync()

async def main():
    async with bot:
        await bot.start(os.getenv("BOT_TOKEN"))

asyncio.run(main())
