"""Factory para resolver provider de skills por ferramenta selecionada."""

from ..contracts.provider import SkillProvider
from ..providers.antigravity import AntigravitySkillProvider
from ..providers.copilot import CopilotSkillProvider
from ..providers.claude_code import ClaudeCodeSkillProvider
from ..providers.cursor import CursorSkillProvider


class SkillProviderFactory:
    """Resolve providers de skills por escolha de menu."""

    _providers: dict[str, SkillProvider] = {
        "copilot": CopilotSkillProvider(),
        "claude_code": ClaudeCodeSkillProvider(),
        "cursor": CursorSkillProvider(),
        "antigravity": AntigravitySkillProvider(),
    }

    _tool_to_provider_key: dict[str, str] = {
        "vscode": "copilot",
        "GitHub Copilot": "copilot",
        "VSCode": "copilot",
        "Copilot CLI": "copilot",
        "claude": "claude_code",
        "Claude Code": "claude_code",
        "cursor": "cursor",
        "Cursor": "cursor",
        "antigravity": "antigravity",
        "Antigravity": "antigravity",
    }

    @classmethod
    def from_tool_choice(cls, tool_choice: str) -> SkillProvider | None:
        provider_key = cls._tool_to_provider_key.get(tool_choice)
        if not provider_key:
            return None
        return cls._providers.get(provider_key)
