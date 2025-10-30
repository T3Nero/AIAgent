
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import schema_get_files_info, schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

client = genai.Client(api_key="AIzaSyBhHjYe4HQroWb6XWpwWQe9kLiCDMHvChk")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    import sys
    import argparse

    if len(sys.argv) == 1:
        print("No Prompt Provided")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    prompt = args.prompt
    verbose = args.verbose

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    iters = 0
    while True:
        iters += 1
        if iters > 20:
            print(f"Maximum iterations reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, available_functions, prompt, verbose)
            if final_response:
                print("Final Response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate content: {e}")

def generate_content(client, messages, available_functions, prompt, verbose):

    response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    # Check for a function call
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])


    if not function_responses:
        raise Exception("no function responses generated, exiting.")


    if verbose:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
