import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Setup logger for bot activities
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Ensure that logging level is set to capture info logs
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Initialize bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs dynamically
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')
    await load_cogs()  # This should remain async

async def load_cogs():
    logger.info("Starting to load cogs...")  # Debugging: Start loading cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                cog_name = f'cogs.{filename[:-3]}'
                logger.info(f"Attempting to load cog: {cog_name}")
                await bot.load_extension(cog_name)  # Now await loading the extension
                logger.info(f'Loaded cog: {filename}')
            except Exception as e:
                logger.error(f'Error loading cog {filename}: {e}')
                logger.debug(f"Full error traceback for cog {filename}: {e.__traceback__}")  # Debugging: Full traceback of the error
                continue  # Continue loading other cogs even if one fails

# 🚀 Start the bot
logger.info("Bot starting...")
bot.run(DISCORD_TOKEN)
