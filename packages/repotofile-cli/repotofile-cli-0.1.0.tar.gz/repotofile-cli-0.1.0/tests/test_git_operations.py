import subprocess
import unittest
from unittest.mock import patch, Mock
from repotofile.git_operations import clone_repo
import os

class TestUtils(unittest.TestCase):
    @patch('repotofile.git_operations.subprocess.run')
    def test_clone_repo_success(self, mock_subproc_run):
        # Mock the subprocess run function to simulate a successful clone
        mock_subproc_run.return_value = Mock(returncode=0)  # Success return code

        # Call the clone_repo function with test parameters
        result = clone_repo('https://github.com/user/repo', 'master', 'repo_dir')

        # Check that the result is True indicating success
        self.assertTrue(result)

        # Ensure that subprocess.run was called with the correct parameters
        mock_subproc_run.assert_called_with(['git', 'clone', '--depth', '1', '--branch', 'master', 'https://github.com/user/repo', 'repo_dir'], check=True)

    @patch('repotofile.git_operations.subprocess.run')
    def test_clone_repo_failure(self, mock_subproc_run):
        # Mock the subprocess run function to simulate a clone failure
        mock_subproc_run.side_effect = subprocess.CalledProcessError(1, 'git clone')  # Failure scenario

        # Call the clone_repo function with test parameters
        result = clone_repo('https://github.com/user/repo', 'master', 'repo_dir')

        # Check that the result is False indicating failure
        self.assertFalse(result)
