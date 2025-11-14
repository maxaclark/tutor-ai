from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("API_KEY")

client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

AI_ROLE = """You are a coding tutor. 
You will guide the student on how to solve the problem without giving a direct answer. 
Ensure it aligns with their learning style. 
Assess their understanding along the way. 
Keep your initial responses very short and concise, elaborate thoroughly only when needed. 
If you give hints, make sure they are not too obvious."""

RESPONSE_PARAMS = {
    "model": "deepseek-chat",
    "presence_penalty": 0.5,
    "response_format": {"type": "text"},
    "max_tokens": 1024,
    "temperature": 0.4,
    "stream": False
}

# defines the model role
def init_conversation():
    return [
        {
            "role": "system",
            "content": AI_ROLE,
            "name": "Coding Assistant"
        }
    ]

# takes in question, returns answer
def get_bot_response(user_input, messages):

    # append user input to the list with ai role
    messages.append({
        "role": "user",
        "content": user_input,
        "name": "Student"
    })

    # get the response from the model
    response = client.chat.completions.create(
        **RESPONSE_PARAMS,
        messages=messages
    )
    bot_reply = response.choices[0].message

    # to make reply serializable
    bot_reply_dict = {
        "role": bot_reply.role,
        "content": bot_reply.content
    }

    # append bot reply to the list with ai role
    messages.append(bot_reply_dict)

    # reply messages for continued conversation, and response for the user
    return bot_reply.content, messages