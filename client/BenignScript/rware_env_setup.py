import sys
import os
import random as rnd

def create_and_write_file(file_path, content):
    """
    Creates a new file and writes the given content to it.
    """
    with open(file_path, "w") as file:
        file.write(content)
    print(f"File '{file_path}' created and content written.")


# Get the path from the command line arguments
path = sys.argv[1]

# Use the path as needed
print(f"Path from arguments: {path}")

# Check if the path exists
if not os.path.exists(path):
    sys.exit("Path does not exist.")

directories = ['valued_memories', 'important_documents', 'personal_files', 'important_company_data', 'important_company_data\\steve']
file_types = ['txt', 'doc', 'pdf', 'xls', 'csv', 'jpg', 'png', 'mp4', 'mp3']
file_names = ['larry', 'steve', 'bill', 'elon', 'tim', 'sundar', 'satya', 'mark', 'jeff', 'jack']
max_files = 10


# create basic folder structure in the specified path
for idx, directory in enumerate(directories):
    directories[idx] = os.path.join(path, directory)
    os.makedirs(directories[idx], exist_ok=True)
    print(f"Directory created: {directory}")
    amt_dir_files = rnd.randint(2, 10)
    for i in range(amt_dir_files):
        file_name = f"{rnd.choice(file_names)}_{i}.{rnd.choice(file_types)}"
        file_path = os.path.join(directories[idx], file_name)
        create_and_write_file(file_path, f"Content of file {file_name}")
        print(f"File created: {file_name}")

    

