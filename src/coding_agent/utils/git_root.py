from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError
from pathlib import Path

class GitRootNotFoundError(Exception):
    pass

def find_git_root(path: Path | None = None) -> Path:
    if path is None:
        path = Path(".")
    try:
        repo = Repo(path, search_parent_directories=True)
        return Path(repo.git.rev_parse("--show-toplevel"))
    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        raise GitRootNotFoundError(f"No Git repository found at or above {path}") from e