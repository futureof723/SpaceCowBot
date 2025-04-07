import discord
from discord.ext import commands
import asyncio
import sqlite3
import logging
from utils.generate_quiz import generate_quiz


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('study_points.db')
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)
        self.ongoing_quizzes = {}

    def cog_unload(self):
        self.conn.commit()
        self.conn.close()

    @commands.command(help="Take a multiple-choice quiz on a topic of your choice.")
    async def quiz(self, ctx, *, topic: str, timeout: int = 30):
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
            return

        if not quiz_questions:
            await ctx.send("Sorry, I couldn’t generate a quiz. Try again later.")
            return

        score = 0
        for i, question_data in enumerate(quiz_questions, start=1):
            question = question_data["question"]
            choices = question_data["choices"]
            answer = question_data["answer"].upper()

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
                msg = await self.bot.wait_for("message", check=check, timeout=timeout)
                if msg.content.upper() == answer:
                    score += 1
                    await ctx.send("✅ Correct!")
                else:
                    await ctx.send(f"❌ Wrong! The correct answer was **{answer}**.")
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Time's up! The correct answer was **{answer}**.")

        embed = discord.Embed(
            title="Quiz Complete!",
            description=f"You scored **{score} / {len(quiz_questions)}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

        try:
            self.c.execute(
                'INSERT OR REPLACE INTO study_points (user_id, points) VALUES (?, COALESCE((SELECT points FROM study_points WHERE user_id = ?), 0) + ?)',
                (ctx.author.id, ctx.author.id, score))
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Database error while updating study points: {e}")
            await ctx.send("Sorry, there was an error saving your quiz points. Try again later.")
        finally:
            self.ongoing_quizzes.pop(ctx.author.id, None)


async def setup(bot):
    await bot.add_cog(Quiz(bot))
