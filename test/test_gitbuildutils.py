import os
import pathlib
import subprocess
import tempfile
import unittest

# Hack to get the root of the project into the Python path without installing
# the package, or resorting to virtual environments. Adding the current and the
# parent directory to the Python path, so tests can run successfully from
# either the root or test dir.
import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')

from gitbuildutils import *


class TestGitUtil(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.git_repo_dir = tempfile.TemporaryDirectory()
        subprocess.run(['git', 'init', '-q'], cwd=cls.git_repo_dir.name)

        cls.not_git_repo_dir = tempfile.TemporaryDirectory()

        for i in [cls.git_repo_dir, cls.not_git_repo_dir]:
            # TODO use pathlib?
            os.makedirs(f'{i.name}/sub_dir')

        cls.git_repo_path = pathlib.Path(cls.git_repo_dir.name)
        cls.not_git_repo_path = pathlib.Path(cls.not_git_repo_dir.name)

    def test_has_git(self):
        """Test the has_git() function.

        The system running the test could or could not have git installed.
        Assert for a return value of either True or False.
        """
        self.assertIn(has_git(), [True, False])

    def test_is_git_dir(self):
        """Test the is_git_dir() function using subtests.
        """

        def sub_test(git_dir, check_parent, subdir):
            test_dir = self.git_repo_path if git_dir else \
                self.not_git_repo_path

            if sub_dir:
                test_dir /= 'sub_dir'

            if git_dir:
                self.assertTrue(is_git_dir(test_dir, check_parent))
            else:
                self.assertFalse(is_git_dir(test_dir, check_parent))

        for git_dir in [True, False]:
            for check_parent in [True, False]:
                for sub_dir in [True, False]:
                    with self.subTest(
                        git_dir=git_dir,
                        check_parent=check_parent,
                        sub_dir=sub_dir
                    ):
                        sub_test(git_dir, check_parent, sub_dir)


if __name__ == "__main__":
    unittest.main()
