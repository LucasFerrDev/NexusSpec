"""Contratos de providers de skills."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class PromptTemplate:
    """Representa um template carregado do projeto ou do pacote.

    ``skill_name`` e ``description`` vêm do frontmatter do template, quando
    presentes; os providers usam valores próprios como fallback.
    """

    name: str
    stem: str
    source_path: Path
    content: str
    skill_name: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class GenerationReport:
    """Resultado de geração de arquivos de skill."""

    provider_name: str
    created_files: list[Path]
    skipped_files: list[Path]


class SkillProvider(Protocol):
    """Contrato para providers específicos por plataforma."""

    name: str

    def generate(
        self,
        project_dir: Path,
        prompts: list[PromptTemplate],
        overwrite: bool = False,
    ) -> GenerationReport:
        """Gera arquivos de skills da plataforma."""
