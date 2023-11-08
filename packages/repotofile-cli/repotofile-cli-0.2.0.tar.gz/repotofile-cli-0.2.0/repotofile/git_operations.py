import subprocess

def clone_repo(url, branch=None, output_dir='repo_dir'):
    # Clone the repository into the specified directory
    clone_command = ['git', 'clone', '--depth', '1']
    if branch:  # If a specific branch or tag is given, use it
        clone_command += ['--branch', branch]
    clone_command += [url, output_dir]

    try:
        subprocess.run(clone_command, check=True)
        print(f'Repository cloned into {output_dir}')
    except subprocess.CalledProcessError as e:
        print(f'Error cloning repository: {e}')
        return False

    return True