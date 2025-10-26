
import os
from dotenv import load_dotenv

from google import genai

client = genai.Client(api_key="AIzaSyBhHjYe4HQroWb6XWpwWQe9kLiCDMHvChk")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    import sys
    import argparse

    if len(sys.argv) == 1:
        print("No Prompt Provided")
        sys.exit(1)

    from google.genai import types

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    prompt = args.prompt

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)
    print(response.text)


    if args.verbose:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
