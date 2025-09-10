import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith('.py'):
        f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ['python3', abs_file_path]+args,
            capture_output=True,
            cwd=abs_working_dir,
            timeout=30,
            text=True
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
             output.append(f"Process exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced."
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file with the python3 interpreter Accepts addtional CLI args as optional array .",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The fie to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as CLO args for python file",
                items=types.Schema(
                    type=types.Type.STRING,
                )
            )
        },
    ),
)
