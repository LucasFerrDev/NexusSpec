"""Service de geração de skills por provider."""

from pathlib import Path

from ..contracts.provider import GenerationReport
from ..factories.provider_factory import SkillProviderFactory
from ..providers.shared.prompt_loader import load_prompt_templates


class SkillsGeneratorService:
    """Orquestra a geração de skills a partir dos prompts do projeto."""

    def generate_for_tool(
        self,
        project_dir: Path,
        tool_choice: str,
        overwrite: bool = False,
    ) -> GenerationReport | None:
        provider = SkillProviderFactory.from_tool_choice(tool_choice)
        if provider is None:
            return None

        prompts = load_prompt_templates(project_dir=project_dir)
        if not prompts:
            return None

        return provider.generate(project_dir=project_dir, prompts=prompts, overwrite=overwrite)

