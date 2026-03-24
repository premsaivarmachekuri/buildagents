import shutil
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = Path(__file__).parent / "templates"


class GeneratorError(Exception):
    """Base error for generation logic."""
    pass


def create_project(name: str, author: str, description: str) -> Path:
    """
    Scaffold a new project from the base template.

    Args:
        name: Project folder name (or '.' for current dir)
        author: Project author name
        description: Project description

    Returns:
        Path to the created project.
    
    Raises:
        GeneratorError: If project creation fails.
    """
    template_dir = TEMPLATES_DIR / "base"
    
    if name == ".":
        target_dir = Path.cwd()
        project_name = target_dir.name
        is_dot = True
    else:
        target_dir = Path.cwd() / name
        project_name = name
        is_dot = False

    # Guard: don't overwrite existing folder (if not ".")
    if not is_dot and target_dir.exists():
        raise GeneratorError(f"Directory '{name}' already exists. Choose a different name.")

    # Copy entire template tree
    try:
        # Use dirs_exist_ok=True if users want to scaffold into an existing folder
        shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
    except Exception as e:
        raise GeneratorError(f"Failed to copy template: {str(e)}")

    # Replace placeholders using Jinja2
    context = {
        "PROJECT_NAME": project_name,
        "AUTHOR": author,
        "DESCRIPTION": description,
    }
    
    _process_templates(target_dir, context)

    return target_dir


def _process_templates(directory: Path, context: Dict[str, Any]) -> None:
    """Walk all files and render them with Jinja2."""
    template_env = Environment(loader=FileSystemLoader(str(directory)))

    # Extensions to process as templates
    text_extensions = {".py", ".txt", ".md", ".env", ".yml", ".yaml", ".toml", ""}

    for file_path in directory.rglob("*"):
        if not file_path.is_file():
            continue
        
        # Skip pycache and git if they were copied somehow
        if "__pycache__" in str(file_path):
            continue

        if file_path.suffix.lower() in text_extensions:
            try:
                # Get the relative path for Jinja2 loader
                rel_path = file_path.relative_to(directory).as_posix()
                template = template_env.get_template(rel_path)
                rendered_content = template.render(**context)
                file_path.write_text(rendered_content, encoding="utf-8")
            except Exception as e:
                # Log error or skip if it's not a valid template
                # Some files might have curly braces but not be valid Jinja (though unlikely in our templates)
                pass