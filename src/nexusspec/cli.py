"""NexusSpec CLI — comandos principais."""

import click
import re
import subprocess
import questionary
from collections.abc import Callable
from questionary import Style
from importlib.resources import files
from pathlib import Path

from nexusspec.integrations.skills.services.skills_generator import SkillsGeneratorService

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

TEMPLATES = [
    "prd.md",
    "techespec.md",
    "tasks.md",
    "verify.md",
    "context-sync.md",
]

PROMPTS_DIR = "prompts"
NEXUS_DIR = ".nexus"
PRD_DIR = "prd"
ARCH_DIR = "architecture"
CHANGES_DIR = "changes"
ARCHIVE_DIR = "archive"

BANNER = """
 _   _                      _____                 
| \\ | | _____  ___   _ ___ / ____|                
|  \\| |/ _ \\ \\/ / | | / __| (___  _ __   ___  ___ 
| . ` |  __/>  <| |_| \\__ \\\\___ \\| '_ \\ / _ \\/ __|
|_|\\_|\\___/_/\\_\\\\__,_|___/____) | |_) |  __/ (__ 
                                |_____/| .__/ \\___|\\___|
                                       | |              
                                       |_|              
"""

MENU_STYLE = Style([
    ("selected",    "fg:#00ffcc bold"),
    ("pointer",     "fg:#00ffcc bold"),
    ("highlighted", "fg:#00ffcc bold"),
    ("question",    "bold"),
    ("answer",      "fg:#00ffcc bold"),
])

TOOLS: list[tuple[str, list[tuple[str, bool]]]] = [
    ("Antigravity",   [("antigravity", False)]),
    ("Cursor",        [("cursor", True)]),
    ("VSCode", [
        ("code", True),
        ("flatpak run com.visualstudio.code", True),
    ]),
    ("Sair", []),
]

# ---------------------------------------------------------------------------
# Helpers — estrutura de projeto
# ---------------------------------------------------------------------------

def _get_template(filename: str) -> str:
    return files("nexusspec.templates").joinpath(filename).read_text(encoding="utf-8")


def _copy_prompts(target_dir: Path, overwrite: bool = False) -> list[str]:
    prompts_path = target_dir / PROMPTS_DIR
    prompts_path.mkdir(parents=True, exist_ok=True)
    copied, skipped = [], []
    for name in TEMPLATES:
        dest = prompts_path / name
        if dest.exists() and not overwrite:
            skipped.append(name)
            continue
        dest.write_text(_get_template(name), encoding="utf-8")
        copied.append(name)
    if skipped:
        click.echo(click.style(f"  ⚠  Ignorados (já existem): {', '.join(skipped)}", fg="yellow"))
        click.echo(click.style("     Use --force para sobrescrever.", fg="yellow"))
    return copied


def _create_docs_structure(target_dir: Path):
    # Pastas principais
    for folder in [
        NEXUS_DIR,
        PRD_DIR,
        ARCH_DIR,
        CHANGES_DIR,
        ARCHIVE_DIR,
    ]:
        (target_dir / folder).mkdir(parents=True, exist_ok=True)

    # .gitkeep em pastas que começam vazias
    for folder in [CHANGES_DIR, ARCHIVE_DIR]:
        gitkeep = target_dir / folder / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

    # Arquivos de scaffolding com cabeçalho mínimo
    _scaffold_file(
        target_dir / NEXUS_DIR / "context.md",
        "# Contexto do projeto\n\n> Preencha: stack, restrições, decisões globais, ferramentas utilizadas.\n",
    )
    _scaffold_file(
        target_dir / PRD_DIR / "prd.md",
        "# PRD — Produto\n\n> Gerado pelo NexusSpec. Execute o prompt prd.md no seu agente de IA.\n",
    )
    _scaffold_file(
        target_dir / PRD_DIR / "personas.md",
        "# Personas\n\n> Perfis de usuário e stakeholders.\n",
    )
    _scaffold_file(
        target_dir / PRD_DIR / "metrics.md",
        "# Métricas de sucesso\n\n> Critérios mensuráveis de sucesso do produto.\n",
    )
    _scaffold_file(
        target_dir / ARCH_DIR / "architecture.md",
        "# Arquitetura\n\n> Decisões técnicas e ADRs.\n",
    )
    _scaffold_file(
        target_dir / ARCH_DIR / "epics.md",
        "# Épicos\n\n> Features agrupadas por área de produto.\n",
    )


def _scaffold_file(path: Path, content: str):
    """Cria um arquivo com conteúdo mínimo apenas se não existir."""
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def _create_readme(target_dir: Path, project_name: str):
    readme = target_dir / "README.md"
    if readme.exists():
        return
    content = f"""# {project_name}

> Projeto inicializado com [NexusSpec](https://github.com/LucasFerrDev/NexusSpec).

## Fluxo NexusSpec

1. **Contexto** — edite `.nexus/context.md` com a stack e restrições do projeto
2. **PRD** — execute `/prd.md` no seu agente de IA → gera `prd/`
3. **TechSpec** — execute `/techespec.md` por feature → atualiza `changes/[feature]/`
4. **Tasks** — execute `/tasks.md` → gera `changes/[feature]/tasks.md`
5. **Implementação** — execute cada task do `tasks.md` numa sessão separada
6. **Verificação** — execute `/verify.md` → gera `changes/[feature]/verify.md`
7. **Arquivo** — execute `nexusspec task archive [feature]` → move para `archive/`

## Comandos úteis

```bash
nexusspec task new --name nome-da-feature   # cria nova feature em changes/
nexusspec task status                        # exibe progresso de todas as features
nexusspec task archive nome-da-feature       # arquiva feature concluída
nexusspec open                               # abre o projeto no editor escolhido
```

## Estrutura

```
{project_name}/
├── .nexus/context.md          ← regras e stack do projeto
├── prd/                       ← PRD, personas, métricas
├── architecture/              ← decisões técnicas, épicos
├── changes/                   ← features em andamento
├── archive/                   ← features concluídas
└── prompts/                   ← prompts para o agente de IA
```
"""
    readme.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Helpers — launcher de ferramentas
# ---------------------------------------------------------------------------

def _try_open(commands: list[tuple[str, bool]], project_path: str) -> bool:
    for cmd_str, requires_path in commands:
        parts = cmd_str.split()
        if requires_path:
            parts.append(project_path)
        try:
            result = subprocess.run(
                parts,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
            if result.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return False


def _generate_skills_for_tool(project_dir: Path, tool_choice: str, overwrite: bool = False):
    service = SkillsGeneratorService()
    report = service.generate_for_tool(project_dir=project_dir, tool_choice=tool_choice, overwrite=overwrite)
    if report is None:
        return

    if report.created_files:
        click.echo(click.style(
            f"  ✔  Skills geradas para {report.provider_name}: {len(report.created_files)} arquivo(s)",
            fg="green",
        ))
    if report.skipped_files:
        click.echo(click.style(
            f"  ⚠  Skills já existentes (não sobrescritas): {len(report.skipped_files)}",
            fg="yellow",
        ))


def _tool_menu(
    project_path: str,
    on_tool_selected: Callable[[str, Path], None] | None = None,
):
    """Exibe o menu interativo de ferramentas e abre o projeto na escolhida."""
    click.echo()

    tool_labels = [label for label, _ in TOOLS]

    choice = questionary.select(
        "Escolha por onde você gostaria de trabalhar:",
        choices=tool_labels,
        style=MENU_STYLE,
    ).ask()

    if choice is None or choice == "Sair":
        click.echo(click.style("\n  Até logo!\n", fg="bright_black"))
        return

    project_dir = Path(project_path)
    if on_tool_selected is not None:
        on_tool_selected(choice, project_dir)

    commands = next(cmds for label, cmds in TOOLS if label == choice)

    click.echo()
    click.echo(click.style(f"  Abrindo {choice}...", fg="cyan"))
    success = _try_open(commands, project_path)

    if success:
        click.echo(click.style(f"  ✔  {choice} aberto com sucesso!\n", fg="green"))
    else:
        click.echo()
        click.echo(click.style("  ✗  Não foi possível abrir a ferramenta selecionada.", fg="red"))
        click.echo(click.style("     Verifique se ela está instalada.\n", fg="red"))


# ---------------------------------------------------------------------------
# Fluxo de init compartilhado
# ---------------------------------------------------------------------------

def _run_init(project_name: str, force: bool) -> Path:
    click.echo(click.style(BANNER, fg="cyan"))

    if project_name == ".":
        target_dir = Path.cwd()
        display_name = target_dir.name
    else:
        target_dir = Path.cwd() / project_name
        display_name = project_name
        if target_dir.exists() and any(target_dir.iterdir()):
            if not force:
                click.echo(click.style(f"  ✗  A pasta '{project_name}' já existe e não está vazia.", fg="red"))
                click.echo(click.style("     Use --force para inicializar mesmo assim.", fg="red"))
                raise SystemExit(1)
        target_dir.mkdir(parents=True, exist_ok=True)

    click.echo(click.style(f"  Inicializando NexusSpec em: {target_dir}\n", fg="white"))

    _create_docs_structure(target_dir)
    click.echo(click.style("  ✔  Estrutura de pastas criada", fg="green"))

    copied = _copy_prompts(target_dir, overwrite=force)
    if copied:
        click.echo(click.style(f"  ✔  Prompts copiados: {', '.join(copied)}", fg="green"))

    _create_readme(target_dir, display_name)
    click.echo(click.style("  ✔  README.md criado", fg="green"))

    click.echo()
    click.echo(click.style("  ─────────────────────────────────────────", fg="bright_black"))
    click.echo(click.style(f"  ✅  Projeto '{display_name}' pronto!", fg="bright_green", bold=True))

    return target_dir


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group(invoke_without_command=True)
@click.version_option(package_name="nexusspec")
@click.pass_context
def main(ctx: click.Context):
    """NexusSpec — CLI para workflows de Spec-Driven Development."""
    if ctx.invoked_subcommand is None:
        click.echo(click.style(BANNER, fg="cyan"))
        click.echo("  Nenhum subcomando informado.")
        click.echo("  Use  nexusspec init <projeto>  para iniciar um projeto.")
        click.echo("  Use  nexusspec --help  para ver todos os comandos.\n")


# ---------------------------------------------------------------------------
# nexusspec init
# ---------------------------------------------------------------------------

@main.command("init")
@click.argument("project_name")
@click.option("--force", is_flag=True, default=False, help="Sobrescreve arquivos de prompt existentes.")
def init(project_name: str, force: bool):
    """
    Inicializa um novo projeto NexusSpec e oferece abrir no editor.

    \b
    Exemplos:
      nexusspec init meu-projeto
      nexusspec init .
      nexusspec init meu-projeto --force
    """
    target_dir = _run_init(project_name, force)
    _tool_menu(
        str(target_dir),
        on_tool_selected=lambda choice, project_dir: _generate_skills_for_tool(
            project_dir=project_dir,
            tool_choice=choice,
            overwrite=force,
        ),
    )


# ---------------------------------------------------------------------------
# nexusspec add
# ---------------------------------------------------------------------------

@main.command("add")
@click.option("--force", is_flag=True, default=False, help="Sobrescreve prompts existentes.")
def add(force: bool):
    """
    Adiciona os prompts NexusSpec em um projeto já existente.

    \b
    Exemplos:
      nexusspec add
      nexusspec add --force
    """
    target_dir = Path.cwd()
    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style(f"  Adicionando prompts NexusSpec em: {target_dir}\n", fg="white"))

    _create_docs_structure(target_dir)
    click.echo(click.style("  ✔  Estrutura NexusSpec verificada", fg="green"))

    copied = _copy_prompts(target_dir, overwrite=force)
    if copied:
        click.echo(click.style(f"  ✔  Prompts adicionados: {', '.join(copied)}", fg="green"))

    click.echo()
    click.echo(click.style("  ─────────────────────────────────────────", fg="bright_black"))
    click.echo(click.style("  ✅  NexusSpec adicionado ao projeto!", fg="bright_green", bold=True))

    _tool_menu(
        str(target_dir),
        on_tool_selected=lambda choice, project_dir: _generate_skills_for_tool(
            project_dir=project_dir,
            tool_choice=choice,
            overwrite=force,
        ),
    )


# ---------------------------------------------------------------------------
# nexusspec open
# ---------------------------------------------------------------------------

@main.command("open")
@click.argument("path", default=".", required=False)
def open_project(path: str):
    """
    Abre um projeto existente no editor escolhido.

    \b
    Exemplos:
      nexusspec open
      nexusspec open meu-projeto
    """
    target = Path(path).resolve()
    if not target.exists():
        click.echo(click.style(f"  ✗  Caminho não encontrado: {target}", fg="red"))
        raise SystemExit(1)
    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style(f"  Projeto: {target}\n", fg="white"))
    _tool_menu(str(target))


# ---------------------------------------------------------------------------
# nexusspec task
# ---------------------------------------------------------------------------

@main.group("task")
def task():
    """Gerencia tarefas do projeto NexusSpec."""
    pass


@task.command("new")
@click.option("--name", "-n", default=None, help="Nome da feature (use hífens, ex: autenticacao-usuario).")
def task_new(name: str | None):
    """
    Cria a estrutura de uma nova tarefa interativamente.

    \b
    Exemplos:
      nexusspec task new
      nexusspec task new --name autenticacao-usuario
    """
    target_dir = Path.cwd()

    # Verifica se é um projeto NexusSpec
    if not (target_dir / PROMPTS_DIR).exists():
        click.echo(click.style("  ✗  Nenhum projeto NexusSpec encontrado neste diretório.", fg="red"))
        click.echo(click.style("     Execute nexusspec init <projeto> primeiro.", fg="red"))
        raise SystemExit(1)

    if not name:
        name = questionary.text(
            "  Nome da feature (use hífens, ex: autenticacao-usuario):",
            style=MENU_STYLE,
        ).ask()

        if not name:
            click.echo(click.style("\n  Operação cancelada.\n", fg="bright_black"))
            return

    # Normaliza: lowercase, espaços → hífens
    name_slug = name.strip().lower().replace(" ", "-")
    feature_dir = target_dir / CHANGES_DIR / name_slug
    feature_dir.mkdir(parents=True, exist_ok=True)

    # Cria os arquivos vazios com cabeçalho mínimo
    files_created = []
    for filename, content in [
        ("spec.md", f"# Spec — {name_slug}\n\n> Comportamento esperado (Given/When/Then).\n"),
        ("design.md", f"# Design — {name_slug}\n\n> Abordagem técnica e decisões de implementação.\n"),
        ("tasks.md", f"# Tasks — {name_slug}\n\n> Liste as tasks atômicas. Cada task deve ser executável numa única sessão de IA.\n"),
        ("verify.md", f"# Verify — {name_slug}\n\n> Checklist pós-implementação para confirmar que a spec foi atendida.\n"),
    ]:
        filepath = feature_dir / filename
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
            files_created.append(filename)

    click.echo()
    click.echo(click.style(f"  ✔  Feature criada: {name_slug}", fg="green"))
    for f in files_created:
        click.echo(click.style(f"     → changes/{name_slug}/{f}", fg="bright_black"))

    click.echo()
    click.echo(click.style("  Próximo passo no seu agente de IA:", fg="white"))
    click.echo(click.style("    /techespec.md", fg="cyan"))
    click.echo()


@task.command("status")
def task_status():
    """
    Exibe o status de todas as tarefas do projeto.

    \b
    Exemplos:
      nexusspec task status
    """
    target_dir = Path.cwd()
    changes_dir = target_dir / CHANGES_DIR

    if not changes_dir.exists():
        click.echo(click.style("  ✗  Nenhuma pasta changes/ encontrada.", fg="red"))
        raise SystemExit(1)

    features = sorted([
        d for d in changes_dir.iterdir() if d.is_dir() and d.name != ".gitkeep"
    ], key=lambda d: d.name)

    if not features:
        click.echo(click.style("\n  Nenhuma feature encontrada.\n", fg="yellow"))
        click.echo(click.style("  Use  nexusspec task new --name nome-da-feature  para criar uma.\n", fg="bright_black"))
        return

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style("  Status das features\n", bold=True))
    click.echo(f"  {'Feature':<30} {'spec':^6} {'design':^7} {'tasks':^6} {'verify':^7}")
    click.echo(f"  {'─'*30} {'─'*6} {'─'*7} {'─'*6} {'─'*7}")

    for feature_dir in features:
        has_spec = (feature_dir / "spec.md").exists()
        has_design = (feature_dir / "design.md").exists()
        has_tasks = (feature_dir / "tasks.md").exists()
        has_verify = (feature_dir / "verify.md").exists()

        all_done = all([has_spec, has_design, has_tasks, has_verify])
        any_done = any([has_spec, has_design, has_tasks, has_verify])

        icon = click.style("✅", fg="green") if all_done else (
            click.style("🔄", fg="yellow") if any_done else click.style("⬜", fg="bright_black")
        )
        mark = lambda v: click.style("✔", fg="green") if v else click.style("✗", fg="red")

        click.echo(
            f"  {icon} {feature_dir.name:<28} {mark(has_spec):^6} {mark(has_design):^7} "
            f"{mark(has_tasks):^6} {mark(has_verify):^7}"
        )

    click.echo()


@task.command("archive")
@click.argument("feature_name")
def task_archive(feature_name: str):
    """
    Move uma feature concluída de changes/ para archive/.

    \b
    Exemplos:
      nexusspec task archive autenticacao-usuario
    """
    target_dir = Path.cwd()
    source = target_dir / CHANGES_DIR / feature_name
    dest = target_dir / ARCHIVE_DIR / feature_name

    if not source.exists():
        click.echo(click.style(f"  ✗  Feature '{feature_name}' não encontrada em changes/.", fg="red"))
        raise SystemExit(1)

    if dest.exists():
        click.echo(click.style(f"  ✗  Já existe '{feature_name}' em archive/.", fg="yellow"))
        raise SystemExit(1)

    import shutil
    shutil.move(str(source), str(dest))
    click.echo(click.style(f"\n  ✅  '{feature_name}' arquivada com sucesso!\n", fg="green"))
    click.echo(click.style(f"     → archive/{feature_name}/\n", fg="bright_black"))


@task.command("done")
@click.argument("task_id")
def task_done(task_id: str):
    """
    Marca uma tarefa como concluída no implementation_plan.md.

    \b
    Exemplos:
      nexusspec task done 001
      nexusspec task done tarefa-001
    """
    target_dir = Path.cwd()
    plan_file = target_dir / "implementation_plan.md"

    # Normaliza o ID
    tid = task_id.replace("tarefa-", "").zfill(3)

    if not plan_file.exists():
        click.echo(click.style("  ✗  implementation_plan.md não encontrado na raiz do projeto.", fg="red"))
        click.echo(click.style("     Execute /plan.md no seu agente de IA para gerá-lo.", fg="bright_black"))
        raise SystemExit(1)

    content = plan_file.read_text(encoding="utf-8")

    if f"tarefa-{tid}" not in content:
        click.echo(click.style(f"  ✗  Tarefa tarefa-{tid} não encontrada no plano.", fg="red"))
        raise SystemExit(1)

    # Substitui o status na linha da tarefa
    updated = re.sub(
        rf"(\| tarefa-{tid} \|[^|]+\|)\s*[⬜🔄✅][^\|]*(\|)",
        rf"\1 ✅ concluída \2",
        content,
    )

    if updated == content:
        click.echo(click.style(f"  ⚠  Tarefa tarefa-{tid} já está marcada como concluída ou o formato da tabela é diferente.", fg="yellow"))
        return

    plan_file.write_text(updated, encoding="utf-8")
    click.echo(click.style(f"\n  ✅  Tarefa tarefa-{tid} marcada como concluída!\n", fg="green"))


# ---------------------------------------------------------------------------
# nexusspec update
# ---------------------------------------------------------------------------

@main.command("update")
@click.option("--force", is_flag=True, default=False, help="Sobrescreve todos os prompts com a versão mais recente.")
def update(force: bool):
    """
    Atualiza os prompts do projeto para a versão mais recente do NexusSpec.

    \b
    Exemplos:
      nexusspec update
      nexusspec update --force
    """
    target_dir = Path.cwd()

    if not (target_dir / PROMPTS_DIR).exists():
        click.echo(click.style("  ✗  Nenhum projeto NexusSpec encontrado neste diretório.", fg="red"))
        raise SystemExit(1)

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style("  Atualizando prompts...\n", fg="white"))

    copied = _copy_prompts(target_dir, overwrite=force)

    if copied:
        click.echo(click.style(f"  ✔  Prompts atualizados: {', '.join(copied)}", fg="green"))
    else:
        click.echo(click.style("  ℹ  Todos os prompts já estão na versão atual.", fg="cyan"))
        click.echo(click.style("     Use --force para sobrescrever mesmo assim.", fg="bright_black"))

    click.echo()


# ---------------------------------------------------------------------------
# nexusspec list
# ---------------------------------------------------------------------------

@main.command("list")
def list_templates():
    """Lista os prompts disponíveis no NexusSpec."""
    click.echo(click.style("\n  Prompts disponíveis no NexusSpec:\n", fg="cyan", bold=True))
    descriptions = {
        "prd.md":          "Gera o PRD principal do produto",
        "techespec.md":    "Gera a TechSpec de uma feature",
        "tasks.md":        "Quebra feature em tasks atômicas",
        "verify.md":       "Verifica implementação contra a spec",
        "context-sync.md": "Sincroniza contexto para diferentes ferramentas",
    }
    click.echo(click.style("  Use / para mencionar no seu agente de IA:\n", fg="bright_black"))
    for name, desc in descriptions.items():
        click.echo(f"  {click.style('/' + name, fg='yellow', bold=True)}")
        click.echo(f"    {desc}\n")
