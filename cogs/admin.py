from discord.ext import commands
import sqlite3
import logging

# Setup logger for error handling
logger = logging.getLogger(__name__)

# Assuming you have an existing database connection
conn = sqlite3.connect('study_points.db')  # SQLite connection is synchronous
c = conn.cursor()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="(Admin) Set this channel to receive automatic daily tips.")
    @commands.has_permissions(administrator=True)
    async def settipchannel(self, ctx):
        try:
            # Set the current channel ID in the settings table in the database
            c.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", ('daily_tip_channel', str(ctx.channel.id)))
            conn.commit()  # This is a synchronous operation
            await ctx.send("🤠 This here channel's now set for daily tips, partner!")
        except sqlite3.Error as e:
            logger.error(f"Database error while setting tip channel: {e}")
            await ctx.send("Sorry, there was an error setting the tip channel. Try again later.")

# Setup function should be async in discord.py 2.0+
async def setup(bot):
    await bot.add_cog(Admin(bot))  # Now this SHOULD be awaited