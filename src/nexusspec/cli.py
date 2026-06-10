"""NexusSpec CLI — comandos principais."""

import click
import re
import shutil
import subprocess
import questionary
from collections.abc import Callable
from questionary import Style
from importlib.resources import files
from pathlib import Path

from nexusspec.integrations.skills.services.skills_generator import SkillsGeneratorService
from nexusspec.integrations.skills.providers.shared.prompt_loader import load_prompt_templates

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

DOCS_DIR = "docs"
PRD_DIR = "docs/prd"
ARCH_DIR = "docs/architecture"
FEATURES_DIR = "features"
SPECS_DIR = "features/specs"
ARCHIVE_DIR = "features/done"

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
    ("Cursor",        [("cursor", True)]),
    ("VSCode", [
        ("code", True),
        ("flatpak run com.visualstudio.code", True),
    ]),
    ("Sair", []),
]

SKILLS_TOOL_LABELS: dict[str, str] = {
    "vscode": "VSCode",
    "claude": "Claude Code",
    "cursor": "Cursor",
    "antigravity": "Antigravity",
}

SKILLS_TOOL_DIRS: dict[str, Path] = {
    "vscode": Path(".github") / "skills",
    "claude": Path(".claude") / "commands",
    "cursor": Path(".cursor") / "rules",
    "antigravity": Path(".agent") / "skills",
}

# ---------------------------------------------------------------------------
# Helpers — estrutura de projeto
# ---------------------------------------------------------------------------

def _normalize_skill_name(skill: str) -> str:
    name = Path(skill).name
    if name.endswith(".mdc"):
        return name[:-4]
    if name.endswith(".md"):
        return name[:-3]
    return name


def _filter_prompts_by_skill(prompts, skill: str):
    target_stem = _normalize_skill_name(skill)
    target_name = f"{target_stem}.md"
    return [
        prompt
        for prompt in prompts
        if prompt.stem == target_stem or prompt.name == skill or prompt.name == target_name
    ]


def _skill_target_path(project_dir: Path, tool_key: str, skill: str) -> Path:
    skill_name = _normalize_skill_name(skill)
    base_dir = project_dir / SKILLS_TOOL_DIRS[tool_key]
    if tool_key in {"vscode", "antigravity"}:
        return base_dir / skill_name
    if tool_key == "cursor":
        return base_dir / f"{skill_name}.mdc"
    return base_dir / f"{skill_name}.md"


def _cleanup_empty_skill_dirs(project_dir: Path, tool_key: str):
    skills_dir = project_dir / SKILLS_TOOL_DIRS[tool_key]
    if skills_dir.exists() and skills_dir.is_dir() and not any(skills_dir.iterdir()):
        skills_dir.rmdir()

    parent_dir = skills_dir.parent
    if parent_dir.exists() and parent_dir.is_dir() and not any(parent_dir.iterdir()):
        parent_dir.rmdir()


def _get_template(filename: str) -> str:
    return files("nexusspec.templates").joinpath(filename).read_text(encoding="utf-8")


def _is_nexusspec_project(target_dir: Path) -> bool:
    return (
        (target_dir / PRD_DIR).exists()
        and (target_dir / ARCH_DIR).exists()
        and (target_dir / SPECS_DIR).exists()
        and (target_dir / ARCHIVE_DIR).exists()
    )


def _create_docs_structure(target_dir: Path):
    for folder in [
        DOCS_DIR,
        PRD_DIR,
        ARCH_DIR,
        FEATURES_DIR,
        SPECS_DIR,
        ARCHIVE_DIR,
    ]:
        (target_dir / folder).mkdir(parents=True, exist_ok=True)

    # .gitkeep em pastas que começam vazias
    for folder in [SPECS_DIR, ARCHIVE_DIR]:
        gitkeep = target_dir / folder / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

    # Arquivos de scaffolding
    _scaffold_file(
        target_dir / PRD_DIR / "prd.md",
        "# PRD — Produto\n\n> Gerado pelo NexusSpec. Execute a skill prd na sua ferramenta de IA.\n",
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

## Fluxo de trabalho

As skills do NexusSpec foram instaladas na sua ferramenta de IA durante o `init`.
Use-as diretamente pelo seu agente na seguinte ordem:

1. **prd** — defina o produto, personas e métricas
2. **techspec** — defina stack, tecnologias e design da feature
3. **task** — gere o checklist de implementação da feature
4. **apply** — implemente todas as tasks pendentes automaticamente
5. **verify** — valide a implementação e arquive quando aprovado

## Comandos úteis

```bash
nspec task new --name nome-da-feature        # cria nova feature em features/specs/
nspec task status                            # exibe progresso de todas as features
nspec task archive nome-da-feature           # arquiva feature concluída em features/done/
nspec open                                   # abre o projeto no editor escolhido
nspec skills add --tool vscode               # gera skills para a ferramenta escolhida
nspec skills remove --tool vscode            # remove as skills da ferramenta escolhida
```

## Estrutura

```
{project_name}/
├── docs/
│   ├── prd/                   ← PRD, personas, métricas
│   └── architecture/          ← decisões técnicas, épicos
├── features/
│   ├── specs/                 ← specs das features em desenvolvimento
│   └── done/                  ← features concluídas e arquivadas
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


def _generate_skills_for_tool(
    project_dir: Path,
    tool_choice: str,
    overwrite: bool = False,
    skill: str | None = None,
):
    prompts = load_prompt_templates(project_dir=project_dir)
    if not prompts:
        click.echo(click.style("  ⚠  Nenhum template de skill encontrado.", fg="yellow"))
        return

    if skill:
        prompts = _filter_prompts_by_skill(prompts, skill)
        if not prompts:
            click.echo(click.style(f"  ✗  Skill '{skill}' não encontrada nos templates disponíveis.", fg="red"))
            return

    service = SkillsGeneratorService()
    report = service.generate_for_tool(
        project_dir=project_dir,
        tool_choice=tool_choice,
        overwrite=overwrite,
        prompts=prompts,
    )
    if report is None:
        click.echo(click.style("  ✗  Ferramenta de skills não suportada.", fg="red"))
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

def _run_init(project_name: str, force: bool, target: Path | None = None) -> Path:
    click.echo(click.style(BANNER, fg="cyan"))

    base_dir = target if target is not None else Path.cwd()

    if project_name == ".":
        target_dir = base_dir
        display_name = target_dir.name
    else:
        target_dir = base_dir / project_name
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
        click.echo("  Use  nspec init <projeto>  para iniciar um projeto.")
        click.echo("  Use  nspec --help  para ver todos os comandos.\n")


# ---------------------------------------------------------------------------
# nspec init
# ---------------------------------------------------------------------------

@main.command("init")
@click.argument("project_name")
@click.option("--force", is_flag=True, default=False, help="Sobrescreve skills existentes.")
@click.option(
    "--target",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Diretório base onde o projeto será criado.",
)
def init(project_name: str, force: bool, target: Path | None):
    """
    Inicializa um novo projeto NexusSpec e oferece abrir no editor.

    \b
    Exemplos:
      nspec init meu-projeto
      nspec init .
      nspec init meu-projeto --force
    """
    target_dir = _run_init(project_name, force, target)
    _tool_menu(
        str(target_dir),
        on_tool_selected=lambda choice, project_dir: _generate_skills_for_tool(
            project_dir=project_dir,
            tool_choice=choice,
            overwrite=force,
        ),
    )


# ---------------------------------------------------------------------------
# nspec add
# ---------------------------------------------------------------------------

@main.command("add")
@click.option("--force", is_flag=True, default=False, help="Sobrescreve skills existentes.")
def add(force: bool):
    """
    Adiciona o NexusSpec em um projeto já existente.

    \b
    Exemplos:
      nspec add
      nspec add --force
    """
    target_dir = Path.cwd()
    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style(f"  Adicionando NexusSpec em: {target_dir}\n", fg="white"))

    _create_docs_structure(target_dir)
    click.echo(click.style("  ✔  Estrutura NexusSpec verificada", fg="green"))

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
# nspec open
# ---------------------------------------------------------------------------

@main.command("open")
@click.argument("path", default=".", required=False)
def open_project(path: str):
    """
    Abre um projeto existente no editor escolhido.

    \b
    Exemplos:
      nspec open
      nspec open meu-projeto
    """
    target = Path(path).resolve()
    if not target.exists():
        click.echo(click.style(f"  ✗  Caminho não encontrado: {target}", fg="red"))
        raise SystemExit(1)
    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style(f"  Projeto: {target}\n", fg="white"))
    _tool_menu(str(target))


# ---------------------------------------------------------------------------
# nspec skills
# ---------------------------------------------------------------------------

@main.group("skills")
def skills():
    """Gerencia skills das ferramentas integradas."""
    pass


@skills.command("add")
@click.option(
    "--tool",
    "tool",
    required=True,
    type=click.Choice(sorted(SKILLS_TOOL_LABELS.keys()), case_sensitive=False),
    help="Ferramenta alvo para gerar skills.",
)
@click.option(
    "--skill",
    "skill",
    default=None,
    help="Nome da skill para gerar (ex: prd).",
)
@click.option("--force", is_flag=True, default=False, help="Sobrescreve skills existentes.")
def skills_add(tool: str, skill: str | None, force: bool):
    """
    Gera skills a partir dos templates do NexusSpec.

    \b
    Exemplos:
      nspec skills add --tool vscode
      nspec skills add --tool claude --force
    """
    tool_key = tool.lower()
    tool_label = SKILLS_TOOL_LABELS[tool_key]
    project_dir = Path.cwd()

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style(f"  Gerando skills para {tool_label} em: {project_dir}\n", fg="white"))

    _generate_skills_for_tool(
        project_dir=project_dir,
        tool_choice=tool_key,
        overwrite=force,
        skill=skill,
    )


@skills.command("remove")
@click.option(
    "--tool",
    "tool",
    required=True,
    type=click.Choice(sorted(SKILLS_TOOL_LABELS.keys()), case_sensitive=False),
    help="Ferramenta alvo para remover skills.",
)
@click.option(
    "--skill",
    "skill",
    default=None,
    help="Nome da skill para remover (ex: prd).",
)
@click.option("--yes", is_flag=True, default=False, help="Remove sem confirmação.")
def skills_remove(tool: str, skill: str | None, yes: bool):
    """
    Remove o diretório de skills da ferramenta escolhida.

    \b
    Exemplos:
      nspec skills remove --tool cursor
      nspec skills remove --tool antigravity --yes
    """
    tool_key = tool.lower()
    tool_label = SKILLS_TOOL_LABELS[tool_key]
    project_dir = Path.cwd()
    target_dir = project_dir / SKILLS_TOOL_DIRS[tool_key]

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style(f"  Removendo skills de {tool_label} em: {project_dir}\n", fg="white"))

    if skill:
        target_path = _skill_target_path(project_dir, tool_key, skill)
        if not target_path.exists():
            click.echo(click.style(f"  ⚠  Skill não encontrada: {target_path.relative_to(project_dir)}", fg="yellow"))
            return

        if not yes:
            if not click.confirm(
                f"Remover {target_path.relative_to(project_dir)}?",
                default=False,
            ):
                click.echo(click.style("  Operação cancelada.", fg="bright_black"))
                return

        if target_path.is_dir():
            shutil.rmtree(target_path)
        else:
            target_path.unlink()

        _cleanup_empty_skill_dirs(project_dir, tool_key)
        click.echo(click.style(
            f"  ✔  Skill removida: {target_path.relative_to(project_dir)}",
            fg="green",
        ))
        return

    if not target_dir.exists():
        relative_path = SKILLS_TOOL_DIRS[tool_key]
        click.echo(click.style(f"  ⚠  Nenhuma skill encontrada em {relative_path}.", fg="yellow"))
        return

    if not target_dir.is_dir():
        click.echo(click.style(f"  ✗  Caminho inválido: {target_dir}", fg="red"))
        raise SystemExit(1)

    if not yes:
        relative_path = SKILLS_TOOL_DIRS[tool_key]
        if not click.confirm(
            f"Remover {relative_path}? Isso apagará os arquivos gerados.",
            default=False,
        ):
            click.echo(click.style("  Operação cancelada.", fg="bright_black"))
            return

    shutil.rmtree(target_dir)
    _cleanup_empty_skill_dirs(project_dir, tool_key)
    click.echo(click.style(f"  ✔  Skills removidas: {SKILLS_TOOL_DIRS[tool_key]}", fg="green"))


# ---------------------------------------------------------------------------
# nspec task
# ---------------------------------------------------------------------------

@main.group("task")
def task():
    """Gerencia tarefas do projeto NexusSpec."""
    pass


@task.command("new")
@click.option("--name", "-n", default=None, help="Nome da feature (use hífens, ex: autenticacao-usuario).")
@click.option(
    "--target",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Diretório do projeto NexusSpec.",
)
def task_new(name: str | None, target: Path | None):
    """
    Cria a estrutura de uma nova tarefa interativamente.

    \b
    Exemplos:
      nspec task new
      nspec task new --name autenticacao-usuario
    """
    target_dir = target if target is not None else Path.cwd()

    # Verifica se é um projeto NexusSpec
    if not _is_nexusspec_project(target_dir):
        click.echo(click.style("  ✗  Nenhum projeto NexusSpec encontrado neste diretório.", fg="red"))
        click.echo(click.style("     Execute nspec init <projeto> primeiro.", fg="red"))
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
    feature_dir = target_dir / SPECS_DIR / name_slug
    feature_dir.mkdir(parents=True, exist_ok=True)

    _scaffold_file(
        feature_dir / "spec.md",
        f"# Spec — {name}\n\n> Execute a skill techspec na sua ferramenta de IA.\n",
    )
    _scaffold_file(
        feature_dir / "design.md",
        f"# Design — {name}\n\n> Gerado pelo techspec.md.\n",
    )
    _scaffold_file(
        feature_dir / "task.md",
        f"# Tasks — {name}\n\n"
        "> Gerado pela skill task. Checklist de implementação.\n\n"
        "## Pendente\n\n"
        "- [ ] \n\n"
        "## Concluído\n\n",
    )
    _scaffold_file(
        feature_dir / "verify.md",
        f"# Verify — {name}\n\n> Execute a skill verify após o apply.\n",
    )

    click.echo()
    click.echo(click.style(f"  ✔  Feature criada: {name_slug}", fg="green"))
    click.echo(click.style(f"     → features/specs/{name_slug}/spec.md", fg="bright_black"))
    click.echo(click.style(f"     → features/specs/{name_slug}/design.md", fg="bright_black"))
    click.echo(click.style(f"     → features/specs/{name_slug}/task.md", fg="bright_black"))
    click.echo(click.style(f"     → features/specs/{name_slug}/verify.md", fg="bright_black"))

    click.echo()
    click.echo(click.style("  Próximo passo no seu agente de IA:", fg="white"))
    click.echo(click.style("    techspec", fg="cyan"))
    click.echo()


def _get_feature_progress(feature_dir: Path) -> str:
    task_file = feature_dir / "task.md"
    if not task_file.exists():
        return "sem task.md"
    content = task_file.read_text(encoding="utf-8")
    content = re.sub(r"^\s*-\s*\[\s\]\s*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\s*-\s*\[x\]\s*$", "", content, flags=re.MULTILINE)
    done = content.count("[x]")
    pending = content.count("[ ]")
    total = done + pending
    if total == 0:
        return "sem tasks"
    return f"{done}/{total} tasks"


@task.command("status")
@click.option(
    "--target",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Diretório do projeto NexusSpec.",
)
def task_status(target: Path | None):
    """
    Exibe o status de todas as tarefas do projeto.

    \b
    Exemplos:
      nspec task status
    """
    target_dir = target if target is not None else Path.cwd()
    specs_dir = target_dir / SPECS_DIR

    if not specs_dir.exists():
        click.echo(click.style("  ✗  Nenhuma pasta features/specs encontrada.", fg="red"))
        raise SystemExit(1)

    features = sorted([
        d for d in specs_dir.iterdir() if d.is_dir() and d.name != ".gitkeep"
    ], key=lambda d: d.name)

    if not features:
        click.echo(click.style("\n  Nenhuma feature encontrada.\n", fg="yellow"))
        click.echo(click.style("  Use  nspec task new --name nome-da-feature  para criar uma.\n", fg="bright_black"))
        return

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style("  Status das features\n", bold=True))
    click.echo(f"  {'Feature':<30} {'Progresso':<18}")
    click.echo(f"  {'─'*30} {'─'*18}")

    for feature_dir in features:
        progress = _get_feature_progress(feature_dir)
        click.echo(f"  {feature_dir.name:<30} {progress:<18}")

    click.echo()


@task.command("archive")
@click.argument("feature_name")
@click.option(
    "--target",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Diretório do projeto NexusSpec.",
)
def task_archive(feature_name: str, target: Path | None):
    """
    Move uma feature concluída de features/specs para features/done.

    \b
    Exemplos:
      nspec task archive autenticacao-usuario
    """
    target_dir = target if target is not None else Path.cwd()
    source = target_dir / SPECS_DIR / feature_name
    dest = target_dir / ARCHIVE_DIR / feature_name

    if not source.exists():
        click.echo(click.style(f"  ✗  Feature '{feature_name}' não encontrada em features/specs.", fg="red"))
        raise SystemExit(1)

    if dest.exists():
        click.echo(click.style(f"  ✗  Já existe '{feature_name}' em features/done.", fg="yellow"))
        raise SystemExit(1)

    import shutil
    task_file = source / "task.md"
    if task_file.exists():
        pending = task_file.read_text(encoding="utf-8").count("[ ]")
        if pending > 0:
            click.echo(click.style(
                f"  ⚠ atenção: {pending} task(s) ainda pendente(s) no task.md.",
                fg="yellow"
            ))
            click.echo(click.style(
                "     execute apply.md e verify.md antes de arquivar.\n",
                fg="bright_black"
            ))

    shutil.move(str(source), str(dest))
    click.echo(click.style(f"\n  ✅  '{feature_name}' arquivada com sucesso!\n", fg="green"))
    click.echo(click.style(f"     → features/done/{feature_name}/\n", fg="bright_black"))


@task.command("done")
@click.argument("task_id")
def task_done(task_id: str):
    """
    Marca uma tarefa como concluída no implementation_plan.md.

    \b
    Exemplos:
      nspec task done 001
      nspec task done tarefa-001
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
# nspec update
# ---------------------------------------------------------------------------

@main.command("update")
@click.option("--force", is_flag=True, default=False, help="Sobrescreve skills com a versão mais recente.")
def update(force: bool):
    """
    Atualiza as skills do projeto para a versão mais recente do NexusSpec.

    \b
    Exemplos:
      nspec update
      nspec update --force
    """
    target_dir = Path.cwd()

    if not _is_nexusspec_project(target_dir):
        click.echo(click.style("  ✗  Nenhum projeto NexusSpec encontrado neste diretório.", fg="red"))
        raise SystemExit(1)

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style("  Atualizando skills...\n", fg="white"))

    _tool_menu(
        str(target_dir),
        on_tool_selected=lambda choice, project_dir: _generate_skills_for_tool(
            project_dir=project_dir,
            tool_choice=choice,
            overwrite=force,
        ),
    )

    click.echo()


# ---------------------------------------------------------------------------
# nspec list
# ---------------------------------------------------------------------------

@main.command("list")
def list_templates():
    """Lista as skills disponíveis no NexusSpec."""
    click.echo(click.style("\n  Skills disponíveis no NexusSpec:\n", fg="cyan", bold=True))
    descriptions = {
        "prd":      "Gera o PRD principal do produto",
        "techspec": "Gera a TechSpec de uma feature",
        "task":     "Gera o checklist de implementação",
        "apply":    "Implementa tasks pendentes automaticamente",
        "verify":   "Verifica implementação contra a spec",
    }
    click.echo(click.style("  Use o nome da skill na sua ferramenta de IA:\n", fg="bright_black"))
    for name, desc in descriptions.items():
        click.echo(f"  {click.style(name, fg='yellow', bold=True)}")
        click.echo(f"    {desc}\n")
