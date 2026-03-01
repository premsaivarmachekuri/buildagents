import shutil
from pathlib import Path
import typer


TEMPLATES_DIR = Path(__file__).parent / "templates"


def create_project(name: str, author: str, description: str) -> None:
    template_dir = TEMPLATES_DIR / "base"
    target_dir = Path.cwd() / name

    # Guard: don't overwrite existing folder
    if target_dir.exists():
        typer.echo(f"❌ Directory '{name}' already exists. Choose a different name.")
        raise typer.Exit(code=1)

    # Copy entire template tree
    shutil.copytree(template_dir, target_dir)

    # Replace placeholders in all text files
    _replace_placeholders(
        target_dir,
        project_name=name,
        author=author,
        description=description,
    )

    typer.echo(f"✅ Project '{name}' created successfully!")
    typer.echo(f"\n📂 Next steps:")
    typer.echo(f"   cd {name}")
    typer.echo(f"   cp .env.example .env")
    typer.echo(f"   pip install -r requirements.txt")
    typer.echo(f"   uvicorn main:app --reload")
    typer.echo(f"\n🔥 Build something dangerous.\n")


def _replace_placeholders(
    directory: Path,
    project_name: str,
    author: str,
    description: str,
) -> None:
    """Walk all files and replace {{placeholders}} with actual values."""
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{AUTHOR}}": author,
        "{{DESCRIPTION}}": description,
    }

    # File extensions to process as text
    text_extensions = {".py", ".txt", ".md", ".env", ".yml", ".yaml", ".toml", ""}

    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix in text_extensions:
            try:
                content = file_path.read_text(encoding="utf-8")
                for placeholder, value in replacements.items():
                    content = content.replace(placeholder, value)
                file_path.write_text(content, encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or unreadable files
                pass