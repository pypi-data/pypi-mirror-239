import argparse
import shutil
import sys
from repotofile.utils import get_repo_name_from_url, sanitize_config_files, create_output_file
from repotofile.git_operations import clone_repo
import os




def run(url, branch, output, ignore_files, ignore_dirs):
    # Step 1: Clone the repo or use the directory
    if os.path.isdir(url):
        print('using existing directory')
        repo_name = os.path.abspath(url).split('/')[-1]
        repo_dir = url
        output_file = f'{repo_name}.txt'
    else:
        print(f'cloning {url}...')
        repo_name = get_repo_name_from_url(url)
        repo_dir = repo_name
        output_file = f'{repo_name}.txt'
        try:
            if not clone_repo(url, branch, repo_name):
                raise Exception("Failed to clone the repository. Please check the URL and branch/tag name.")

        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            sys.exit(1)
        
    # Step 2: Sanitize configuration files
    sanitize_config_files(repo_dir, ignore_files, additional_ignore_dirs=ignore_dirs)

    # Step 3: Generate the output file
    create_output_file(repo_dir, output_file)

    # Step 4: Cleanup repo_dir
    if not os.path.isdir(url):
        shutil.rmtree(repo_name)

    print(f"Repository contents have been successfully written to {output_file}")

def parse_args():
    parser = argparse.ArgumentParser(description='CLI tool to clone GitHub repos using Git, optionally sanitize config files, and generate a text file.')
    parser.add_argument('url', help='URL of the GitHub repository to clone or directory to process')
    parser.add_argument('-b', '--branch', help='Branch or tag to clone', default=None)
    parser.add_argument('-o', '--output', help='Custom output file name or path', default=None)
    parser.add_argument(
        '--ignore-files',
        help='A comma-separated list of glob patterns for files to ignore',
        default=''
    )
    parser.add_argument(
        '--ignore-dirs',
        help='A comma-separated list of dirs to ignore',
        default=''
    )
    args = parser.parse_args()
    args.ignore_files = args.ignore_files.split(',') if args.ignore_files else []
    args.ignore_dirs = args.ignore_dirs.split(',') if args.ignore_dirs else []
    return args

def main():
    args = parse_args()
    run(args.url, args.branch, args.output, args.ignore_files, args.ignore_dirs)

if __name__ == "__main__":
    main()
