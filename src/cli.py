import typer
from invoke import Context
from rich.console import Console

app = typer.Typer()
console = Console()
c = Context()
c.config.run.echo = True

# pylint: disable=pointless-exception-statement
# pylint: disable=inconsistent-return-statements
def run(cmd):
    try:
        out = c.run(cmd)
        return out
    except Exception:
        console.print(f"[red]Error during '{cmd}'[/red]")
        typer.Abort()
# pylint: enable=pointless-exception-statement
# pylint: enable=inconsistent-return-statements


@app.command(help="Build the wheel for the project")
def flit_build():
    run("flit build")


@app.command(help="Publish the wheel to PyPI")
def flit_publish():
    run("flit publish")


@app.command()
def fmt():
    run("uv run ruff format")


@app.command(help="Run the ruff linter (fast)")
def lint():
    run("uv run ruff check")

@app.command(help="Run all linters including slow pylint")
def lint_full():
    run("uv run ruff check")
    run("uv run pylint cli.py")
    run("uv run pylint src")

@app.command()
def typecheck():
    run("uv run mypy src")


if __name__ == "__main__":
    app()
