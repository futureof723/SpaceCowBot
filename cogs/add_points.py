from discord.ext import commands

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Example command to add points for a user
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

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Points(bot))
