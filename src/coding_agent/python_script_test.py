import pytest
from pathlib import Path
from coding_agent.serialization.python_file import PythonFile
from coding_agent.sh import ProcessOutput
from coding_agent.utils.data import data_dir
from coding_agent.python_script import AtomicPythonScript

execution_dir = data_dir() / "python_scripts/executions"

@pytest.fixture
def hello_world_script():
    file_name = "example.py"
    script_dir = data_dir() / "python_scripts"
    return PythonFile.from_file(file_name, base_path=script_dir)

def test_atomic_python_script_run(hello_world_script):
    # Create an instance of AtomicPythonScript
    atomic_script = AtomicPythonScript(hello_world_script, tmp_dir_base=execution_dir)

    # Run the script
    result = atomic_script.run()

    # Check if the result is a ProcessOutput
    assert isinstance(result, ProcessOutput)

    # Check if the script executed successfully
    assert result.returncode == 0

    # Check if the output matches the expected "Hello, Example World!"
    assert result.stdout.strip() == "Hello, Example World!"

    # Check if there's no error output
    assert result.stderr == ""

    # Cleanup the temporary directory
    atomic_script.cleanup()

def test_atomic_python_script_run_with_timestamps(hello_world_script):
    # Create an instance of AtomicPythonScript
    atomic_script = AtomicPythonScript(hello_world_script, tmp_dir_base=execution_dir)

    # Run the script with timestamps
    result = atomic_script.run(add_timestamps=True)

    # Check if the result is a ProcessOutput
    assert isinstance(result, ProcessOutput)

    # Check if the script executed successfully
    assert result.returncode == 0

    # Check if the output contains "Hello, Example World!" (ignoring timestamps)
    assert len(result.stdout.strip()) > len("Hello, Example World!")
    assert "Hello, Example World!" in result.stdout

    # Check if there's no error output
    assert result.stderr == ""

    # Cleanup the temporary directory
    atomic_script.cleanup()

def test_atomic_python_script_tmp_dir_creation_and_cleanup(hello_world_script):
    # Create an instance of AtomicPythonScript
    atomic_script = AtomicPythonScript(hello_world_script, tmp_dir_base=execution_dir)

    # Check if the temporary directory was created
    assert atomic_script._tmp_dir.exists()
    assert atomic_script._tmp_dir.is_dir()

    # Check if the Python file was saved in the temporary directory
    assert (atomic_script._tmp_dir / "example.py").exists()
    assert (atomic_script._tmp_dir / "example.py").is_file()

    # Cleanup the temporary directory
    atomic_script.cleanup()

    # Check if the temporary directory was removed
    assert not atomic_script._tmp_dir.exists()
    assert not atomic_script._tmp_dir.is_dir()

