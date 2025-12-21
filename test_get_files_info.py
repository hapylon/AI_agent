from functions.get_files_info import get_files_info

dirs = [".", "pkg", "/bin", "../"]
working_dir = "calculator"
for item in dirs:
    if item == ".":
        print(f"Result for current directory:")    
    else:
        print(f"Result for {item} directory:")
    # print(f"  {get_files_info(working_dir, item)}")
    
    result = get_files_info(working_dir, item)
    
    # add two spaces to the start of each line
    indented = "  " + result.replace("\n", "\n  ")
    print(indented)


# get_files_info("calculator", ".")
# get_files_info("calculator", "pkg")
# get_files_info("calculator", "/bin")
# get_files_info("calculator", "../")