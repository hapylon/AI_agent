import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    file_abspath = os.path.join(os.path.abspath(working_directory), file_path)
    abs_wd = os.path.abspath(working_directory)
    
    if not os.path.exists(file_abspath):
        return f'Error: File "{file_path}" not found.'
    if not os.path.abspath(file_abspath).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        
        completed_process = subprocess.run(
            ["python", file_abspath, *args], 
            timeout=30, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            cwd=abs_wd,
            text=True)
        output = f'STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}'
        if completed_process.returncode != 0:
            output += f'\nProcess exited with code {completed_process.returncode}'
        # if not output:
        #     return "No output produced"
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced"
        return output
    
    except Exception as e:
            return f'Error: executing Python file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    # description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    description="Runs a specified .py file at the specified filepath (constrained to the working directory), with the specified arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the .py file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                 type=types.Type.ARRAY,
                 description="A list of strings to pass as arguments to the .py file. Depending on the specified .py file and the desired output, it may be unnecessary to pass a list of arguments.",
                 items=types.Schema(
                    type=types.Type.STRING,
                    description="Each item is a string argument."
                )
            )
        },
    ),
)
        