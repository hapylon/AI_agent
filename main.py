import argparse
import os
# from google.genai import types

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info 
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.call_function import call_function

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_run_python_file,
        schema_write_file
    ] 
)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # print("Parsed args:", args.user_prompt)


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Did you create a .env file and set GEMINI_API_KEY?")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    counter = 0
    while counter < 20:
        if (response_text_empty == True) & (function_call_made == False):
            print(f"FINAL RESPONSE: {messages}")
            break

        else:
            try:
                generate_content(client, messages, verbose=args.verbose)

            except Exception as e:
                print(f'Error in generate_content loop: {e}');
                break;
        counter +=1
        
response_text_empty = None
function_call_made = None

def generate_content(client, messages, verbose: bool = False):    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        ),
        # config=config # types.GenerateContentConfig(system_instruction=system_prompt)
    )
    list_for_later = []

    for variation in response.candidates:
        messages.append(variation.content)

    if response.usage_metadata is None:
        raise RuntimeError("Gemini API response appears malformed") # seems like a failed API request because response.metadata is None...")
    
    if verbose:
        # print("User prompt:", messages[0].parts[0].text)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # print("Response:")
    if not response.function_calls:
        print("Response:")
        print(response.text)
        global response_text_empty
        if not response.text:    
            response_text_empty = True
        else:
            response_text_empty = False
        return
        # for function_call_part in response.function_calls:
        #     print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part, verbose=verbose)
        parts = function_call_result.parts
        global function_call_made
        function_call_made = True
        if not parts or not parts[0].function_response or not parts[0].function_response.response:
            raise Exception("fatal exception of some sort")
        else:
            list_for_later.append(parts[0])
        if verbose:
            # print(f"-> {function_call_result.parts[0].function_response.response}")
            print(f"-> {parts[0].function_response.response}")
    
    user_message_with_results = types.Content(
        role = "user",
        parts = list_for_later
    )
    
    messages.append(user_message_with_results)
    
    
if __name__ == "__main__":
    main()
