"""Carregamento de templates para geração de skills."""

from importlib.resources import files
from pathlib import Path

from ...contracts.provider import PromptTemplate
from .frontmatter import split_frontmatter


def read_template_metadata(content: str) -> tuple[str | None, str | None]:
    """Lê ``name`` e ``description`` do frontmatter YAML de um template."""
    fields, _ = split_frontmatter(content)
    name = fields.get("name")
    description = fields.get("description")
    return (
        name if isinstance(name, str) and name else None,
        description if isinstance(description, str) and description else None,
    )


def _build_template(name: str, source_path: Path, content: str) -> PromptTemplate:
    skill_name, description = read_template_metadata(content)
    return PromptTemplate(
        name=name,
        stem=Path(name).stem,
        source_path=source_path,
        content=content,
        skill_name=skill_name,
        description=description,
    )


def _load_from_package() -> list[PromptTemplate]:
    templates_dir = files("nexusspec.templates")
    templates: list[PromptTemplate] = []
    for entry in templates_dir.iterdir():
        if not entry.name.endswith(".md"):
            continue
        if entry.name.startswith("_"):
            continue
        templates.append(
            _build_template(entry.name, Path(entry.name), entry.read_text(encoding="utf-8"))
        )
    return templates


def load_prompt_templates(project_dir: Path, prompts_dir: str = "prompts") -> list[PromptTemplate]:
    """Lê os templates .md do projeto e retorna templates ordenados."""
    base_dir = project_dir / prompts_dir
    if not base_dir.exists():
        return sorted(_load_from_package(), key=lambda t: t.name)

    templates: list[PromptTemplate] = []
    for prompt_file in sorted(base_dir.glob("*.md")):
        templates.append(
            _build_template(prompt_file.name, prompt_file, prompt_file.read_text(encoding="utf-8"))
        )
    return templates
