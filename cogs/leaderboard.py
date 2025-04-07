import discord
from discord.ext import commands
import sqlite3
import logging

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)

    def cog_unload(self):
        self.conn.commit()
        self.conn.close()

    @commands.command(help="Show the leaderboard of top study point earners.")
    async def leaderboard(self, ctx):
        try:
            # Fetch top 10 users by points
            self.c.execute('SELECT user_id, points FROM study_points ORDER BY points DESC LIMIT 10')
            results = self.c.fetchall()

            if not results:
                await ctx.send("No study points have been earned yet!")
                return

            embed = discord.Embed(
                title="🏆 Study Leaderboard",
                description="Here are the top 10 study point earners:",
                color=discord.Color.gold()
            )
            embed.set_footer(text="Keep studying hard to climb the leaderboard!")
            embed.set_thumbnail(url="https://example.com/leaderboard-icon.png")  # Use a custom icon if you have one

            for i, (user_id, points) in enumerate(results, start=1):
                try:
                    user = await self.bot.fetch_user(user_id)
                    embed.add_field(
                        name=f"{i}. {user.name}",
                        value=f"{points} points",
                        inline=False
                    )
                except discord.NotFound:
                    embed.add_field(
                        name=f"{i}. Unknown User",
                        value=f"{points} points",
                        inline=False
                    )
                except Exception as e:
                    self.logger.error(f"Error while fetching user data: {e}")
                    embed.add_field(
                        name=f"{i}. Error fetching user",
                        value=f"{points} points",
                        inline=False
                    )

            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            self.logger.error(f"Database error while fetching leaderboard: {e}")
            await ctx.send("Sorry, there was an error retrieving the leaderboard. Try again later.")

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
