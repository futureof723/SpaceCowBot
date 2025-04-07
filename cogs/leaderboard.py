"""
Discord bot leaderboard extension.
This module provides a leaderboard system that retrieves and displays
the top users based on study points stored in a SQLite database.
"""

import discord
from discord.ext import commands
import sqlite3
import logging

class Leaderboard(commands.Cog):
    """
    A Cog that manages the study points leaderboard.

    This cog fetches the top users from the database and displays them in a
    Discord embed. It handles errors gracefully and formats the leaderboard
    in an easy-to-read format using Discord's rich embed features.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        conn (sqlite3.Connection): The SQLite database connection.
        c (sqlite3.Cursor): The database cursor for executing queries.
        logger (logging.Logger): Logger for error reporting.
    """

    def __init__(self, bot):
        """
        Initialize the Leaderboard cog and establish a database connection.

        Args:
            bot (commands.Bot): The Discord bot instance this cog is attached to.
        """
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)

    def cog_unload(self):
        """
        Perform cleanup when the cog is unloaded.

        Ensures that pending changes to the database are saved and
        the connection is properly closed to prevent resource leaks.

        Returns:
            None
        """
        self.conn.commit()
        self.conn.close()

    @commands.command(help="Show the leaderboard of top study point earners.")
    async def leaderboard(self, ctx):
        """
        Display the top 10 users with the highest study points.

        Fetches and formats user ranking from the database, and sends
        a styled embed message listing the top 10 users and their points.

        Args:
            ctx (commands.Context): The context in which the command was called.

        Returns:
            None

        Error Handling:
            - Catches database errors and reports them to the logger.
            - Handles missing or unresolvable user IDs.
        """
        try:
            # Retrieve the top 10 users from the study_points table
            self.c.execute('SELECT user_id, points FROM study_points ORDER BY points DESC LIMIT 10')
            results = self.c.fetchall()

            # If no results were found, notify the user
            if not results:
                await ctx.send("No study points have been earned yet!")
                return

            # Create the embed that will display the leaderboard
            embed = discord.Embed(
                title="🏆 Study Leaderboard",
                description="Here are the top 10 study point earners:",
                color=discord.Color.gold()
            )
            embed.set_footer(text="Keep studying hard to climb the leaderboard!")
            embed.set_thumbnail(url="https://example.com/leaderboard-icon.png")  # Replace with actual image if available

            # Add each user to the leaderboard embed
            for i, (user_id, points) in enumerate(results, start=1):
                try:
                    user = await self.bot.fetch_user(user_id)
                    embed.add_field(
                        name=f"{i}. {user.name}",
                        value=f"{points} points",
                        inline=False
                    )
                except discord.NotFound:
                    # If the user can't be found (e.g. left server), show as unknown
                    embed.add_field(
                        name=f"{i}. Unknown User",
                        value=f"{points} points",
                        inline=False
                    )
                except Exception as e:
                    # Log any unexpected user fetch errors
                    self.logger.error(f"Error while fetching user data: {e}")
                    embed.add_field(
                        name=f"{i}. Error fetching user",
                        value=f"{points} points",
                        inline=False
                    )

            # Send the formatted leaderboard to the channel
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            # Log and report any database access issues
            self.logger.error(f"Database error while fetching leaderboard: {e}")
            await ctx.send("Sorry, there was an error retrieving the leaderboard. Try again later.")

# Setup function to load the cog
async def setup(bot):
    """
    Setup function to add the Leaderboard cog to the bot.

    This function is called by discord.py when the extension is loaded.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    await bot.add_cog(Leaderboard(bot))
