"""
Discord bot points system extension.
This module allows users to earn and check their study points, which are
stored in a local SQLite database. Admins or authorized users can assign
points to members, encouraging participation and engagement.
"""

import sqlite3
import logging
from discord.ext import commands

# Configure logger for error tracking
logger = logging.getLogger(__name__)


class Points(commands.Cog):
    """
    A Cog that manages study point assignment and tracking.

    This cog handles assigning points to users and allowing users
    to check their current point totals. All point data is stored
    and retrieved using a SQLite database.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        conn (sqlite3.Connection): The SQLite database connection.
        cursor (sqlite3.Cursor): The database cursor for executing queries.
    """

    def __init__(self, bot):
        """
        Initialize the Points cog and establish a database connection.

        Args:
            bot (commands.Bot): The Discord bot instance this cog is attached to.
        """
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params):
        """
        Execute a database query with parameters and handle errors.

        Commits the transaction after successful execution. Rolls back and logs
        the error if an exception occurs.

        Args:
            query (str): The SQL query string to execute.
            params (tuple): Parameters to bind to the SQL query.

        Raises:
            sqlite3.Error: Re-raises the exception after logging it.
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise

    @commands.command(help="Add study points to a user.")
    async def addpoints(self, ctx, user: commands.UserConverter, points: int):
        """
        Command to add study points to a specific user.

        Adds the given number of points to the specified user in the database.
        If the user doesn't exist in the table, a new record is created.

        Args:
            ctx (commands.Context): The context in which the command was called.
            user (discord.User): The user to award points to.
            points (int): The number of points to award.

        Returns:
            None

        Error Handling:
            - Sends a message if non-positive points are given.
            - Catches exceptions and informs the user if something goes wrong.
        """
        try:
            if points <= 0:
                await ctx.send("🤠 You gotta add positive points, partner!")
                return

            user_id = user.id

            # Insert or update the user's points
            query = '''INSERT INTO study_points (user_id, points) 
                       VALUES (?, ?) 
                       ON CONFLICT(user_id) 
                       DO UPDATE SET points = points + ?'''
            self.execute_query(query, (user_id, points, points))

            await ctx.send(f"🤠 Added {points} points to user {user.name} ({user_id}).")

        except ValueError:
            await ctx.send("🤠 Hold up, partner! Make sure you're providing a valid number for points!")
        except Exception as e:
            await ctx.send(f"🤠 Something went wrong: {e}")

    @commands.command(help="Check your own study points.")
    async def checkpoints(self, ctx):
        """
        Command for users to check their current study points.

        Looks up the user ID in the database and returns the number of points they have.
        If the user is not found, a friendly message is shown.

        Args:
            ctx (commands.Context): The context in which the command was called.

        Returns:
            None

        Error Handling:
            - Catches and logs errors while fetching points.
        """
        try:
            user_id = ctx.author.id

            # Retrieve the points from the database
            query = '''SELECT points FROM study_points WHERE user_id = ?'''
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()

            if result is None:
                await ctx.send("🤠 Looks like you ain't got no points yet, partner!")
            else:
                points = result[0]
                await ctx.send(f"🤠 You currently have {points} points, partner!")

        except Exception as e:
            await ctx.send(f"🤠 Something went wrong while fetching points: {e}")


# Setup function to load the cog
async def setup(bot):
    """
    Setup function to add the Points cog to the bot.

    This function ensures any existing instance of the Points cog
    is removed before loading a new one, preventing duplicates.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    if "Points" in bot.cogs:
        await bot.remove_cog("Points")
    await bot.add_cog(Points(bot))
