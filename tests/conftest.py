from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from nexusspec import cli
from nexusspec.integrations.skills.providers.shared.frontmatter import split_frontmatter

SKILL_STEMS = {"apply", "prd", "specify", "task", "verify"}


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Projeto NexusSpec vazio, definido como diretório de trabalho."""
    cli._create_docs_structure(tmp_path)
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def no_editor(monkeypatch: pytest.MonkeyPatch) -> list:
    """Impede que algum teste abra um editor de verdade; registra as chamadas."""
    calls: list = []

    def fake_try_open(commands, project_path):
        calls.append((commands, project_path))
        return True

    monkeypatch.setattr(cli, "_try_open", fake_try_open)
    return calls


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Valida o frontmatter com um parser YAML real e retorna (campos, corpo)."""
    content = path.read_text(encoding="utf-8")
    assert content.startswith("---\n"), f"{path} não começa com frontmatter"
    _, raw, body = content.split("---\n", 2)
    fields = yaml.safe_load(raw)
    assert isinstance(fields, dict)
    # Não pode existir um segundo bloco de frontmatter no corpo
    assert split_frontmatter(body.lstrip())[0] == {}
    return fields, body
