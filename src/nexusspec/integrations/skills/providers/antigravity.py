"""Provider de skills para Antigravity."""

from pathlib import Path

from ..contracts.provider import GenerationReport, PromptTemplate


class AntigravitySkillProvider:
    """Gera `.agent/skills/<skill>/SKILL.md` com metadados básicos."""

    name = "Antigravity"

    def generate(
        self,
        project_dir: Path,
        prompts: list[PromptTemplate],
        overwrite: bool = False,
    ) -> GenerationReport:
        created_files: list[Path] = []
        skipped_files: list[Path] = []

        for prompt in prompts:
            skill_file = project_dir / ".agent" / "skills" / prompt.stem / "SKILL.md"
            skill_file.parent.mkdir(parents=True, exist_ok=True)

            if skill_file.exists() and not overwrite:
                skipped_files.append(skill_file)
                continue

            content = (
                "---\n"
                f"name: {prompt.stem}\n"
                "description: Skill generated automatically by NexusSpec\n"
                "---\n\n"
                f"{prompt.content}"
            )
            skill_file.write_text(content, encoding="utf-8")
            created_files.append(skill_file)

        return GenerationReport(
            provider_name=self.name,
            created_files=created_files,
            skipped_files=skipped_files,
        )

