"""
Discord bot shop extension.
This module provides a virtual shop where users can spend their earned study points
on rewards like nickname color changes, roles, emoji perks, and XP boosts.
"""

import discord
from discord.ext import commands
import sqlite3
import asyncio
from utils.shop_items import (
    change_nickname_color,
    assign_special_role,
    unlock_animated_emoji,
    apply_xp_boost
)


class Shop(commands.Cog):
    """
    A Cog that allows users to purchase in-server perks using their study points.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        conn (sqlite3.Connection): SQLite database connection.
        cursor (sqlite3.Cursor): Cursor for executing SQL queries.
    """

    def __init__(self, bot):
        """
        Initialize the Shop cog with a database connection and reference to the bot.

        Args:
            bot (commands.Bot): The bot instance this cog is attached to.
        """
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params):
        """
        Execute a SQL query with parameters and commit the transaction.

        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters to safely insert into the query.

        Raises:
            Exception: If a database error occurs.
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")

    @commands.command(help="Open the shop to purchase items using points.")
    async def shop(self, ctx):
        """
        Display a shop menu of available items and handle purchase interactions.

        This command shows a list of items a user can buy with their study points.
        Once a selection is made, it checks the user's balance, deducts points,
        and applies the reward (e.g., color change, role, emoji unlock).

        Args:
            ctx (commands.Context): The context in which the command was invoked.

        Returns:
            None
        """
        # Define shop items and their costs
        items = {
            'Change Nickname Color': 50,
            'Assign Special Role': 100,
            'Unlock Animated Emoji': 75,
            'XP Boost': 150
        }

        # Create and send an embed with shop items
        embed = discord.Embed(
            title="SpaceCowBot Shop",
            description="Choose an item and spend points!",
            color=discord.Color.green()
        )
        for i, (item, price) in enumerate(items.items(), 1):
            embed.add_field(name=f"{i}. {item}", value=f"Price: {price} points", inline=False)

        await ctx.send(embed=embed)
        await ctx.send("🤠 Pick an item by typing the corresponding number.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

        try:
            # Wait for user input (item selection)
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            choice = int(msg.content)

            if choice < 1 or choice > len(items):
                await ctx.send("🤠 That's not a valid choice, partner!")
                return

            item_name = list(items.keys())[choice - 1]
            price = items[item_name]

            # Check user's available points
            user_id = ctx.author.id
            query = '''SELECT points FROM study_points WHERE user_id = ?'''
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()

            if result is None or result[0] < price:
                await ctx.send("🤠 You don't have enough points for this item!")
                return

            # Deduct the price from user's points
            self.execute_query(
                '''UPDATE study_points SET points = points - ? WHERE user_id = ?''',
                (price, user_id)
            )

            # Handle each shop item purchase
            if item_name == 'Change Nickname Color':
                await ctx.send("🤠 You can choose a color for your nickname! Here's a list of options:")
                color_list = "\n".join([
                    "Tomato",
                    "OrangeRed",
                    "LimeGreen",
                    "SteelBlue",
                    "BlueViolet"
                ])
                await ctx.send(f"Available colors:\n{color_list}\n\nOr type the color name directly (e.g., Tomato).")

                def color_check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                msg = await self.bot.wait_for('message', check=color_check, timeout=60)
                selected_color = msg.content.strip()

                valid_colors = ["Tomato", "OrangeRed", "LimeGreen", "SteelBlue", "BlueViolet"]
                if selected_color in valid_colors:
                    await change_nickname_color(ctx.author, selected_color)
                else:
                    await ctx.send("🤠 That’s not a valid color name! Please choose from the list.")

            elif item_name == 'Assign Special Role':
                await assign_special_role(ctx.author)

            elif item_name == 'Unlock Animated Emoji':
                await unlock_animated_emoji(ctx.author)

            elif item_name == 'XP Boost':
                await apply_xp_boost(ctx.author)

            # Confirm the purchase
            await ctx.send(f"🤠 You've spent {price} points on **{item_name}**!")

        except asyncio.TimeoutError:
            await ctx.send("🤠 You took too long to make a choice, partner!")
        except Exception as e:
            await ctx.send(f"🤠 Something went wrong: {e}")


# Setup function to load the cog
async def setup(bot):
    """
    Setup function to add the Shop cog to the bot.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    await bot.add_cog(Shop(bot))
