import subprocess

import pytest

from nexusspec import cli


class FakeRun:
    def __init__(self):
        self.calls: list[tuple[list[str], dict]] = []

    def __call__(self, parts, **kwargs):
        self.calls.append((parts, kwargs))
        return subprocess.CompletedProcess(parts, 0)


@pytest.fixture
def fake_run(monkeypatch) -> FakeRun:
    fake = FakeRun()
    monkeypatch.setattr(cli.subprocess, "run", fake)
    return fake


def _commands_for(label: str):
    return next(cmds for tool_label, cmds in cli.TOOLS if tool_label == label)


@pytest.mark.parametrize("label, binary", [("Claude Code", "claude"), ("Codex CLI", "codex")])
def test_cli_interativa_herda_o_terminal(fake_run, tmp_path, label, binary):
    assert cli._try_open(_commands_for(label), str(tmp_path))

    parts, kwargs = fake_run.calls[0]
    # Sem o caminho como argumento (seria lido como prompt) e com o projeto como cwd
    assert parts == [binary]
    assert kwargs == {"cwd": str(tmp_path)}


def test_editor_grafico_recebe_o_caminho(fake_run, tmp_path):
    assert cli._try_open(_commands_for("Cursor"), str(tmp_path))

    parts, kwargs = fake_run.calls[0]
    assert parts == ["cursor", str(tmp_path)]
    assert kwargs["stdout"] is subprocess.DEVNULL
