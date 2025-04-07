"""
🤠 motivational_tip.py

This module uses OpenAI's ChatCompletion API to generate a short, cowboy-themed
motivational message or study tip. These tips are designed to encourage students
with a bit of Western-style flair.

Example Output:
"Keep yer boots steady on the path of learnin’. One step at a time, partner."

Usage:
    from utils.motivational_tip import generate_motivational_tip
    tip = generate_motivational_tip()
    print(tip)
"""

import openai
import logging

# 📝 Set up a logger for capturing API errors or unexpected issues
logger = logging.getLogger(__name__)

def generate_motivational_tip():
    """
    Generates a short motivational study tip or quote in cowboy style using OpenAI.

    Returns:
        str: A motivational quote or message. If the API fails, a fallback message is returned.
    """
    try:
        # 🧠 Send a prompt to OpenAI instructing it to respond in a cowboy tone
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You're a wise cowboy who gives short motivational messages to students."
                },
                {
                    "role": "user",
                    "content": "Give me a short motivational study tip or quote in cowboy style."
                }
            ],
            temperature=0.9,  # 🔥 Add creativity and variation to the response
            max_tokens=100     # ⏱ Limit response length to keep it snappy
        )

        # ✅ Extract and return the message content
        return response['choices'][0]['message']['content'].strip()

    except openai.error.OpenAIError as e:
        # ❌ Log OpenAI-specific errors
        logger.error(f"OpenAI API error: {e}")
        return "Couldn't rustle up a tip right now, partner. Try again later."
    except Exception as e:
        # ❌ Log unexpected errors
        logger.error(f"Error generating motivational tip: {e}")
        return "Couldn't rustle up a tip right now, partner. Try again later."
