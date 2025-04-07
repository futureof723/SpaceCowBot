import discord
from discord.ext import commands
import openai
import os
import asyncio
import logging
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

logger = logging.getLogger(__name__)

user_last_asked = {}

class AskCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Ask a question and get a space cowboy-style answer.")
    async def ask(self, ctx, *, question: str):
        # Handle empty or invalid questions
        if not question.strip():
            await ctx.send("🤠 Ain't no question here, partner. Please ask me somethin'!")
            return

        # Rate limiting to avoid too many requests
        user_id = ctx.author.id
        if user_id in user_last_asked and (time.time() - user_last_asked[user_id]) < 10:  # 10 seconds cooldown
            await ctx.send("🤠 Slow down, partner! You can ask again in a few seconds.")
            return

        user_last_asked[user_id] = time.time()

        prompt = f"Answer the following question in the style of a space cowboy: '{question}'"

        try:
            # Use run_in_executor to run the synchronous OpenAI API call in a separate thread
            response = await self.bot.loop.run_in_executor(
                None,
                lambda: openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "You are a space cowboy who gives friendly, adventurous responses."},
                              {"role": "user", "content": question}]
                )
            )

            # Extract the generated text from the response
            answer = response['choices'][0]['message']['content'].strip()

            # Send the response back to Discord
            await ctx.send(f"{answer}")

        except Exception as e:
            logger.error(f"Error while fetching response from OpenAI: {e}")
            await ctx.send("🤠 Something went wrong with the space-time continuum... try again later.")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(AskCommand(bot))