"""
Discord bot extension that handles a points system for users.
This module provides functionality to track and modify study points for server members.
"""

from discord.ext import commands


class Points(commands.Cog):
    """
    A Cog for managing a study points system in a Discord server.

    This cog provides commands to add, remove, and view study points for users.
    Points are stored in a SQLite database with the 'study_points' table.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
    """

    def __init__(self, bot):
        """
        Initialize the Points cog.

        Args:
            bot (commands.Bot): The Discord bot instance this cog is attached to.
        """
        self.bot = bot

    def execute_query(self, query, params=None):
        """
        Execute an SQL query on the database.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query. Defaults to None.

        Returns:
            Varies: Results from the database query if applicable.

        Note:
            This method requires database connection logic that is not shown in the snippet.
            The implementation should handle connection management and cursor operations.
        """
        # Database execution code would go here
        pass

    # Example command to add points for a user
    @commands.command(help="Add study points to a user.")
    async def addpoints(self, ctx, user: commands.UserConverter, points: int):
        """
        Add study points to a specified user.

        This command adds the specified number of points to a user's total in the database.
        If the user doesn't exist in the database, they will be created with the initial points.

        Args:
            ctx (commands.Context): The invocation context.
            user (discord.User): The user to add points to (converted from mention or ID).
            points (int): The number of points to add.

        Returns:
            None: Feedback is sent directly to the Discord channel.

        Raises:
            ValueError: If the points parameter can't be converted to a positive integer.
            Exception: If there's a database error or other unexpected issue.
        """
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
            await ctx.send(
                "🤠 Hold up, partner! Make sure you're providing a valid number for points!")
        except Exception as e:
            await ctx.send(f"🤠 Something went wrong: {e}")


async def setup(bot):
    """
    Setup function to add the Points cog to the bot.

    This function is called by Discord.py when the extension is loaded.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    await bot.add_cog(Points(bot))