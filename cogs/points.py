import sqlite3
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params):
        try:
            # Execute the SQL query with parameters
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise

    @commands.command(help="Add study points to a user.")
    async def addpoints(self, ctx, user: commands.UserConverter, points: int):
        try:
            # Ensure the points are a valid integer
            if points <= 0:
                await ctx.send("🤠 You gotta add positive points, partner!")
                return

            # Fetch user ID and the user object
            user_id = user.id

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
        try:
            # Fetch user ID (the user who called the command)
            user_id = ctx.author.id

            query = '''SELECT points FROM study_points WHERE user_id = ?'''
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()

            if result is None:
                await ctx.send(f"🤠 Looks like you ain't got no points yet, partner!")
            else:
                points = result[0]
                await ctx.send(f"🤠 You currently have {points} points, partner!")

        except Exception as e:
            await ctx.send(f"🤠 Something went wrong while fetching points: {e}")

# Setup function to add the cog to the bot
async def setup(bot):
    if "Points" in bot.cogs:
        await bot.remove_cog("Points")
    await bot.add_cog(Points(bot))
