from typing import Optional
import typer
from buildagents.core.generator import create_project, GeneratorError

app = typer.Typer(
    name="buildagents",
    help="🔥 Production-ready scaffolder for Agentic AI applications",
    add_completion=False,
)


@app.command()
def create(
    name: Optional[str] = typer.Argument(None, help="Name of your agentic AI project"),
    author: Optional[str] = typer.Option(None, "--author", "-a", help="Your name"),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        "-d",
        help="Project description",
    ),
    template: Optional[str] = typer.Option(
        None,
        "--template",
        "-t",
        help="Choose a scaffold template",
    ),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Run in interactive mode"
    ),
):
    """
    Scaffold a production-ready Agentic AI project.

    Example:
        buildagents create my-agent-app
        buildagents create .
        buildagents create my-agent-app --template minimal
        buildagents create --interactive
    """
    if name is None:
        typer.echo("\n🛠️ No project name provided. Starting interactive setup...")
        name = typer.prompt("Project name", default="my-agent-app")
        interactive = True  # Default to interactive if name was missing

    if interactive:
        author = typer.prompt("Author name", default=author or "Your Name")
        description = typer.prompt("Project description", default=description or "An Agentic AI Application")
        template = typer.prompt("Select template (base/minimal)", default=template or "base")
    else:
        author = author or "Your Name"
        description = description or "An Agentic AI Application"
        template = template or "base"
    is_dot = name == "."
    if is_dot:
        import os
        display_name = os.path.basename(os.getcwd())
    else:
        display_name = name

    typer.echo(f"\n🚀 Creating project: {display_name} using template '{template}'")
    
    try:
        create_project(name=name, author=author, description=description, template=template)
        
        typer.echo(f"✅ Project '{display_name}' created successfully!")
        typer.echo(f"\n📂 Next steps:")
        if not is_dot:
            typer.echo(f"   cd {name}")
        typer.echo(f"   cp .env.example .env")
        typer.echo(f"   pip install -r requirements.txt")
        typer.echo(f"   uvicorn main:app --reload")
        typer.echo(f"\n🔥 Build something dangerous.\n")
        
    except GeneratorError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ An unexpected error occurred: {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def version():
    """Show the current version of buildagents."""
    from buildagents import __version__
    typer.echo(f"buildagents v{__version__}")


if __name__ == "__main__":
    app()