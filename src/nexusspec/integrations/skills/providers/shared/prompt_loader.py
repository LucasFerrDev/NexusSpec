"""Carregamento de utilities para geração de skills."""

from pathlib import Path

from ...contracts.provider import PromptTemplate


def load_prompt_templates(project_dir: Path, prompts_dir: str = "utilities") -> list[PromptTemplate]:
    """Lê os templates .md do projeto e retorna templates ordenados."""
    base_dir = project_dir / prompts_dir
    if not base_dir.exists():
        return []

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
