import pytest
from pathlib import Path
from git import Repo
from coding_agent.utils.git_root import find_git_root, GitRootNotFoundError

@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary Git repository."""
    repo = Repo.init(tmp_path)
    (tmp_path / "test_file.txt").touch()
    repo.index.add(["test_file.txt"])
    repo.index.commit("Initial commit")
    return repo

def test_find_git_root_current_directory(git_repo):
    """Test finding Git root from the repository root."""
    repo_path = Path(git_repo.working_dir)
    assert find_git_root(repo_path) == repo_path

def test_find_git_root_subdirectory(git_repo):
    """Test finding Git root from a subdirectory."""
    repo_path = Path(git_repo.working_dir)
    subdir = repo_path / "subdir"
    subdir.mkdir()
    assert find_git_root(subdir) == repo_path

def test_find_git_root_nested_subdirectory(git_repo):
    """Test finding Git root from a nested subdirectory."""
    repo_path = Path(git_repo.working_dir)
    nested_dir = repo_path / "dir1" / "dir2" / "dir3"
    nested_dir.mkdir(parents=True)
    assert find_git_root(nested_dir) == repo_path

def test_find_git_root_no_arg(git_repo, monkeypatch):
    """Test finding Git root when no argument is provided (uses current directory)."""
    repo_path = Path(git_repo.working_dir)
    monkeypatch.chdir(repo_path)
    assert find_git_root() == repo_path

def test_find_git_root_non_git_directory(tmp_path):
    """Test behavior when not in a Git repository."""
    non_git_dir = tmp_path / "not_git"
    non_git_dir.mkdir()
    with pytest.raises(GitRootNotFoundError):
        find_git_root(non_git_dir)

def test_find_git_root_relative_path(git_repo):
    """Test finding Git root using a relative path."""
    repo_path = Path(git_repo.working_dir)
    subdir = repo_path / "subdir"
    subdir.mkdir()
    relative_path = Path("subdir")
    with pytest.raises(GitRootNotFoundError):
        find_git_root(relative_path)