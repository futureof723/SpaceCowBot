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

# Initialize bot with necessary intents
class BotSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(BotSetup(bot))
