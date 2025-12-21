import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    # cage_path = "/mnt/c/Users/JohnC/github/bootdotdev/chatbot_project"
    result = []

    if not os.path.abspath(full_path).startswith(abs_working_dir):
    # if not os.path.abspath(full_path).startswith(cage_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    try:

        for item in os.listdir(full_path):
            actual_item = os.path.join(full_path, item)
            # item_dict = {}
            # item_dict["file_name"] = item
            line = f"- {item}: "

            if os.path.isfile(actual_item):
                line += f"file_size={os.path.getsize(actual_item)} bytes, "
                line += "is_dir=False"
            
            else:
                line += f"file_size={os.path.getsize(actual_item)} bytes, "
                line += "is_dir=True"

            result.append(line)

        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)