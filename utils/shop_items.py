"""
🛍️ shop_items.py

This module provides utility functions for handling shop item rewards
in a Discord bot context. Users can purchase perks like nickname color changes,
special roles, emoji unlocks, and XP boosts using earned study points.

Each function here is designed to be called asynchronously from bot commands.

Dependencies:
- discord.py
"""

import discord
import random


# 💥 Change Nickname Color
async def change_nickname_color(user, selected_color=None):
    """
    Changes the user's nickname color by assigning a role with the selected color.

    Parameters:
        user (discord.Member): The user who is changing their nickname color.
        selected_color (str, optional): A color name selected by the user. If not provided, one is chosen randomly.

    Behavior:
        - Assigns a role named "Color-{ColorName}" with the specified hex color.
        - If the role doesn't exist, it creates it and then assigns it.
        - Notifies the user via DM about the change.
    """
    color_map = {
        "Tomato": "#ff6347",
        "OrangeRed": "#ff4500",
        "LimeGreen": "#32cd32",
        "SteelBlue": "#4682b4",
        "BlueViolet": "#8a2be2"
    }

    if not selected_color:
        selected_color = random.choice(list(color_map.keys()))

    selected_color_hex = color_map.get(selected_color)

    if selected_color_hex:
        role_name = f"Color-{selected_color}"
        existing_role = discord.utils.get(user.guild.roles, name=role_name)

        if not existing_role:
            # Create new role with the selected color
            role = await user.guild.create_role(
                name=role_name,
                color=discord.Color(int(selected_color_hex[1:], 16))
            )
            await user.add_roles(role)
        else:
            # Use existing role
            await user.add_roles(existing_role)

        await user.send(
            f"🌈 Your nickname color has been changed to {selected_color} ({selected_color_hex})!")
    else:
        await user.send("🤠 That’s not a valid color name! Please pick a valid one from the list.")


# ⭐ Assign Special Role
async def assign_special_role(user):
    """
    Assigns a predefined special role to the user.

    Parameters:
        user (discord.Member): The user who is buying the role.

    Notes:
        You must manually ensure that the 'Special Role' exists on your server.
    """
    role_name = "Special Role"
    role = discord.utils.get(user.guild.roles, name=role_name)

    if role:
        await user.add_roles(role)
        await user.send(f"🌟 You've been assigned the '{role_name}' role!")
    else:
        await user.send(f"🚫 Sorry, the '{role_name}' role doesn't exist on this server.")


# 😎 Unlock Animated Emoji
async def unlock_animated_emoji(user):
    """
    Notifies the user that they've unlocked an animated emoji.

    Parameters:
        user (discord.Member): The user who purchased the unlock.

    Note:
        Make sure the server has an emoji named 'animated_emoji' or adjust the name accordingly.
    """
    emoji_name = "animated_emoji"
    emoji = discord.utils.get(user.guild.emojis, name=emoji_name)

    if emoji:
        await user.send(f"🎉 You've unlocked the animated emoji {emoji}! Enjoy using it!")
    else:
        await user.send("😔 Sorry, that animated emoji is not available on this server.")


# 🚀 Apply XP Boost
async def apply_xp_boost(user):
    """
    Simulates applying an XP boost to the user.

    Parameters:
        user (discord.Member): The user who activated the boost.

    Note:
        This function is a placeholder. Integrate it with your actual XP system.
    """
    await user.send("⚡ You've activated an XP boost! Your XP gain is doubled for the next hour!")

    # ⏱️ You could expand this by storing the boost status in your database
