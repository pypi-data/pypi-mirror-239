import argparse
import shutil
import sys
from repotofile.utils import get_repo_name_from_url, sanitize_config_files, create_output_file
from repotofile.git_operations import clone_repo

def main():
    parser = argparse.ArgumentParser(description='CLI tool to clone GitHub repos using Git, optionally sanitize config files, and generate a text file.')
    parser.add_argument('url', help='URL of the GitHub repository to clone')
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

    # Step 1: Clone the repo
    try:
        repo_name = get_repo_name_from_url(args.url)
        ignore_patterns = args.ignore_files.split(',') if args.ignore_files else []
        ignore_dirs = args.ignore_dirs.split(',') if args.ignore_dirs else []
        success = clone_repo(args.url, args.branch, repo_name)
        if not success:
            raise Exception("Failed to clone the repository. Please check the URL and branch/tag name.")
        
        # Step 2: Sanitize configuration files
        sanitize_config_files(repo_name, ignore_patterns, additional_ignore_dirs=ignore_dirs)

        # Step 3: Generate the output file
        if args.output is None:
            output_file = f'{repo_name}.txt'
        else:
            output_file = args.output

        create_output_file(repo_name, output_file)

        # Step 4: Cleanup repo_dir
        shutil.rmtree(repo_name)

        print(f"Repository contents have been successfully written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
        
