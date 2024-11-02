from pathlib import Path
from coding_agent.utils.git_root import find_git_root

def data_dir() -> Path:
    git_root = find_git_root(Path(__file__).parent)
    return git_root / "data"
