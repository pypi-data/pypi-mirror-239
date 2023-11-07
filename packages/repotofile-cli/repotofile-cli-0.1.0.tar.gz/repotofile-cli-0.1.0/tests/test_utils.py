import unittest
from repotofile.utils import sanitize_config_files, create_output_file
import os
import tempfile


class TestUtils(unittest.TestCase):
    def setUp(self):
        # Set up a temporary directory with some files
        self.test_dir = tempfile.TemporaryDirectory()
        self.repo_dir = os.path.join(self.test_dir.name, 'repo')
        os.mkdir(self.repo_dir)

        # Create dummy files to represent code and config files
        self.code_files = ['main.py', 'utils.py']
        self.config_files = ['config.yaml', 'settings.json']
        
        for filename in self.code_files + self.config_files:
            with open(os.path.join(self.repo_dir, filename), 'w') as f:
                f.write(f'dummy content for {filename}')

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_create_output_file(self):
        output_file_path = os.path.join(self.test_dir.name, 'output.txt')

        # Optionally sanitize config files before running create_output_file
        sanitize_config_files(self.repo_dir)

        create_output_file(self.repo_dir, output_file_path)

        # Verify the output file content
        with open(output_file_path, 'r') as output_file:
            output_content = output_file.read()

        # Check for the presence of code file content
        for filename in self.code_files:
            self.assertIn(f'dummy content for {filename}', output_content)

        # Check that config files have been sanitized
        for filename in self.config_files:
            self.assertNotIn(f'dummy content for {filename}', output_content)
            self.assertIn('# Content omitted for convenience', output_content)

    def test_sanitize_config_files(self):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create dummy config files
            config_files = ['config.yaml', 'settings.json']
            for filename in config_files:
                with open(os.path.join(tmpdirname, filename), 'w') as f:
                    f.write('dummy content')

            # Run the sanitize_config_files function on the temp directory
            sanitize_config_files(tmpdirname)

            # Check if each config file was sanitized properly
            for filename in config_files:
                with open(os.path.join(tmpdirname, filename), 'r') as f:
                    content = f.read()
                    self.assertEqual(content, '# Content omitted for convenience\n')




