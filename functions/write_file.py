import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        file_path_dir = os.path.dirname(full_path)
        if file_path_dir and not os.path.exists(file_path_dir): 
            os.makedirs(file_path_dir)
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
name="write_file",
description="Writes the specified content to a specified filepath (constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "filepath": types.Schema(
            type=types.Type.STRING,
            description="The filepath of the file to write, relative to the working directory.",
        ),
        "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to a file at the specified filepath."
        )
    },
),
)
    