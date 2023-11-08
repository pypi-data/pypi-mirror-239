import os
import fnmatch
import os

CONFIG_PATTERNS = ['*.yaml', '*.yml', '*.json', '*.conf', '*.ini', '*.env']

def create_output_file(repo_dir, output_file):
    common_encodings = ['utf-8', 'latin-1', 'utf-16']
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_content = None
                for encoding in common_encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            file_content = f.read()
                        break  # if the file is read successfully, exit the loop
                    except UnicodeDecodeError:
                        continue  # if an error occurs, try the next encoding
                if file_content is not None:
                    output.write(f'--- Start of {file_path} ---\n')
                    output.write(file_content)
                    output.write(f'--- End of {file_path} ---\n\n')
                else:
                    print(f"Skipping file {file_path} due to encoding issues.")

def sanitize_config_files(repo_dir):
    for root, dirs, files in os.walk(repo_dir):
        for pattern in CONFIG_PATTERNS:
            for filename in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, filename)
                with open(file_path, 'w') as file:
                    file.write('# Content omitted for convenience\n')