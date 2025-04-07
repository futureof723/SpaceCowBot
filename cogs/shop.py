# shop.py

import discord
from discord.ext import commands
import sqlite3
from utils.shop_items import change_nickname_color, assign_special_role, unlock_animated_emoji, apply_xp_boost

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")

    @commands.command(help="Open the shop to purchase items using points.")
    async def shop(self, ctx):
        items = {
            'Change Nickname Color': 50,
            'Assign Special Role': 100,
            'Unlock Animated Emoji': 75,
            'XP Boost': 150
        }

        embed = discord.Embed(title="SpaceCowBot Shop", description="Choose an item and spend points!", color=discord.Color.green())
        for i, (item, price) in enumerate(items.items(), 1):
            embed.add_field(name=f"{i}. {item}", value=f"Price: {price} points", inline=False)

        await ctx.send(embed=embed)
        await ctx.send("🤠 Pick an item by typing the corresponding number.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)

            choice = int(msg.content)
            if choice < 1 or choice > len(items):
                await ctx.send("🤠 That's not a valid choice, partner!")
                return

            item_name = list(items.keys())[choice - 1]
            price = items[item_name]

            user_id = ctx.author.id
            query = '''SELECT points FROM study_points WHERE user_id = ?'''
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()

            if result is None or result[0] < price:
                await ctx.send("🤠 You don't have enough points for this item!")
                return

            self.execute_query('''UPDATE study_points SET points = points - ? WHERE user_id = ?''', (price, user_id))

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
                # Check if the selected color is valid
                valid_colors = ["Tomato", "OrangeRed", "LimeGreen", "SteelBlue", "BlueViolet"]
                if selected_color in valid_colors:
                    await change_nickname_color(ctx.author, selected_color)  # Now passes selected_color
                else:
                    await ctx.send("🤠 That’s not a valid color name! Please choose from the list.")

            elif item_name == 'Assign Special Role':
                await assign_special_role(ctx.author)
            elif item_name == 'Unlock Animated Emoji':
                await unlock_animated_emoji(ctx.author)
            elif item_name == 'XP Boost':
                await apply_xp_boost(ctx.author)

            await ctx.send(f"🤠 You've spent {price} points on {item_name}!")

        except Exception as e:
            await ctx.send(f"🤠 Something went wrong: {e}")
        except asyncio.TimeoutError:
            await ctx.send("🤠 You took too long to make a choice, partner!")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Shop(bot))
