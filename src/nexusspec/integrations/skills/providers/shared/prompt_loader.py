"""Carregamento de templates para geração de skills."""

from importlib.resources import files
from pathlib import Path

from ...contracts.provider import PromptTemplate


def _load_from_package() -> list[PromptTemplate]:
    templates_dir = files("nexusspec.templates")
    templates: list[PromptTemplate] = []
    for entry in templates_dir.iterdir():
        if not entry.name.endswith(".md"):
            continue
        if entry.name.startswith("_"):
            continue
        templates.append(
            PromptTemplate(
                name=entry.name,
                stem=Path(entry.name).stem,
                source_path=Path(entry.name),
                content=entry.read_text(encoding="utf-8"),
            )
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
            PromptTemplate(
                name=prompt_file.name,
                stem=prompt_file.stem,
                source_path=prompt_file,
                content=prompt_file.read_text(encoding="utf-8"),
            )
        )
    return templates
