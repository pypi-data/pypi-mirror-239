import os
import fnmatch
import os

from repotofile.ignored_patterns import DEFAULT_IGNORE_DIRS, DEFAULT_IGNORE_PATTERNS

CONFIG_PATTERNS = ['*.yaml', '*.yml', '*.json', '*.conf', '*.ini', '*.env']

def create_output_file(repo_dir, output_file):
    common_encodings = ['utf-8', 'latin-1']
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(repo_dir):
            if should_ignore_path(root):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                file_content = None
                for encoding in common_encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            file_content = f.read()
                            if encoding == 'utf-16':
                                file_content = file_content.lstrip('\ufeff')
                        break  # if the file is read successfully, exit the loop
                    except UnicodeDecodeError:
                        continue  # if an error occurs, try the next encoding
                if file_content is not None:
                    output.write(f'--- Start of {file_path} ---\n')
                    output.write(file_content)
                    output.write('\n')
                    output.write(f'--- End of {file_path} ---\n\n')
                else:
                    print(f"Skipping file {file_path} due to encoding issues.")

def should_ignore_path(path, ignore_dirs=DEFAULT_IGNORE_DIRS, additional_ignore_dirs=[]):
    ignore_dirs = ignore_dirs + additional_ignore_dirs
    # Check if the path contains any of the ignored directories
    for ignored_dir in ignore_dirs:
        if ignored_dir in path.split(os.sep):
            return True
    return False
                    
def sanitize_config_files(repo_dir, additional_ignore_patterns=[], additional_ignore_dirs=[]):
    # Combine the default ignore patterns with any additional ones provided by the user
    ignore_patterns = DEFAULT_IGNORE_PATTERNS + additional_ignore_patterns

    for root, dirs, files in os.walk(repo_dir):
        
        # Remove the ignored directories from the list of directories to traverse
        if should_ignore_path(root, additional_ignore_dirs=additional_ignore_dirs):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file matches any of the ignore patterns
            if should_ignore_file(file_path, ignore_patterns):
                # Open the file and replace its contents
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write('# Content omitted for convenience\n')

def should_ignore_file(file, ignore_patterns):
    return any(fnmatch.fnmatch(file, pattern) for pattern in ignore_patterns)

def get_repo_name_from_url(url: str):
    # handles cases where there is .git on the end of the URL or not
    url = url.strip()
    url = url.rstrip('/')
    url = url.split('?')[0]
    url = url.strip('.git')
    return url.split('/')[-1]
    

    