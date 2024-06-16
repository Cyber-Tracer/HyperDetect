import requests
import threading
import argparse
import os
import zipfile

def download_zip_file(base_url, file_number, output_dir):
    url = f"{base_url}/{file_number}.zip"
    file_path = f"{output_dir}/{file_number}.zip"
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        raise requests.HTTPError(f"Failed to download {url}")

def extract_and_remove_zip(zip_path, extract_to):
    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"The file {zip_path} does not exist.")
    
    # Check if the extraction directory exists, if not, create it
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Remove the zip file
    os.remove(zip_path)

def download_zip_files_multithreaded(base_url, start_index, end_index, output_dir, num_threads=2):
    def worker(file_numbers):
        for file_number in file_numbers:
            print(f"Downloading {file_number}.zip...")
            try:
                download_zip_file(base_url, file_number, output_dir)
            except requests.HTTPError as e:
                print(f"Failed to download {file_number}.zip: {e}")
                continue
            print(f"Finished downloading {file_number}.zip")
            print(f"Extracting {file_number}.zip...")
            extract_and_remove_zip(f"{output_dir}/{file_number}.zip", output_dir)
            print(f"Finished extracting {file_number}.zip")

    file_numbers = [f"{i:03d}" for i in range(start_index, end_index + 1)]
    chunk_size = len(file_numbers) // num_threads
    
    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=worker, args=(file_numbers[start:end],))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def main(start_index, end_index, output_dir, base_url = "https://digitalcorpora.s3.amazonaws.com/corpora/files/govdocs1/zipfiles"):
    download_zip_files_multithreaded(base_url, start_index, end_index, output_dir)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download zip files from a base URL.")
    parser.add_argument("start_index", type=int, help="Start index for file numbers")
    parser.add_argument("end_index", type=int, help="End index for file numbers")
    parser.add_argument("output_dir", type=str, help="Output directory for downloaded files")
    args = parser.parse_args()

    main(args.start_index, args.end_index, args.output_dir)