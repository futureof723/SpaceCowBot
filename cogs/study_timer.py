"""
⏲️ study_timer.py

This module defines a StudyTimer cog for a Discord bot, allowing users to track study sessions
and earn points based on the time they spend studying. Users can start and stop study timers,
and their points are stored in a SQLite database. This module includes cooldown logic to prevent
users from starting multiple sessions too quickly.

Dependencies:
- discord.py
- sqlite3
- logging
"""

import discord
from discord.ext import commands
import time
import sqlite3
import logging


class StudyTimer(commands.Cog):
    """
    A cog that allows users to track their study time and earn points based on the time spent studying.

    Attributes:
        bot (commands.Bot): The bot instance.
        study_timer_start (float or None): The start time of the current study session (in seconds since epoch).
        study_timer_user (int or None): The user ID of the person currently studying.
        conn (sqlite3.Connection): The connection object to the SQLite database.
        c (sqlite3.Cursor): The cursor object for interacting with the database.
        logger (logging.Logger): Logger for error handling and debugging.
        user_last_study (dict): A dictionary that tracks the last study session time for each user.
    """

    def __init__(self, bot):
        """
        Initializes the StudyTimer cog.

        Parameters:
            bot (commands.Bot): The bot instance to associate with this cog.
        """
        self.bot = bot
        self.study_timer_start = None
        self.study_timer_user = None
        self.conn = sqlite3.connect('study_points.db')
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)
        self.user_last_study = {}

    def cog_unload(self):
        """
        Closes the SQLite connection when the cog is unloaded.
        This ensures any changes are saved to the database before the cog is removed.
        """
        self.conn.commit()
        self.conn.close()

    def get_points(self, user_id):
        """
        Retrieves the current study points for a given user from the database.

        Parameters:
            user_id (int): The user ID to query for points.

        Returns:
            int: The current points of the user.
        """
        self.c.execute('SELECT points FROM study_points WHERE user_id = ?', (user_id,))
        return self.c.fetchone()

    def update_points(self, user_id, points):
        """
        Updates the points of a user in the database. If the user doesn't exist, they are added.

        Parameters:
            user_id (int): The user ID to update points for.
            points (int): The number of points to assign to the user.
        """
        self.c.execute('INSERT OR REPLACE INTO study_points (user_id, points) VALUES (?, ?)',
                       (user_id, points))
        self.conn.commit()

    @commands.command(help="Start your study timer and earn points based on time.")
    async def startstudy(self, ctx):
        """
        Starts the study timer for the user. Users can only start a new study session once every 60 seconds.

        Parameters:
            ctx (commands.Context): The context of the command invocation.
        """
        user_id = ctx.author.id
        current_time = time.time()

        # Cooldown system: Prevent starting a study session more than once every minute
        if user_id in self.user_last_study and (current_time - self.user_last_study[user_id]) < 60:
            await ctx.send(
                "🤠 Hold your horses, partner! You can only start a new study session once every minute.")
            return

        self.user_last_study[user_id] = current_time

        if self.study_timer_start is not None:
            await ctx.send("The study timer is already running!")
        else:
            self.study_timer_start = time.time()
            self.study_timer_user = ctx.author.id
            points = self.get_points(ctx.author.id) or 0
            await ctx.send(f"🤠 You currently have {points} points. Let's start studying, partner!")

    @commands.command(help="Stop your study timer and see how many points you earned.")
    async def stopstudy(self, ctx):
        """
        Stops the study timer and calculates how many points the user earned based on study time.

        Parameters:
            ctx (commands.Context): The context of the command invocation.
        """
        if self.study_timer_start is None:
            await ctx.send("No timer is running.")
            return

        if self.study_timer_user != ctx.author.id:
            await ctx.send("You can't stop someone else's study timer.")
            return

        time_spent = time.time() - self.study_timer_start

        # Timeout safeguard: automatically stop after 1 hour
        if time_spent > 3600:
            await ctx.send("Your study session automatically timed out after 1 hour.")
            self.study_timer_start = None
            self.study_timer_user = None
            return

        minutes = int(time_spent // 60)
        points = minutes

        self.update_points(ctx.author.id, points)

        self.study_timer_start = None
        self.study_timer_user = None

        await ctx.send(
            f"{ctx.author.mention}, you studied for {minutes} minutes and earned {points} points!")


# Setup function to add the cog to the bot
async def setup(bot):
    """
    Sets up the StudyTimer cog and adds it to the bot.

    Parameters:
        bot (commands.Bot): The bot instance to add the cog to.
    """
    await bot.add_cog(StudyTimer(bot))
