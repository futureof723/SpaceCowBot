import discord
from discord.ext import commands
import time
import sqlite3
import logging


class StudyTimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.study_timer_start = None
        self.study_timer_user = None
        self.conn = sqlite3.connect('study_points.db')
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)
        self.user_last_study = {}

    def cog_unload(self):
        self.conn.commit()
        self.conn.close()

    def get_points(self, user_id):
        self.c.execute('SELECT points FROM study_points WHERE user_id = ?', (user_id,))
        return self.c.fetchone()

    def update_points(self, user_id, points):
        self.c.execute('INSERT OR REPLACE INTO study_points (user_id, points) VALUES (?, ?)',
                       (user_id, points))
        self.conn.commit()

    @commands.command(help="Start your study timer and earn points based on time.")
    async def startstudy(self, ctx):
        user_id = ctx.author.id
        current_time = time.time()

        # Cooldown system
        if user_id in self.user_last_study and (
                current_time - self.user_last_study[user_id]) < 60:  # 1 minute cooldown
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
        if self.study_timer_start is None:
            await ctx.send("No timer is running.")
            return

        if self.study_timer_user != ctx.author.id:
            await ctx.send("You can't stop someone else's study timer.")
            return

        time_spent = time.time() - self.study_timer_start

        # Timeout safeguard
        if time_spent > 3600:  # Automatically stop after 1 hour
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


async def setup(bot):
    await bot.add_cog(StudyTimer(bot))
