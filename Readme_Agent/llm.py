import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()



def generate_response(messages) -> str:
    response = completion(
        model="openrouter/deepseek/deepseek-v4-flash",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        messages=messages,
    )

    return response["choices"][0]["message"]["content"] # type: ignore