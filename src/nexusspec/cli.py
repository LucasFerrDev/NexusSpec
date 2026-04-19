"""NexusSpec CLI — comandos principais."""

import click
import os
import shutil
from importlib.resources import files
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
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


def _get_template(filename: str) -> str:
    """Retorna o conteúdo de um template empacotado."""
    return files("nexusspec.templates").joinpath(filename).read_text(encoding="utf-8")


def _copy_prompts(target_dir: Path, overwrite: bool = False) -> list[str]:
    """
    Copia os templates de prompts para target_dir/prompts/.
    Retorna lista de arquivos copiados.
    """
    prompts_path = target_dir / PROMPTS_DIR
    prompts_path.mkdir(parents=True, exist_ok=True)

    copied = []
    skipped = []

    for template_name in TEMPLATES:
        dest = prompts_path / template_name
        if dest.exists() and not overwrite:
            skipped.append(template_name)
            continue
        content = _get_template(template_name)
        dest.write_text(content, encoding="utf-8")
        copied.append(template_name)

    if skipped:
        click.echo(
            click.style(
                f"  ⚠  Ignorados (já existem): {', '.join(skipped)}", fg="yellow"
            )
        )
        click.echo(
            click.style("     Use --force para sobrescrever.", fg="yellow")
        )

    return copied


def _create_docs_structure(target_dir: Path):
    """Cria a estrutura de pastas docs/tarefas/."""
    for subdir in DOCS_SUBDIRS:
        (target_dir / DOCS_DIR / subdir).mkdir(parents=True, exist_ok=True)

    # .gitkeep para o git rastrear a pasta vazia
    gitkeep = target_dir / DOCS_DIR / "tarefas" / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()


def _create_readme(target_dir: Path, project_name: str):
    """Cria um README.md inicial se não existir."""
    readme = target_dir / "README.md"
    if readme.exists():
        return

    content = f"""# {project_name}

> Projeto inicializado com [NexusSpec](https://github.com/LucasFerrDev/NexusSpec).

## Fluxo NexusSpec

1. **PRD Geral** — `#pdr_geral.md`
2. **PRD da tarefa** — `#prd_tarefa.md`
3. **TechSpec da tarefa** — `#techspec_tarefa.md`
4. **Plano automático** — `#plan.md`
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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(package_name="nexusspec")
def main():
    """NexusSpec — CLI para workflows de Spec-Driven Development."""
    pass


# ---------------------------------------------------------------------------
# nexusspec init <PROJECT_NAME>
# nexusspec init .
# ---------------------------------------------------------------------------

@main.command("init")
@click.argument("project_name")
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Sobrescreve arquivos de prompt existentes.",
)
def init(project_name: str, force: bool):
    """
    Inicializa um novo projeto NexusSpec.

    \b
    Exemplos:
      nexusspec init meu-projeto
      nexusspec init .
      nexusspec init meu-projeto --force
    """
    click.echo(click.style(BANNER, fg="cyan"))

    # Resolver diretório alvo
    if project_name == ".":
        target_dir = Path.cwd()
        display_name = target_dir.name
    else:
        target_dir = Path.cwd() / project_name
        display_name = project_name

        if target_dir.exists() and any(target_dir.iterdir()):
            if not force:
                click.echo(
                    click.style(
                        f"  ✗  A pasta '{project_name}' já existe e não está vazia.",
                        fg="red",
                    )
                )
                click.echo(
                    click.style("     Use --force para inicializar mesmo assim.", fg="red")
                )
                raise SystemExit(1)
        target_dir.mkdir(parents=True, exist_ok=True)

    click.echo(click.style(f"  Inicializando NexusSpec em: {target_dir}\n", fg="white"))

    # Estrutura de pastas
    _create_docs_structure(target_dir)
    click.echo(click.style("  ✔  Estrutura de pastas criada (docs/tarefas/)", fg="green"))

    # Prompts
    copied = _copy_prompts(target_dir, overwrite=force)
    if copied:
        click.echo(
            click.style(f"  ✔  Prompts copiados: {', '.join(copied)}", fg="green")
        )

    # README
    _create_readme(target_dir, display_name)
    click.echo(click.style("  ✔  README.md criado", fg="green"))

    # Resumo final
    click.echo()
    click.echo(click.style("  ─────────────────────────────────────────", fg="bright_black"))
    click.echo(click.style(f"  ✅  Projeto '{display_name}' pronto!", fg="bright_green", bold=True))
    click.echo()
    click.echo("  Próximo passo no seu agente de IA:")
    click.echo(click.style("    #pdr_geral.md", fg="cyan"))
    click.echo()


# ---------------------------------------------------------------------------
# nexusspec add
# ---------------------------------------------------------------------------

@main.command("add")
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Sobrescreve prompts existentes.",
)
def add(force: bool):
    """
    Adiciona os prompts NexusSpec em um projeto já existente.

    Executa no diretório atual. Não cria README nem sobrescreve
    arquivos existentes (a menos que --force seja passado).

    \b
    Exemplos:
      nexusspec add
      nexusspec add --force
    """
    target_dir = Path.cwd()

    click.echo(click.style(BANNER, fg="cyan"))
    click.echo(click.style(f"  Adicionando prompts NexusSpec em: {target_dir}\n", fg="white"))

    # Estrutura docs/tarefas se não existir
    _create_docs_structure(target_dir)
    click.echo(click.style("  ✔  Estrutura docs/tarefas/ verificada", fg="green"))

    # Prompts
    copied = _copy_prompts(target_dir, overwrite=force)
    if copied:
        click.echo(
            click.style(f"  ✔  Prompts adicionados: {', '.join(copied)}", fg="green")
        )

    click.echo()
    click.echo(click.style("  ─────────────────────────────────────────", fg="bright_black"))
    click.echo(click.style("  ✅  NexusSpec adicionado ao projeto!", fg="bright_green", bold=True))
    click.echo()
    click.echo("  Próximo passo no seu agente de IA:")
    click.echo(click.style("    #pdr_geral.md", fg="cyan"))
    click.echo()


# ---------------------------------------------------------------------------
# nexusspec list
# ---------------------------------------------------------------------------

@main.command("list")
def list_templates():
    """Lista os prompts disponíveis no NexusSpec."""
    click.echo(click.style("\n  Prompts disponíveis no NexusSpec:\n", fg="cyan", bold=True))
    descriptions = {
        "pdr_geral.md": "Gera o PRD Geral do produto (docs/PRD_GERAL.md)",
        "prd_tarefa.md": "Gera o PRD de uma tarefa específica",
        "techspec_tarefa.md": "Gera a TechSpec técnica de uma tarefa",
        "plan.md": "Identifica tarefas sem plano e gera automaticamente",
    }
    for name, desc in descriptions.items():
        click.echo(f"  {click.style(name, fg='yellow', bold=True)}")
        click.echo(f"    {desc}\n")
