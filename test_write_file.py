from functions.write_file import write_file

files_to_write = [("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), 
                  ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
                  ("calculator", "/tmp/temp.txt", "this should not be allowed")
                  ]
for a, b, c in files_to_write:
    result = write_file(a, b, c)
    print(result)    
    
