import typer
from buildagents.core.generator import create_project, GeneratorError

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
    template: str = typer.Option(
        "base",
        "--template",
        "-t",
        help="Choose a scaffold template",
    ),
):
    """
    Scaffold a production-ready Agentic AI project.

    Example:
        buildagents create my-agent-app
        buildagents create .
        buildagents create my-agent-app --template minimal
        buildagents create my-agent-app --author "John" --description "My AI Agent" --template base
    """
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