"""
Discord bot extension for administrative commands.
This module provides functionality for server administrators to configure bot settings.
"""

from discord.ext import commands
import sqlite3
import logging

# Setup logger for error handling and debugging
logger = logging.getLogger(__name__)

# Create a connection to the SQLite database
# Note: SQLite operations are synchronous and may block the event loop
conn = sqlite3.connect('study_points.db')
c = conn.cursor()


class Admin(commands.Cog):
    """
    A Cog providing administrative commands for bot configuration.

    This cog contains commands that should only be accessible to server administrators,
    allowing them to configure various aspects of the bot's functionality.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
    """

    def __init__(self, bot):
        """
        Initialize the Admin cog.

        Args:
            bot (commands.Bot): The Discord bot instance this cog is attached to.
        """
        self.bot = bot

    @commands.command(help="(Admin) Set this channel to receive automatic daily tips.")
    @commands.has_permissions(administrator=True)
    async def settipchannel(self, ctx):
        """
        Set the current channel to receive daily study tips.

        This command stores the current channel's ID in the database settings table
        with the key 'daily_tip_channel'. The bot will use this channel for posting
        automated daily study tips.

        Args:
            ctx (commands.Context): The invocation context containing information
                                  about where the command was called.

        Returns:
            None: Feedback is sent directly to the Discord channel.

        Raises:
            sqlite3.Error: If there's an issue with the database operation.

        Note:
            This command requires administrator permissions to use.
        """
        try:
            # Set the current channel ID in the settings table in the database
            # REPLACE works like INSERT but will update existing entries with the same key
            c.execute("REPLACE INTO settings (key, value) VALUES (?, ?)",
                      ('daily_tip_channel', str(ctx.channel.id)))

            # Commit the changes to the database
            # Warning: This is a synchronous operation that could block the bot
            conn.commit()

            # Send confirmation message to the channel
            await ctx.send("🤠 This here channel's now set for daily tips, partner!")
        except sqlite3.Error as e:
            # Log the error for debugging purposes
            logger.error(f"Database error while setting tip channel: {e}")

            # Send a user-friendly error message
            await ctx.send("Sorry, there was an error setting the tip channel. Try again later.")


# Setup function for discord.py 2.0+ (needs to be async)
async def setup(bot):
    """
    Setup function to add the Admin cog to the bot.

    This function is called by Discord.py when the extension is loaded.
    In discord.py 2.0+, this function must be async and use 'await'.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    await bot.add_cog(Admin(bot))  # Using await as required in discord.py 2.0+