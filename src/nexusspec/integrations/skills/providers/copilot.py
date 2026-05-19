"""Provider de skills para GitHub Copilot/VSCode."""

from pathlib import Path

from ..contracts.provider import GenerationReport, PromptTemplate


class CopilotSkillProvider:
    """Gera `.github/skills/<skill>/SKILL.md` para cada prompt."""

    name = "GitHub Copilot / VSCode"

    def generate(
        self,
        project_dir: Path,
        prompts: list[PromptTemplate],
        overwrite: bool = False,
    ) -> GenerationReport:
        created_files: list[Path] = []
        skipped_files: list[Path] = []

        for prompt in prompts:
            skill_file = project_dir / ".github" / "skills" / prompt.stem / "SKILL.md"
            skill_file.parent.mkdir(parents=True, exist_ok=True)

            if skill_file.exists() and not overwrite:
                skipped_files.append(skill_file)
                continue

            skill_file.write_text(prompt.content, encoding="utf-8")
            created_files.append(skill_file)

        return GenerationReport(
            provider_name=self.name,
            created_files=created_files,
            skipped_files=skipped_files,
        )

