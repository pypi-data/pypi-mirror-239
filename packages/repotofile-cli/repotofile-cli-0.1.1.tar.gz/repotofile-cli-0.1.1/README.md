# repotofile-cli

`repotofile-cli` is a very light weight command-line tool that allows users to download a GitHub repository and generate a text file containing the repository's code, excluding files specified in `.gitignore`. It's particularly useful for code analysis, backups, and easy sharing of code snapshots.

## Features

- Clone any public GitHub repository.
- Optionally exclude configuration files, replacing their content with a placeholder.
- Generate a single text or markdown file with the entire codebase, neatly separated by files.
- Easy to install and use with a simple command.

## Installation

To install `repotofile-cli`, ensure you have Python installed on your system, then run:

```bash
pip install repotofile-cli
```

## Usage

After installation, you can use the `repotofile` command or its shorthand `rtf`:

```bash
repotofile <repository-url> [options]
```

or

```bash
rtf <repository-url> [options]
```

### Options

- `-b`, `--branch` : Specify a branch or tag to download. Defaults to the default branch of the repository.
- `-o`, `--output` : Custom output file name or path. Defaults to 'repository_contents.txt'.
- `--no-config` : Replace the content of configuration files with a placeholder comment.

### Examples

Cloning a repository and generating the default output file:

```bash
repotofile https://github.com/user/repo
```

Cloning a specific branch:

```bash
repotofile https://github.com/user/repo -b feature-branch
```

Generating a custom output file:

```bash
repotofile https://github.com/user/repo -o ~/Documents/repo_snapshot.txt
```

Excluding configuration files:

```bash
repotofile https://github.com/user/repo --no-config
```

## Contributing

Contributions to `repotofile-cli` are welcome! Please read our contributing guidelines (link to guidelines) to get started.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Maurits Bos - <maurits.bos@gmail.com>
Project Link: <https://github.com/mbbrainz/repotofile-cli>
