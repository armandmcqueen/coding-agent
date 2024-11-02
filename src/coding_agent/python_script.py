import uuid
from pathlib import Path
from rich.console import Console
import datetime
import shutil

from coding_agent.serialization.python_file import PythonFile
from coding_agent.sh import Runner, ProcessOutput

console = Console()


StdOut = str
StdErr = str

class AtomicPythonScript:
    # The interface for running a Python script with a start and end.
    # This only consider the situation where the environment is valid and the code is terminating, so we can
    # look at the process as: execute() -> (error?, stdout, stderr)
    # Would be good to add a timeout?
    def __init__(self, file: PythonFile, tmp_dir_base: Path = Path(".")):
        file_stem = file.file_name.split(".")[0]
        # Get time as isoformat
        timestamp = datetime.datetime.now().isoformat()
        self._tmp_dir = tmp_dir_base / f"exec-{file_stem}-{timestamp}"
        self._tmp_dir.mkdir(parents=True, exist_ok=False)
        self.file = file
        self.script_location = self.file.save_to_file(base_path=self._tmp_dir)

    def run(self, add_timestamps: bool = False) -> ProcessOutput:
        runner = Runner(add_timestamps=add_timestamps)
        runner.cd(self._tmp_dir)
        result = runner.run(f"python {self.file.file_name}")
        # Write stdout and stderr to files in the tmp directory
        with open(self._tmp_dir / "stdout.txt", "w") as f:
            f.write(result.stdout)
        with open(self._tmp_dir / "stderr.txt", "w") as f:
            f.write(result.stderr)
        # Write the return code to a file in the tmp directory
        with open(self._tmp_dir / "returncode.txt", "w") as f:
            f.write(str(result.returncode))
        return result

    def cleanup(self):
        shutil.rmtree(self._tmp_dir)

    def tmp_dir(self):
        return self._tmp_dir