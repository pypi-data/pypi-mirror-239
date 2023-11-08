import os
import fnmatch
import os

CONFIG_PATTERNS = ['*.yaml', '*.yml', '*.json', '*.conf', '*.ini', '*.env']

def create_output_file(repo_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                file_path = os.path.join(root, file)
                output.write(f'--- Start of {file_path} ---\n')
                with open(file_path, 'r', encoding='utf-8') as f:
                    output.write(f.read())
                output.write(f'--- End of {file_path} ---\n\n')


def sanitize_config_files(repo_dir):
    for root, dirs, files in os.walk(repo_dir):
        for pattern in CONFIG_PATTERNS:
            for filename in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, filename)
                with open(file_path, 'w') as file:
                    file.write('# Content omitted for convenience\n')