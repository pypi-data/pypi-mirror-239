import unittest
from repotofile.utils import sanitize_config_files, create_output_file, should_ignore_file, get_repo_name_from_url, should_ignore_path
from repotofile.ignored_patterns import DEFAULT_IGNORE_DIRS, DEFAULT_IGNORE_PATTERNS
import os
import tempfile


class TestUtils(unittest.TestCase):
    def setUp(self):
        # Set up a temporary directory with some files
        self.test_dir = tempfile.TemporaryDirectory()
        self.repo_dir = os.path.join(self.test_dir.name, 'repo')
        os.mkdir(self.repo_dir)
        os.mkdir(os.path.join(self.repo_dir, 'src'))

        # Create dummy files to represent code and config files
        self.code_files = ['main.py', 'utils.py']
        self.config_files = ['config.yaml', 'settings.json']
        self.nested_code_files = ['src/main.py', 'src/utils.py']
        
        for filename in self.code_files + self.config_files:
            with open(os.path.join(self.repo_dir, filename), 'w') as f:
                f.write(f'dummy content for {filename}')

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_create_output_file_with_encodings(self):
        # Create dummy files with different encodings
        encoded_files = {
            'utf8.txt': 'utf-8 content',
            'latin1.txt': 'latin-1 content',
        }
        for filename, content in encoded_files.items():
            with open(os.path.join(self.repo_dir, filename), 'w', encoding=filename.split('.')[0]) as f:
                f.write(content)

        output_file_path = os.path.join(self.test_dir.name, 'output.txt')
        create_output_file(self.repo_dir, output_file_path)

        # Verify the output file content
        with open(output_file_path, 'r', encoding='utf-8') as output_file:
            output_content = output_file.read()

        # Check for the presence of file content for different encodings
        for content in encoded_files.values():
            self.assertIn(content, output_content)

    def test_sanitize_config_files_with_additional_patterns(self):
        additional_patterns = ['*.log', '*.tmp']
        # Create additional dummy config files
        additional_config_files = ['debug.log', 'temp.tmp']
        for filename in additional_config_files:
            with open(os.path.join(self.repo_dir, filename), 'w') as f:
                f.write('dummy content')

        sanitize_config_files(self.repo_dir, additional_ignore_patterns=additional_patterns)

        # Verify that additional config files have been sanitized
        for filename in self.config_files + additional_config_files:
            with open(os.path.join(self.repo_dir, filename), 'r') as f:
                content = f.read()
                
                self.assertEqual(content, '# Content omitted for convenience\n')

    def test_should_ignore_file(self):
        self.assertTrue(should_ignore_file('config.yaml', DEFAULT_IGNORE_PATTERNS))
        self.assertFalse(should_ignore_file('main.py', DEFAULT_IGNORE_PATTERNS))
    
        # Test nested files
        self.assertTrue(should_ignore_file('src/package-lock.json', DEFAULT_IGNORE_PATTERNS))
        self.assertTrue(should_ignore_file('src/anyfolder/another/package-lock.json', DEFAULT_IGNORE_PATTERNS))

        self.assertFalse(should_ignore_file('src/anything.py', DEFAULT_IGNORE_PATTERNS))

        # Test starting patterns
        self.assertTrue(should_ignore_file('.prettierrc.js', ['.prettierrc.*']))
        # Test additional patterns
        additional_patterns = ['*.log', '*.tmp']
        self.assertTrue(should_ignore_file('debug.log', additional_patterns))
        self.assertFalse(should_ignore_file('notes.txt', additional_patterns))

    def test_should_ignore_path(self):
        self.assertTrue(should_ignore_path('./node_modules/', DEFAULT_IGNORE_DIRS))
        self.assertTrue(should_ignore_path('.git/', DEFAULT_IGNORE_DIRS))
        self.assertTrue(should_ignore_path('.git/source/index/', DEFAULT_IGNORE_DIRS))
        self.assertTrue(should_ignore_path('./openapi-codegen/.git/', DEFAULT_IGNORE_DIRS))
        self.assertTrue(should_ignore_path('src/anyfolder/another/node_modules/', DEFAULT_IGNORE_DIRS))

        self.assertFalse(should_ignore_path('src/anything.py', DEFAULT_IGNORE_DIRS))

    def test_get_repo_name_from_url(self):
        self.assertEqual(get_repo_name_from_url('https://github.com/user/repo.git'), 'repo')
        self.assertEqual(get_repo_name_from_url('https://github.com/user/repo'), 'repo')
        # Test with URLs that have extra slashes or URL parameters
        self.assertEqual(get_repo_name_from_url('https://github.com/user/repo/'), 'repo')
        self.assertEqual(get_repo_name_from_url('https://github.com/user/repo.git?some_param=value'), 'repo')

class TestSanitizeConfigFiles(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with a nested structure
        self.test_dir = tempfile.TemporaryDirectory()
        self.nested_dir = os.path.join(self.test_dir.name, 'nested')
        os.makedirs(self.nested_dir)

        # Create dummy config files in both the root and nested directories
        self.root_config_file = os.path.join(self.test_dir.name, 'root_config.json')
        with open(self.root_config_file, 'w') as f:
            f.write('root config data')

        self.nested_config_file = os.path.join(self.nested_dir, 'nested_config.json')
        with open(self.nested_config_file, 'w') as f:
            f.write('nested config data')

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_sanitize_nested_files(self):
        # Define the ignore patterns
        ignore_patterns = ['*.json']

        # Sanitize config files
        sanitize_config_files(self.test_dir.name, ignore_patterns)

        # Verify that root config file was sanitized
        with open(self.root_config_file, 'r') as f:
            self.assertEqual(f.read(), '# Content omitted for convenience\n')

        # Verify that nested config file was sanitized
        with open(self.nested_config_file, 'r') as f:
            self.assertEqual(f.read(), '# Content omitted for convenience\n')