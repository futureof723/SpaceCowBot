"""
Discord bot quiz extension.
This module enables users to take multiple-choice quizzes on topics of their choice.
Scores are recorded in a SQLite database and can be used in gamification systems
such as leaderboards or point tracking.
"""

import discord
from discord.ext import commands
import asyncio
import sqlite3
import logging
from utils.generate_quiz import generate_quiz  # Custom quiz generation logic


class Quiz(commands.Cog):
    """
    A Cog that allows users to take quizzes and earn study points.

    This cog provides an interactive quiz feature where users are prompted
    with multiple-choice questions. Correct answers increase their point
    totals, which are stored in a local SQLite database.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        conn (sqlite3.Connection): The database connection for storing quiz scores.
        c (sqlite3.Cursor): Cursor for executing database operations.
        logger (logging.Logger): Logger for tracking errors and debug info.
        ongoing_quizzes (dict): Tracks users with active quizzes to prevent overlap.
    """

    def __init__(self, bot):
        """
        Initialize the Quiz cog, open the database connection, and set up logging.

        Args:
            bot (commands.Bot): The bot instance this cog is attached to.
        """
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)
        self.ongoing_quizzes = {}  # Prevent users from taking multiple quizzes simultaneously

    def cog_unload(self):
        """
        Clean up the cog by committing and closing the database connection.

        Called automatically when the cog is unloaded.
        """
        self.conn.commit()
        self.conn.close()

    @commands.command(help="Take a multiple-choice quiz on a topic of your choice.")
    async def quiz(self, ctx, *, topic: str, timeout: int = 30):
        """
        Starts a quiz session for the user on the given topic.

        Fetches a set of multiple-choice questions, displays them one at a time,
        and evaluates the user's answers. Points are awarded for correct answers
        and stored in the database.

        Args:
            ctx (commands.Context): The context in which the command was called.
            topic (str): The topic on which to generate the quiz.
            timeout (int, optional): The time limit to answer each question (default is 30 seconds).

        Returns:
            None
        """
        if ctx.author.id in self.ongoing_quizzes:
            await ctx.send("You already have an ongoing quiz! Finish that one first.")
            return

        self.ongoing_quizzes[ctx.author.id] = True
        await ctx.send(f"Alright, {ctx.author.mention}, let’s quiz you on **{topic}**!")

        try:
            quiz_questions = generate_quiz(topic)
        except Exception as e:
            self.logger.error(f"Error generating quiz for topic '{topic}': {e}")
            await ctx.send("Sorry, I couldn’t generate a quiz. Try again later.")
            self.ongoing_quizzes.pop(ctx.author.id, None)
            return

        if not quiz_questions:
            await ctx.send("Sorry, I couldn’t generate a quiz. Try again later.")
            self.ongoing_quizzes.pop(ctx.author.id, None)
            return

        score = 0
        for i, question_data in enumerate(quiz_questions, start=1):
            question = question_data["question"]
            choices = question_data["choices"]
            answer = question_data["answer"].upper()

            # Format choices for display
            choices_str = "\n".join([f"{letter}) {text}" for letter, text in choices.items()])

            embed = discord.Embed(
                title=f"Question {i}",
                description=f"**{question}**\n\n{choices_str}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.content.upper() in choices.keys()

            try:
                # Wait for the user's answer or timeout
                msg = await self.bot.wait_for("message", check=check, timeout=timeout)
                if msg.content.upper() == answer:
                    score += 1
                    await ctx.send("✅ Correct!")
                else:
                    await ctx.send(f"❌ Wrong! The correct answer was **{answer}**.")
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Time's up! The correct answer was **{answer}**.")

        # Final score summary
        embed = discord.Embed(
            title="Quiz Complete!",
            description=f"You scored **{score} / {len(quiz_questions)}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

        try:
            # Update the user's score in the database
            self.c.execute(
                '''
                INSERT OR REPLACE INTO study_points (user_id, points)
                VALUES (?, COALESCE((SELECT points FROM study_points WHERE user_id = ?), 0) + ?)
                ''',
                (ctx.author.id, ctx.author.id, score)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Database error while updating study points: {e}")
            await ctx.send("Sorry, there was an error saving your quiz points. Try again later.")
        finally:
            # Clean up ongoing quiz flag for the user
            self.ongoing_quizzes.pop(ctx.author.id, None)


# Setup function to load the cog
async def setup(bot):
    """
    Setup function to add the Quiz cog to the bot.

    This function is called when the extension is loaded by discord.py.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    await bot.add_cog(Quiz(bot))
