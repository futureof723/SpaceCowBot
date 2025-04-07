import openai
import logging

# Set up logger for error handling
logger = logging.getLogger(__name__)

def generate_motivational_tip():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You're a wise cowboy who gives short motivational messages to students."},
                      {"role": "user", "content": "Give me a short motivational study tip or quote in cowboy style."}],
            temperature=0.9,
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Couldn't rustle up a tip right now, partner. Try again later."
    except Exception as e:
        logger.error(f"Error generating motivational tip: {e}")
        return "Couldn't rustle up a tip right now, partner. Try again later."
