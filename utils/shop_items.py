import discord
import random


# 💥 Functions for Shop Items
async def change_nickname_color(user, selected_color=None):
    """
    Changes the user's nickname color to a color selected by the user.
    If no color is selected, a random color is chosen from the list.
    """
    # Color names and their corresponding hex values
    color_map = {
        "Tomato": "#ff6347",
        "OrangeRed": "#ff4500",
        "LimeGreen": "#32cd32",
        "SteelBlue": "#4682b4",
        "BlueViolet": "#8a2be2"
    }

    # If no selected color, pick a random color from the available color names
    if not selected_color:
        selected_color = random.choice(list(color_map.keys()))

    # Get the hex color code for the selected color
    selected_color_hex = color_map.get(selected_color)

    if selected_color_hex:
        # Try to create a role with the selected color if it doesn't already exist
        role_name = f"Color-{selected_color}"
        existing_role = discord.utils.get(user.guild.roles, name=role_name)

        if not existing_role:
            # Create the role with the selected color
            role = await user.guild.create_role(name=role_name,
                                                color=discord.Color(int(selected_color_hex[1:], 16)))
            await user.add_roles(role)  # Assign the new role to the user
            await user.send(f"Your nickname color has been changed to {selected_color} ({selected_color_hex})!")
        else:
            await user.add_roles(existing_role)  # If the role exists, assign it
            await user.send(f"Your nickname color has been changed to {selected_color} ({selected_color_hex})!")
    else:
        await user.send("🤠 That’s not a valid color name! Please pick a valid one from the list.")


async def assign_special_role(user):
    """
    Assigns a special role to the user (can be expanded with more logic or role options).
    """
    role_name = "Special Role"  # Customize this as needed
    role = discord.utils.get(user.guild.roles, name=role_name)

    if role:
        await user.add_roles(role)
        await user.send(f"You've been assigned the '{role_name}' role!")
    else:
        await user.send(f"Sorry, the '{role_name}' role doesn't exist on this server.")


async def unlock_animated_emoji(user):
    """
    Unlocks an animated emoji for the user (this is just an example, you can customize it further).
    """
    emoji_name = "animated_emoji"  # This should be the name of the emoji you want to unlock
    emoji = discord.utils.get(user.guild.emojis, name=emoji_name)

    if emoji:
        # You can create a custom message here or assign the emoji in a special channel, for instance
        await user.send(f"You've unlocked the animated emoji {emoji}! Enjoy using it!")
    else:
        await user.send("Sorry, the requested animated emoji is not available in this server.")


async def apply_xp_boost(user):
    """
    Applies an XP boost (this can be integrated with your XP system).
    """
    # Example: Increase user's XP or a similar action
    # This is a placeholder, and you should integrate this with your XP system
    await user.send("You've activated an XP boost! Your XP gain is doubled for the next hour!")

    # Optionally: Handle time-based boosts, saving data, etc.
