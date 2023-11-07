import argparse
import sys
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
    try:
        repo_dir = 'repo_dir'  # This would be a temporary directory created for cloning
        success = clone_repo(args.url, args.branch, repo_dir)
        if not success:
            raise Exception("Failed to clone the repository. Please check the URL and branch/tag name.")
        
        # Step 2 (optional): Sanitize configuration files if --no-config is set
        if args.no_config:
            sanitize_config_files(repo_dir)

        # Step 3: Generate the output file
        create_output_file(repo_dir, args.output)

        print(f"Repository contents have been successfully written to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    main()