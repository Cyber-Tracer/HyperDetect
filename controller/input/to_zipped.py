import os
import zipfile
import argparse

def zip_subdirectories(directory, output_directory):
    # Get all subdirectories from the given directory
    subdirectories = [subdir for subdir in os.listdir(directory) if os.path.isdir(os.path.join(directory, subdir))]

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Zip each subdirectory to the output directory
    for subdir in subdirectories:
        zip_filename = os.path.join(output_directory, subdir + '.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(os.path.join(directory, subdir)):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(directory, subdir)))
        print(f'Zipped {subdir} to {zip_filename}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Zip all subdirectories in a given directory')
    parser.add_argument('--directory', type=str, help='The directory to zip subdirectories from, default: V1', default=os.path.join(os.path.dirname(__file__), 'V1/'))
    parser.add_argument('--output_directory', type=str, help='The output directory for the zipped files, default: ../input_zipped/V1', default=os.path.join(os.path.dirname(__file__), '../input_zipped/V1/'))
    args = parser.parse_args()
    zip_subdirectories(args.directory, args.output_directory)