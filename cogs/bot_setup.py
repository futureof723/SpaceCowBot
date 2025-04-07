"""
Discord bot setup extension.
This module provides the base configuration for the Discord bot,
handling environment variables and initial setup.
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
# This allows sensitive data like tokens to be stored outside the code
load_dotenv()

# Get the Discord bot token from environment variables
# This token is required to authenticate the bot with Discord's API
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Setup logger for bot activities
# This creates a logger that can be used to track bot events and errors
logger = logging.getLogger(__name__)


class BotSetup(commands.Cog):
    """
    A Cog that handles the initial setup and configuration of the Discord bot.

    This cog currently serves as a container for bot initialization code but can
    be expanded to include startup tasks, configuration checks, and other
    initialization procedures.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
    """

    def __init__(self, bot):
        """
        Initialize the BotSetup cog.

        Args:
            bot (commands.Bot): The Discord bot instance this cog is attached to.

        Note:
            This cog currently doesn't add any commands but could be extended
            to include initialization routines, status checks, or configuration commands.
        """
        self.bot = bot


# Setup function to add the cog to the bot
async def setup(bot):
    """
    Setup function to add the BotSetup cog to the bot.

    This function is called by Discord.py when the extension is loaded.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    await bot.add_cog(BotSetup(bot))