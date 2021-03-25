import os
import pathlib
import subprocess


def has_git():
    return subprocess.run(
        ['git', '--version'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0


def is_git_dir(path: pathlib.Path, check_parents=False):
    # First check fast is_dir, then do a git status if false
    if (path / '.git').is_dir():
        return True
    else:
        return subprocess.run(
            ['git', 'status'], cwd=path,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ).returncode == 0
