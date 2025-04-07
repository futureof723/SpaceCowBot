"""
Main entry point for the Discord bot.

This script loads environment variables, initializes logging,
sets up bot commands and listeners, and dynamically loads cogs from the `cogs/` directory.
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# === Load environment variables from .env file ===
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# === Set up logger ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Capture INFO-level logs and above

# Stream handler for console output
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Log format: timestamp - log level - message
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# === Configure bot and intents ===
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content (for commands)

# Create bot instance with custom command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """
    Called when the bot successfully connects and is ready.

    Logs the bot's name and attempts to load all cogs dynamically.
    """
    logger.info(f'✅ Logged in as {bot.user.name}')
    await load_cogs()


async def load_cogs():
    """
    Load all Python files in the `cogs/` directory as bot extensions.

    This function looks for `.py` files and attempts to load them as Discord bot extensions.
    It logs both successful and failed cog loads for debugging.
    """
    logger.info("🔧 Starting to load cogs...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                logger.info(f"➡️ Loading cog: {cog_name}")
                await bot.load_extension(cog_name)
                logger.info(f'✅ Successfully loaded cog: {filename}')
            except Exception as e:
                logger.error(f'❌ Error loading cog {filename}: {e}')
                # This debug line can be expanded to use traceback.print_exc() if needed
                continue  # Skip failed cog and continue loading others


# === Start the bot ===
logger.info("🚀 Bot starting up...")
bot.run(DISCORD_TOKEN)
