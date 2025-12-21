from functions.run_python_file import run_python_file

test_cases = [["calculator", "main.py"], 
               ["calculator", "main.py", ["3 + 5"]], 
               ["calculator", "tests.py"], 
               ["calculator", "../main.py"], 
               ["calculator", "nonexistent.py"], 
               ["calculator","lorem.txt"]]
# test_items = lambda item: ["calculator"].append(item) for item in test_halves

for item in test_cases:
    if len(item) == 2:
        print(run_python_file(item[0], item[1]))
    if len(item) == 3:
        print(run_python_file(item[0], item[1], item[2]))
