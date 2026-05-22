"""Provider de commands para Claude Code."""

from pathlib import Path

from ..contracts.provider import GenerationReport, PromptTemplate


class ClaudeCodeSkillProvider:
    """Gera `.claude/commands/<prompt>.md` a partir dos prompts do projeto."""

    name = "Claude Code"

    def generate(
        self,
        project_dir: Path,
        prompts: list[PromptTemplate],
        overwrite: bool = False,
    ) -> GenerationReport:
        created_files: list[Path] = []
        skipped_files: list[Path] = []

        for prompt in prompts:
            command_file = project_dir / ".claude" / "commands" / prompt.name
            command_file.parent.mkdir(parents=True, exist_ok=True)

            if command_file.exists() and not overwrite:
                skipped_files.append(command_file)
                continue

            command_file.write_text(prompt.content, encoding="utf-8")
            created_files.append(command_file)

        return GenerationReport(
            provider_name=self.name,
            created_files=created_files,
            skipped_files=skipped_files,
        )
