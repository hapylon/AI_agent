import os
from google.genai import types
from functions.get_files_info import get_files_info 
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_result = None
    
    if verbose==True:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    function_call_part.args["working_directory"] = "./calculator"
    
    FUNCTIONS = {
        "run_python_file": run_python_file,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "get_files_info": get_files_info,
        }
    if function_name in ("get_file_content", "write_file"):
        if "filepath" in function_call_part.args:
            function_call_part.args["file_path"] = function_call_part.args.pop("filepath")
            
    if function_name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    function_to_call = FUNCTIONS[function_name]
    function_result = function_to_call(**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    # try:
    #     FUNCTIONS = {
    #         "run_python_file": run_python_file,
    #         "get_file_content": get_file_content,
    #         "write_file_content": write_file_content,
    #         "get_files_info": get_files_info,
    #         }
    #     if function_name in FUNCTIONS:
    #         function_to_call = FUNCTIONS[function_call_part.name]
    #         function_result = function_to_call(**function_call_part.args)
    # except:
    #     return types.Content(
    #         role="tool",
    #         parts=[
    #             types.Part.from_function_response(
    #                 name=function_name,
    #                 response={"error": f"Unknown function: {function_name}"},
    #             )
    #         ],
    #     )
    # return types.Content(
    #     role="tool",
    #     parts=[
    #         types.Part.from_function_response(
    #             name=function_name,
    #             response={"result": function_result},
    #         )
    #     ],
    # )
