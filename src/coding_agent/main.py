import pytest
from pathlib import Path
from coding_agent.serialization.python_file import PythonFile
from coding_agent.sh import ProcessOutput
from coding_agent.utils.data import data_dir
from coding_agent.python_script import AtomicPythonScript
from rich.console import Console

console = Console()

execution_dir = data_dir() / "python_scripts/executions"

def triangle_numbers_script():
    file_name = "triangle_numbers.py"
    script_dir = data_dir() / "python_scripts"
    code = PythonFile.from_file(file_name, base_path=script_dir)
    script = AtomicPythonScript(code, tmp_dir_base=execution_dir / "triangle_numbers")
    out = script.run()
    # Print stdout in green and stderr in red
    console.print("STDOUT:", style="bold blue")
    console.print(out.stdout.strip(), style="green")
    console.print("STDERR:", style="bold blue")
    console.print(out.stderr.strip(), style="red")

    # Cleanup the temporary directory
    script.cleanup()



if __name__ == '__main__':
    triangle_numbers_script()