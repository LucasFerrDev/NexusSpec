from pathlib import Path

import pytest

from nexusspec import cli

from conftest import SKILL_STEMS, parse_frontmatter

SKILL_PATHS = {
    "vscode": lambda stem: Path(".github/skills") / stem / "SKILL.md",
    "claude": lambda stem: Path(".claude/commands") / f"{stem}.md",
    "codex": lambda stem: Path(".agents/skills") / stem / "SKILL.md",
    "cursor": lambda stem: Path(".cursor/rules") / f"{stem}.mdc",
    "antigravity": lambda stem: Path(".agent/skills") / stem / "SKILL.md",
}


def _generated_files(project: Path, tool: str) -> set[Path]:
    base = project / cli.SKILLS_TOOL_DIRS[tool]
    return {p.relative_to(project) for p in base.rglob("*") if p.is_file()}


def test_todas_as_ferramentas_estao_cobertas():
    assert set(SKILL_PATHS) == set(cli.SKILLS_TOOL_LABELS)


@pytest.mark.parametrize("tool", sorted(SKILL_PATHS))
def test_skills_add_gera_caminho_e_frontmatter(runner, project, tool):
    result = runner.invoke(cli.main, ["skills", "add", "--tool", tool])
    assert result.exit_code == 0, result.output

    expected = {SKILL_PATHS[tool](stem) for stem in SKILL_STEMS}
    assert _generated_files(project, tool) == expected

    for stem in SKILL_STEMS:
        fields, body = parse_frontmatter(project / SKILL_PATHS[tool](stem))
        assert body.strip()
        assert fields["description"]
        if tool == "cursor":
            assert fields["globs"] == ["**/*"]
            assert fields["alwaysApply"] is False
            assert body.lstrip().startswith("# Skill: ")
        else:
            assert fields["name"] == stem


@pytest.mark.parametrize("tool", ["cursor", "antigravity", "codex"])
def test_description_vem_do_template(runner, project, tool):
    runner.invoke(cli.main, ["skills", "add", "--tool", tool])

    fields, _ = parse_frontmatter(project / SKILL_PATHS[tool]("prd"))
    assert fields["description"].startswith("[01] Gera o PRD")


def test_skills_add_com_skill_gera_apenas_uma(runner, project):
    result = runner.invoke(cli.main, ["skills", "add", "--tool", "codex", "--skill", "prd"])

    assert result.exit_code == 0, result.output
    assert _generated_files(project, "codex") == {SKILL_PATHS["codex"]("prd")}


def test_skills_add_skill_inexistente(runner, project):
    result = runner.invoke(cli.main, ["skills", "add", "--tool", "codex", "--skill", "nao-existe"])

    assert "não encontrada" in result.output
    assert not (project / ".agents").exists()


def test_skills_add_sem_force_pula_e_com_force_sobrescreve(runner, project):
    runner.invoke(cli.main, ["skills", "add", "--tool", "claude"])
    target = project / SKILL_PATHS["claude"]("prd")
    original = target.read_text(encoding="utf-8")
    target.write_text("editado", encoding="utf-8")

    result = runner.invoke(cli.main, ["skills", "add", "--tool", "claude"])
    assert "não sobrescritas): 5" in result.output
    assert target.read_text(encoding="utf-8") == "editado"

    result = runner.invoke(cli.main, ["skills", "add", "--tool", "claude", "--force"])
    assert "Claude Code: 5 arquivo(s)" in result.output
    assert target.read_text(encoding="utf-8") == original


@pytest.mark.parametrize("tool", sorted(SKILL_PATHS))
def test_skills_remove_yes_apaga_diretorio(runner, project, tool):
    runner.invoke(cli.main, ["skills", "add", "--tool", tool])

    result = runner.invoke(cli.main, ["skills", "remove", "--tool", tool, "--yes"])

    assert result.exit_code == 0, result.output
    skills_dir = project / cli.SKILLS_TOOL_DIRS[tool]
    assert not skills_dir.exists()
    assert not skills_dir.parent.exists()


def test_skills_remove_skill_unica(runner, project):
    runner.invoke(cli.main, ["skills", "add", "--tool", "cursor"])

    result = runner.invoke(cli.main, ["skills", "remove", "--tool", "cursor", "--skill", "prd", "--yes"])

    assert result.exit_code == 0, result.output
    expected = {SKILL_PATHS["cursor"](s) for s in SKILL_STEMS - {"prd"}}
    assert _generated_files(project, "cursor") == expected


def test_skills_remove_sem_yes_cancela(runner, project):
    runner.invoke(cli.main, ["skills", "add", "--tool", "codex"])

    result = runner.invoke(cli.main, ["skills", "remove", "--tool", "codex"], input="n\n")

    assert "Operação cancelada" in result.output
    assert (project / ".agents" / "skills").exists()


def test_update_regenera_ferramentas_instaladas_sem_abrir_editor(runner, project, monkeypatch, no_editor):
    def fail():
        raise AssertionError("update não deve abrir o menu de ferramentas")

    monkeypatch.setattr(cli, "_select_tool", fail)
    runner.invoke(cli.main, ["skills", "add", "--tool", "claude"])
    runner.invoke(cli.main, ["skills", "add", "--tool", "cursor"])
    edited = project / SKILL_PATHS["claude"]("prd")
    edited.write_text("antigo", encoding="utf-8")

    result = runner.invoke(cli.main, ["update"])

    assert result.exit_code == 0, result.output
    assert edited.read_text(encoding="utf-8") != "antigo"
    assert "Cursor: 5 arquivo(s)" in result.output
    assert not (project / ".agents").exists()
    assert no_editor == []


def test_update_com_tool(runner, project, no_editor):
    result = runner.invoke(cli.main, ["update", "--tool", "codex"])

    assert result.exit_code == 0, result.output
    assert _generated_files(project, "codex") == {SKILL_PATHS["codex"](s) for s in SKILL_STEMS}


def test_update_sem_skills_instaladas(runner, project):
    result = runner.invoke(cli.main, ["update"])

    assert result.exit_code == 0
    assert "Nenhuma skill instalada" in result.output
