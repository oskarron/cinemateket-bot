# run_bot_once.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from main import (
    compare,
)  # Make sure Python can find main.py in parent dir

# Load environment variables from .env
load_dotenv()

# --- Bot setup ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with the actual text channel ID where you want to post
CHANNEL_ID = 1209161223547916401


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Fetch channel (use fetch_channel to avoid caching issues)
    channel = await bot.fetch_channel(CHANNEL_ID)

    # Run scraper and get results
    matches = compare()  # synchronous scraper
    if not matches:
        results = "No matches today 🎥"

    # Send results to Discord
    await channel.send(f"**Daily recommendations:**\n{results}")

    # Shut down the bot after posting
    await bot.close()


if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError("No DISCORD_BOT_TOKEN in environment!")

    bot.run(TOKEN)
