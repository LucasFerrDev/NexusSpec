"""NexusSpec CLI — comandos principais."""

import click
import os
import re
import subprocess
import readline
import glob
import questionary
from questionary import Style
from importlib.resources import files
from pathlib import Path

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

TEMPLATES = [
    "pdr_geral.md",
    "prd_tarefa.md",
    "techspec_tarefa.md",
    "plan.md",
]

PROMPTS_DIR = "prompts"
DOCS_DIR = "docs"
DOCS_SUBDIRS = ["tarefas"]

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
    ("Claude Code",   [("claude", True)]),
    ("Codex",         [("codex", False)]),
    ("Copilot CLI",   [("copilot", False)]),
    ("Cursor",        [("cursor", True)]),
    ("Gemini CLI",    [("gemini", False)]),
    ("IntelliJ IDEA", [
        ("idea", True),
        ("flatpak run com.jetbrains.IntelliJ-IDEA-Ultimate", True),
        ("flatpak run com.jetbrains.IntelliJ-IDEA-Community", True),
    ]),
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
    for subdir in DOCS_SUBDIRS:
        (target_dir / DOCS_DIR / subdir).mkdir(parents=True, exist_ok=True)
    gitkeep = target_dir / DOCS_DIR / "tarefas" / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()


def _create_readme(target_dir: Path, project_name: str):
    readme = target_dir / "README.md"
    if readme.exists():
        return
    content = f"""# {project_name}

> Projeto inicializado com [NexusSpec](https://github.com/LucasFerrDev/NexusSpec).

## Fluxo NexusSpec

1. **PRD Geral** — `/pdr_geral.md`
2. **PRD da tarefa** — `/prd_tarefa.md`
3. **TechSpec da tarefa** — `/techspec_tarefa.md`
4. **Plano automático** — `/plan.md`
5. **Implementação** — implemente o plano salvando os arquivos na raiz do projeto

## Estrutura

```
{project_name}/
├── docs/
│   └── tarefas/        ← pastas tarefa-001, tarefa-002...
├── prompts/            ← prompts do NexusSpec
│   ├── pdr_geral.md
│   ├── prd_tarefa.md
│   ├── techspec_tarefa.md
│   └── plan.md
└── README.md
```
"""
    readme.write_text(content, encoding="utf-8")


def _next_task_id(target_dir: Path) -> str:
    """Determina o próximo ID de tarefa com base nas pastas existentes."""
    tarefas_dir = target_dir / DOCS_DIR / "tarefas"
    existing = [
        d.name for d in tarefas_dir.iterdir()
        if d.is_dir() and re.match(r"tarefa-\d+", d.name)
    ] if tarefas_dir.exists() else []

    if not existing:
        return "001"

    nums = [int(re.search(r"\d+", name).group()) for name in existing]
    return str(max(nums) + 1).zfill(3)


def _update_implementation_plan(target_dir: Path, task_id: str, task_name: str):
    """Adiciona a nova tarefa na tabela do implementation_plan.md se ele existir."""
    plan_file = target_dir / "implementation_plan.md"
    if not plan_file.exists():
        return

    content = plan_file.read_text(encoding="utf-8")
    new_row = (
        f"| tarefa-{task_id} | {task_name} | ⬜ pendente | "
        f"[PLANO_TAREFA_{task_id}.md]"
        f"(docs/tarefas/tarefa-{task_id}/PLANO_TAREFA_{task_id}.md) |"
    )

    # Insere após o cabeçalho da tabela de status
    if "| Tarefa | Nome |" in content:
        lines = content.splitlines()
        insert_after = next(
            (i for i, l in enumerate(lines) if "| Tarefa | Nome |" in l), None
        )
        if insert_after is not None:
            # pula a linha de separação da tabela
            insert_at = insert_after + 2
            lines.insert(insert_at, new_row)
            plan_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


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


def _tool_menu(project_path: str):
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
    click.echo(click.style("  ✔  Estrutura de pastas criada (docs/tarefas/)", fg="green"))

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
    _tool_menu(str(target_dir))


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
    click.echo(click.style("  ✔  Estrutura docs/tarefas/ verificada", fg="green"))

    copied = _copy_prompts(target_dir, overwrite=force)
    if copied:
        click.echo(click.style(f"  ✔  Prompts adicionados: {', '.join(copied)}", fg="green"))

    click.echo()
    click.echo(click.style("  ─────────────────────────────────────────", fg="bright_black"))
    click.echo(click.style("  ✅  NexusSpec adicionado ao projeto!", fg="bright_green", bold=True))

    _tool_menu(str(target_dir))


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
@click.option("--name", "-n", default=None, help="Nome da tarefa (sem espaços, use hífens).")
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

    task_id = _next_task_id(target_dir)

    if not name:
        name = questionary.text(
            f"  Nome da tarefa [{task_id}]:",
            style=MENU_STYLE,
        ).ask()

        if not name:
            click.echo(click.style("\n  Operação cancelada.\n", fg="bright_black"))
            return

    # Normaliza: lowercase, espaços → hífens
    name_slug = name.strip().lower().replace(" ", "-")
    task_dir = target_dir / DOCS_DIR / "tarefas" / f"tarefa-{task_id}"
    task_dir.mkdir(parents=True, exist_ok=True)

    # Cria os arquivos vazios com cabeçalho mínimo
    files_created = []
    for doc_type, suffix in [
        ("PRD",      f"PRD_TAREFA_{task_id}.md"),
        ("TECHSPEC", f"TECHSPEC_TAREFA_{task_id}.md"),
        ("PLANO",    f"PLANO_TAREFA_{task_id}.md"),
    ]:
        filepath = task_dir / suffix
        if not filepath.exists():
            filepath.write_text(
                f"# {doc_type} — Tarefa {task_id}: {name_slug}\n\n> Gerado pelo NexusSpec.\n",
                encoding="utf-8",
            )
            files_created.append(suffix)

    # Atualiza o implementation_plan.md se existir
    _update_implementation_plan(target_dir, task_id, name_slug)

    click.echo()
    click.echo(click.style(f"  ✔  Tarefa tarefa-{task_id} criada: {name_slug}", fg="green"))
    for f in files_created:
        click.echo(click.style(f"     → docs/tarefas/tarefa-{task_id}/{f}", fg="bright_black"))

    click.echo()
    click.echo(click.style("  Próximo passo no seu agente de IA:", fg="white"))
    click.echo(click.style(f"    /prd_tarefa.md", fg="cyan"))
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
    tarefas_dir = target_dir / DOCS_DIR / "tarefas"

    if not tarefas_dir.exists():
        click.echo(click.style("  ✗  Nenhuma pasta docs/tarefas/ encontrada.", fg="red"))
        raise SystemExit(1)

    tasks = sorted([
        d for d in tarefas_dir.iterdir()
        if d.is_dir() and re.match(r"tarefa-\d+", d.name)
    ], key=lambda d: d.name)

    if not tasks:
        click.echo(click.style("\n  Nenhuma tarefa encontrada.\n", fg="yellow"))
        click.echo(click.style("  Use  nexusspec task new  para criar uma.\n", fg="bright_black"))
        return

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style("  Status das tarefas\n", bold=True))
    click.echo(f"  {'ID':<14} {'Nome':<35} {'PRD':^5} {'TECH':^5} {'PLANO':^6}")
    click.echo(f"  {'─'*14} {'─'*35} {'─'*5} {'─'*5} {'─'*6}")

    for task_dir in tasks:
        tid = re.search(r"\d+", task_dir.name).group()
        has_prd    = (task_dir / f"PRD_TAREFA_{tid}.md").exists()
        has_tech   = (task_dir / f"TECHSPEC_TAREFA_{tid}.md").exists()
        has_plan   = (task_dir / f"PLANO_TAREFA_{tid}.md").exists()

        # Tenta extrair o nome do cabeçalho do PRD
        task_name = "—"
        prd_file = task_dir / f"PRD_TAREFA_{tid}.md"
        if prd_file.exists():
            first_line = prd_file.read_text(encoding="utf-8").splitlines()[0]
            match = re.search(r"Tarefa \d+:\s*(.+)", first_line)
            if match:
                task_name = match.group(1).strip()[:34]

        # Status geral
        if has_prd and has_tech and has_plan:
            status_icon = click.style("✅", fg="green")
        elif has_prd or has_tech:
            status_icon = click.style("🔄", fg="yellow")
        else:
            status_icon = click.style("⬜", fg="bright_black")

        prd_mark   = click.style("✔", fg="green") if has_prd  else click.style("✗", fg="red")
        tech_mark  = click.style("✔", fg="green") if has_tech else click.style("✗", fg="red")
        plan_mark  = click.style("✔", fg="green") if has_plan else click.style("✗", fg="red")

        click.echo(
            f"  {status_icon} {task_dir.name:<12} {task_name:<35} {prd_mark:^5} {tech_mark:^5} {plan_mark:^6}"
        )

    click.echo()
    click.echo(click.style("  ⬜ pendente  🔄 em andamento  ✅ completa\n", fg="bright_black"))


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
        "pdr_geral.md":       "Gera o PRD Geral do produto (docs/PRD_GERAL.md)",
        "prd_tarefa.md":      "Gera o PRD de uma tarefa específica",
        "techspec_tarefa.md": "Gera a TechSpec técnica de uma tarefa",
        "plan.md":            "Identifica tarefas sem plano e gera automaticamente",
    }
    click.echo(click.style("  Use / para mencionar no seu agente de IA:\n", fg="bright_black"))
    for name, desc in descriptions.items():
        click.echo(f"  {click.style('/' + name, fg='yellow', bold=True)}")
        click.echo(f"    {desc}\n")
