from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("API_KEY")

client = OpenAI(api_key=key)

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
    conversation = client.conversations.create()
    conversation_id = conversation.id

    response = client.responses.create(
        model="gpt-5-nano",
        input=[{"role": "system", "content": AI_ROLE}, {"role": "user", "content": "Hello!"}],
        conversation=conversation_id
    )

    return [{
        "conversation_id": conversation_id
    }]

# takes in question, returns answer
def get_bot_response(user_input, messages):

    # get the response from the model
    response = client.responses.create(
        model="gpt-5-nano",
        input=user_input,
        conversation=messages[0]["conversation_id"]
    )


    # reply messages for continued conversation, and response for the user
    return response.output_text