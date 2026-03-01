import typer
from buildagents.generator import create_project

app = typer.Typer(
    name="buildagents",
    help="🔥 Production-ready scaffolder for Agentic AI applications",
    add_completion=False,
)


@app.command()
def create(
    name: str = typer.Argument(..., help="Name of your agentic AI project"),
    author: str = typer.Option("Your Name", "--author", "-a", help="Your name"),
    description: str = typer.Option(
        "An Agentic AI Application",
        "--description",
        "-d",
        help="Project description",
    ),
):
    """
    Scaffold a production-ready Agentic AI project.

    Example:
        buildagents create my-agent-app
        buildagents create my-agent-app --author "John" --description "My AI Agent"
    """
    typer.echo(f"\n🚀 Creating project: {name}")
    create_project(name=name, author=author, description=description)


@app.command()
def version():
    """Show the current version of buildagents."""
    from buildagents import __version__
    typer.echo(f"buildagents v{__version__}")


if __name__ == "__main__":
    app()