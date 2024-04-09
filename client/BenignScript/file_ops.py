import os
import time
import random as rnd

def create_and_write_file(file_path, content):
    """
    Creates a new file and writes the given content to it.
    """
    with open(file_path, "w") as file:
        file.write(content)
    print(f"File '{file_path}' created and content written.")

def read_file(file_path):
    """
    Reads and prints the content of the specified file.
    """
    with open(file_path, "r") as file:
        file.read()
        print("File read:\n", file_path)

def rename_file(old_name, new_name):
    """
    Renames the specified file from old_name to new_name.
    """
    os.rename(old_name, new_name)
    print(f"File renamed from '{old_name}' to '{new_name}'.")

def delete_file(file_path):
    """
    Deletes the specified file.
    """
    os.remove(file_path)
    print(f"File '{file_path}' has been deleted.")

def benign_rename(file_path):
    new_file_name = "benign_renamed_file.txt"
    new_file_name = os.path.join(os.path.dirname(file_path), new_file_name)
    rename_file(file_path, new_file_name)
    time.sleep(1)
    rename_file(new_file_name, file_path)

def benign_delete(file_path):
    delete_file(file_path)
    time.sleep(1)
    create_and_write_file(file_path, "This is a benign file created for testing purposes.")

def benign_file_read(file_path):
    read_file(file_path)

def benign_file_append(file_path):
    with open(file_path, "a") as file:
        file.write('Some more content')


def main():
    file_name = "benign_test_file.txt"
    content = "This is a benign file created for testing purposes.\n" \
              "Adding some more content to simulate typical user behavior.\n"
    
    directories = ["C:\\Users\\Client\\Downloads", "C:\\Users\\Client\\Desktop", "C:\\Users\\Client\\Documents"]
    start_time = time.time()
    benign_fileops_duration = 60
    rnd_min = 1
    rnd_max = 5

    print(f"Simulate bengign file operations for {benign_fileops_duration} seconds, rnd timeout between {rnd_min} and {rnd_max} seconds.")

    # Create file in each directory, establish baseline
    for directory in directories:
        time.sleep(rnd.randint(rnd_min, rnd_max))
        file_path = os.path.join(directory, file_name)
        create_and_write_file(file_path, content)

    benign_funcs = [benign_rename, benign_delete, benign_file_read, benign_file_append]

    while time.time() - start_time < benign_fileops_duration:
        time.sleep(rnd.randint(rnd_min, rnd_max))
        rnd.choice(benign_funcs)(file_path)

    print("Benign file operations completed, cleaning up...")
    for directory in directories:
        file_path = os.path.join(directory, file_name)
        delete_file(file_path)

    print("Benign fileops simulation completed.")

if __name__ == "__main__":
    main()
