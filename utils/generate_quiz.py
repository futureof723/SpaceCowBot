# 🧠 Generate quiz questions using OpenAI
import openai
import json
from utils.logger import logger

def generate_quiz(topic):
    try:
        system_message = {
            "role": "system",
            "content": "You are a helpful AI that generates multiple choice quizzes in structured JSON."
        }

        user_message = {
            "role": "user",
            "content": f"""Generate a quiz with 3 multiple choice questions about "{topic}". 
Format your response as a JSON list like this:
[{{"question": "What is 2 + 2?", "choices": {{"A": "3", "B": "4", "C": "5", "D": "6"}}, "answer": "B"}}]"""
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message, user_message],
            temperature=0.7,
            max_tokens=500
        )

        content = response.choices[0].message.content.strip()
        quiz_data = json.loads(content)
        return quiz_data

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        return None