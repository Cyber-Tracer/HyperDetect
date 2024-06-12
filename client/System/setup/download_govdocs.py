import requests
import threading
import argparse

def download_zip_file(base_url, file_number, output_dir):
    url = f"{base_url}/{file_number}.zip"
    file_path = f"{output_dir}/{file_number}.zip"
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Failed to download {url}")

def download_zip_files_multithreaded(base_url, start_index, end_index, output_dir, num_threads=4):
    def worker(file_numbers):
        for file_number in file_numbers:
            print(f"Downloading {file_number}.zip...")
            download_zip_file(base_url, file_number, output_dir)
            print(f"Finished downloading {file_number}.zip")

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
    download_zip_files_multithreaded(base_url, start_index, end_index, output_dir, num_threads=6)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download zip files from a base URL.")
    parser.add_argument("start_index", type=int, help="Start index for file numbers")
    parser.add_argument("end_index", type=int, help="End index for file numbers")
    parser.add_argument("output_dir", type=str, help="Output directory for downloaded files")
    args = parser.parse_args()

    main(args.start_index, args.end_index, args.output_dir)