import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" is not a file'
    
   
    try:
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            return f'{file_content_string}"{file_path}" truncated at 10000 characters'
        return file_content_string
    except Exception as e:
        return f"Error reading files: {e}"
     



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of the given file as a string , constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file from, relative to the working directory.",
            ),
        },
    ),
)
