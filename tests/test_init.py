from pathlib import Path

from nexusspec import cli


EXPECTED_FILES = [
    "docs/prd/prd.md",
    "docs/prd/personas.md",
    "docs/prd/metrics.md",
    "docs/architecture/architecture.md",
    "docs/architecture/epics.md",
    "features/specs/.gitkeep",
    "features/done/.gitkeep",
    "README.md",
]


def test_init_cria_estrutura_sem_abrir_editor(runner, tmp_path, monkeypatch, no_editor):
    monkeypatch.setattr(cli, "_select_tool", lambda: None)

    result = runner.invoke(cli.main, ["init", "meu-projeto", "--target", str(tmp_path)])

    assert result.exit_code == 0, result.output
    project_dir = tmp_path / "meu-projeto"
    for relative in EXPECTED_FILES:
        assert (project_dir / relative).exists(), relative
    assert cli._is_nexusspec_project(project_dir)
    assert no_editor == []
    for skills_dir in cli.SKILLS_TOOL_DIRS.values():
        assert not (project_dir / skills_dir).exists()


def test_init_gera_skills_da_ferramenta_escolhida(runner, tmp_path, monkeypatch, no_editor):
    monkeypatch.setattr(cli, "_select_tool", lambda: "Claude Code")

    result = runner.invoke(cli.main, ["init", "meu-projeto", "--target", str(tmp_path)])

    assert result.exit_code == 0, result.output
    project_dir = tmp_path / "meu-projeto"
    assert (project_dir / ".claude" / "commands" / "prd.md").exists()
    assert len(no_editor) == 1
    assert no_editor[0][1] == str(project_dir)


def test_init_falha_em_pasta_nao_vazia_sem_force(runner, tmp_path, monkeypatch, no_editor):
    monkeypatch.setattr(cli, "_select_tool", lambda: None)
    existing = tmp_path / "meu-projeto"
    existing.mkdir()
    (existing / "arquivo.txt").write_text("x")

    result = runner.invoke(cli.main, ["init", "meu-projeto", "--target", str(tmp_path)])
    assert result.exit_code == 1

    result = runner.invoke(cli.main, ["init", "meu-projeto", "--target", str(tmp_path), "--force"])
    assert result.exit_code == 0, result.output
    assert (existing / "arquivo.txt").exists()
    assert cli._is_nexusspec_project(existing)


def test_readme_gerado_usa_specify(runner, tmp_path, monkeypatch, no_editor):
    monkeypatch.setattr(cli, "_select_tool", lambda: None)
    runner.invoke(cli.main, ["init", "p", "--target", str(tmp_path)])

    readme = (tmp_path / "p" / "README.md").read_text(encoding="utf-8")
    assert "**specify**" in readme
    assert "techspec" not in readme
