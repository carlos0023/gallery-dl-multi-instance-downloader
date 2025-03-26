import csv
import subprocess
import re
import concurrent.futures
import os
import threading
import signal

print_lock = threading.Lock()
file_lock = threading.Lock()

def sanitize_folder_name(folder_name):
    folder_name = re.sub(r'[:|/\\]', '-', folder_name)
    folder_name = folder_name.replace('"', "'").replace('“', "'").replace('”', "'")
    folder_name = re.sub(r'[^\x00-\x7F<>?*]', '_', folder_name)
    folder_name = folder_name.rstrip(' .')
    return folder_name

def run_command(folder_name, image_url, log_file, line_number, total_lines):
    sanitized_folder_name = sanitize_folder_name(folder_name)

    command = f'gallery-dl -w --no-part {image_url} -D "{sanitized_folder_name}"'  #-e "{log_file}_test.csv"
    with print_lock:
        print(f'[{line_number}/{total_lines}] {command}')
    process = subprocess.Popen(command, shell=True)
    result = process.wait()
    if result != 0:
        with print_lock:
            print(f'Command failed with return code {result}: {command}')
        with file_lock:
            with open(log_file, mode='a', newline='', encoding='utf-8') as log:
                log_writer = csv.writer(log)
                log_writer.writerow([result, sanitized_folder_name, image_url])

def validate_folder_path(prompt):
    while True:
        folder_path = str(input(prompt)).replace('"', '')
        return folder_path

def validate_file_path(prompt):
    while True:
        file_path = str(input(prompt)).replace('"', '')
        if os.path.isfile(file_path):
            return file_path
        else:
            print("Invalid file path. Please try again.")

def validate_new_file_path(prompt):
    while True:
        file_path = str(input(prompt)).replace('"', '')
        folder_path = os.path.dirname(file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return file_path

def validate_threads(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number >= 1:
                return number
            else:
                print("The number must be at least 1.")
        except ValueError:
            print("Invalid. Please enter a number.")

def run_commands_from_csv():
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    os.chdir(target_directory)

    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        lines = list(reader)
        total_lines = len(lines)

        with open(log_file, mode='w', newline='', encoding='utf-8') as log:
            log_writer = csv.writer(log)
            log_writer.writerow(['error', 'title', 'url'])

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for line_number, row in enumerate(lines, start=1):
                folder_name = row['title']
                image_url = row['url']
                futures.append(executor.submit(run_command, folder_name, image_url, log_file, line_number, total_lines))

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f'Exception occurred: {e}')

target_directory = validate_folder_path('Folder to store the output files at [e.g "D:\\path\\to\\files"]:\n')
csv_file = validate_file_path('\nYour CSV file with URLs (title, url) [e.g "D:\\path\\to\\file_urls.csv"]:\n')
log_file = validate_new_file_path('\nWhere you want the failed error log file [e.g "D:\\path\\to\\errored_dl_urls_log.csv"]:\n')
threads = validate_threads('\nHow many instances of the program to run at once [e.g Low: 16, Medium: 32, High: 64, Very High: 96, Extreme: 128]:\n')

run_commands_from_csv()

input("\nDone. Press Enter to finish...")
