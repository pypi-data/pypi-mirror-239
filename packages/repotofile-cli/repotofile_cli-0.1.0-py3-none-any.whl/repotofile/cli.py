import argparse
from utils import sanitize_config_files, create_output_file
from git_operations import clone_repo

def main():
    parser = argparse.ArgumentParser(description='CLI tool to clone GitHub repos using Git, optionally sanitize config files, and generate a text file.')
    parser.add_argument('url', help='URL of the GitHub repository to clone')
    parser.add_argument('-b', '--branch', help='Branch or tag to clone', default='master')
    parser.add_argument('-o', '--output', help='Custom output file name or path', default='repository_contents.txt')
    parser.add_argument('--no-config', help='Replace content of configuration files with a placeholder comment', action='store_true')

    args = parser.parse_args()

    # Step 1: Clone the repo
    repo_dir = 'repo_dir'  # This would be a temporary directory created for cloning
    if clone_repo(args.url, args.branch, repo_dir):
        # Step 2 (optional): Sanitize configuration files if --no-config is set
        if args.no_config:
            sanitize_config_files(repo_dir)
        # Steps for generating the output file will go here
        create_output_file(repo_dir, args.output)
        
if __name__ == "__main__":
    main()