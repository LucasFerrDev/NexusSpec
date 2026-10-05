from pathlib import Path

import pytest

from nexusspec import cli

TASK_MD = """# Tasks — auth

## Pendente

- [ ] criar model de usuário
- [ ] criar endpoint de login
- [ ] criar endpoint de logout

## Concluído

(vazio no início — a skill apply moverá os itens para cá conforme implementar)
"""


@pytest.fixture
def feature(project: Path) -> Path:
    feature_dir = project / cli.SPECS_DIR / "auth"
    feature_dir.mkdir()
    (feature_dir / "task.md").write_text(TASK_MD, encoding="utf-8")
    return feature_dir


def test_task_new_cria_arquivos(runner, project):
    result = runner.invoke(cli.main, ["task", "new", "--name", "Autenticacao Usuario"])

    assert result.exit_code == 0, result.output
    feature_dir = project / cli.SPECS_DIR / "autenticacao-usuario"
    for filename in ["spec.md", "design.md", "task.md", "verify.md"]:
        assert (feature_dir / filename).exists()
    assert "specify" in (feature_dir / "spec.md").read_text(encoding="utf-8")
    assert "specify" in result.output


def test_task_new_fora_de_projeto(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(cli.main, ["task", "new", "--name", "x"])

    assert result.exit_code == 1
    assert "Nenhum projeto NexusSpec" in result.output


def test_task_status(runner, project, feature):
    runner.invoke(cli.main, ["task", "new", "--name", "vazia"])

    result = runner.invoke(cli.main, ["task", "status"])

    assert result.exit_code == 0, result.output
    lines = {line.split()[0]: line for line in result.output.splitlines() if line.strip().startswith(("auth", "vazia"))}
    assert "0/3 tasks" in lines["auth"]
    assert "sem tasks" in lines["vazia"]


def test_task_archive_sem_pendencias(runner, project, feature):
    (feature / "task.md").write_text("## Concluído\n\n- [x] feito\n", encoding="utf-8")

    result = runner.invoke(cli.main, ["task", "archive", "auth"])

    assert result.exit_code == 0, result.output
    assert not feature.exists()
    assert (project / cli.ARCHIVE_DIR / "auth" / "task.md").exists()


def test_task_archive_com_pendencias_pede_confirmacao(runner, project, feature):
    result = runner.invoke(cli.main, ["task", "archive", "auth"], input="n\n")

    assert "3 task(s) ainda pendente(s)" in result.output
    assert "Operação cancelada" in result.output
    assert feature.exists()

    result = runner.invoke(cli.main, ["task", "archive", "auth"], input="y\n")
    assert not feature.exists()


def test_task_archive_yes_pula_confirmacao(runner, project, feature):
    result = runner.invoke(cli.main, ["task", "archive", "auth", "--yes"])

    assert result.exit_code == 0, result.output
    assert "Arquivar mesmo assim?" not in result.output
    assert (project / cli.ARCHIVE_DIR / "auth").exists()


def test_task_archive_feature_inexistente(runner, project):
    result = runner.invoke(cli.main, ["task", "archive", "nao-existe"])
    assert result.exit_code == 1


def test_task_done_por_indice(runner, project, feature):
    result = runner.invoke(cli.main, ["task", "done", "auth", "2"])

    assert result.exit_code == 0, result.output
    content = (feature / "task.md").read_text(encoding="utf-8")
    pendente, concluido = content.split("## Concluído")
    assert "criar endpoint de login" not in pendente
    assert "- [x] criar endpoint de login" in concluido
    assert "(vazio no início" not in content
    assert "1/3 tasks" in result.output


def test_task_done_por_texto(runner, project, feature):
    result = runner.invoke(cli.main, ["task", "done", "auth", "LOGOUT"])

    assert result.exit_code == 0, result.output
    concluido = (feature / "task.md").read_text(encoding="utf-8").split("## Concluído")[1]
    assert "- [x] criar endpoint de logout" in concluido


def test_task_done_texto_ambiguo(runner, project, feature):
    result = runner.invoke(cli.main, ["task", "done", "auth", "endpoint"])

    assert result.exit_code == 1
    assert "mais de uma task" in result.output
    assert (feature / "task.md").read_text(encoding="utf-8") == TASK_MD


@pytest.mark.parametrize("selector", ["0", "4", "inexistente"])
def test_task_done_seletor_invalido(runner, project, feature, selector):
    result = runner.invoke(cli.main, ["task", "done", "auth", selector])

    assert result.exit_code == 1
    assert (feature / "task.md").read_text(encoding="utf-8") == TASK_MD


def test_task_done_cria_secao_concluido(runner, project, feature):
    (feature / "task.md").write_text("# Tasks\n\n- [ ] única\n", encoding="utf-8")

    runner.invoke(cli.main, ["task", "done", "auth", "1"])

    assert (feature / "task.md").read_text(encoding="utf-8") == "# Tasks\n\n## Concluído\n\n- [x] única\n"


def test_task_done_sem_task_md(runner, project):
    result = runner.invoke(cli.main, ["task", "done", "nao-existe", "1"])
    assert result.exit_code == 1
