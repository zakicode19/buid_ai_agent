import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

MAX_ITERATION = 20
system_prompt =  """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of a file
- Write to a file (create or update)
- Run a Ptyhon file with optional argument
When the users asks about the code project thery are referring to the working directory. So you should typically start by looking at the project's files, and figuring out how to run the porject and how to run tis tests, you'll always wnat to test the tests and the actual project. to veryfy that behavour is working.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
'''
args = sys.argv

if len(args) == 1:
    print('Pleas proved a promt')
    sys.exit(1)
promt = args[1]
'''
def main():

    args = sys.argv

    if len(args)==1:
        print('Pleas proved a promt')
        sys.exit(1)
    promt = args[1]
    verbose_mode  = False

    if '-v' in args or '--verbose' in args:
        verbose_mode = True

    #print(f"Your promt: {promt}")
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role='user', parts=[types.Part(text=promt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python_file,
            schema_get_file_content,
            schema_write_file
        ]
    )

    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        )
    for _ in range(MAX_ITERATION):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=config)
        

        if verbose_mode:
            print('User prompt: ', promt)
            print('Prompt tokens:',response.usage_metadata.prompt_token_count)
            print('Response tokens:',response.usage_metadata.candidates_token_count)
            
        #print('Response:')
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose_mode)
                messages.append(result)
                #print(result)
        else:
            print(response.text)
            return
if __name__ == "__main__":
    main()
