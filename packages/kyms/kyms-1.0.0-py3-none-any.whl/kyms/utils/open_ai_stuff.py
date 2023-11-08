import openai
import logging
import time


def generate_response(system_prompt, user_prompt):
    logging.info(f"generate_gpt4_response SYSTEM: {system_prompt}")
    logging.info(f"generate_gpt4_response PROMPT: {user_prompt}")

    char_count = len(user_prompt) + len(system_prompt)
    logging.info(f"Calling openai with {char_count}...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.7,
    )
    result = response.choices[0].message.content

    logging.info(f"generate_response RESULT: {result}")
    time.sleep(60)
    return result
