import os
from dotenv import load_dotenv

from google import genai

client = genai.Client(api_key="AIzaSyBhHjYe4HQroWb6XWpwWQe9kLiCDMHvChk")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
)
    print(response.text)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
