"""
🧠 generate_quiz.py

This module uses OpenAI's GPT model to dynamically generate multiple-choice quizzes
based on a given topic. The quiz is returned as structured JSON that includes
questions, choices, and the correct answer.

Requirements:
- OpenAI Python SDK (`openai`)
- A logger utility at `utils.logger` for error reporting
"""

import openai
import json
from utils.logger import logger  # Custom logger for consistent error reporting


def generate_quiz(topic):
    """
    Generate a quiz containing 3 multiple-choice questions based on the provided topic.

    Parameters:
        topic (str): The subject or theme to generate quiz questions about.

    Returns:
        list or None: A list of dictionaries with keys: "question", "choices", and "answer".
                      Returns None if there is an error in quiz generation or API call.
    """
    try:
        # Define the role of the assistant in the conversation
        system_message = {
            "role": "system",
            "content": "You are a helpful AI that generates multiple choice quizzes in structured JSON."
        }

        # Prompt the AI with a user message containing instructions and expected output format
        user_message = {
            "role": "user",
            "content": f"""Generate a quiz with 3 multiple choice questions about "{topic}". 
Format your response as a JSON list like this:
[{{"question": "What is 2 + 2?", "choices": {{"A": "3", "B": "4", "C": "5", "D": "6"}}, "answer": "B"}}]"""
        }

        # Call the OpenAI API to generate quiz content
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message, user_message],
            temperature=0.7,
            max_tokens=500
        )

        # Extract and clean the generated content
        content = response.choices[0].message.content.strip()

        # Convert the JSON string into Python list of dicts
        quiz_data = json.loads(content)

        return quiz_data

    except openai.error.OpenAIError as e:
        logger.error(f"❌ OpenAI API error while generating quiz for topic '{topic}': {e}")
        return None
    except Exception as e:
        logger.error(f"❌ General error while generating quiz for topic '{topic}': {e}")
        return None
