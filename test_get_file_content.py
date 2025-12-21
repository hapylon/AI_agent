from functions.get_file_content import get_file_content

files_to_test = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
working_dir = "calculator"
for item in files_to_test:
    print(f"Result for {item}:")
    print(get_file_content(working_dir, item))
    # result = get_files_info(working_dir, item)
    
    # # add two spaces to the start of each line
    # indented = "  " + result.replace("\n", "\n  ")
    # print(indented)
