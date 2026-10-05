# NexusSpec

> CLI para workflows de Spec-Driven Development com GitHub Copilot (e outros agentes de IA).

NexusSpec padroniza como times criam e mantêm documentação de produto antes de escrever código, seguindo o fluxo: **PRD → Specify → Task → Apply → Verify**.

Para um passo a passo completo do fluxo, veja o [tutorial](docs/tutorial.md).

---

## Instalação

**Via pip (em um ambiente virtual):**
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install git+https://github.com/LucasFerrDev/NexusSpec.git
```

**Via uv (recomendado):**
```bash
uv tool install git+https://github.com/LucasFerrDev/NexusSpec.git
```

> Se o seu sistema bloquear `pip install` globalmente, use um virtualenv como acima.

Após instalar, o comando `nspec` estará disponível no terminal do ambiente ativo.

### Atualizar a CLI

```bash
uv tool upgrade nexusspec
# ou
pip install -U git+https://github.com/LucasFerrDev/NexusSpec.git
```

Depois de atualizar a CLI, rode `nspec update` dentro de cada projeto para regenerar as skills com os templates novos.

---

## Uso

### Novo projeto

```bash
nspec init meu-projeto
```

Cria a pasta `meu-projeto/` com toda a estrutura pronta:

```
meu-projeto/
├── docs/
│   ├── prd/
│   │   ├── prd.md
│   │   ├── personas.md
│   │   └── metrics.md
│   └── architecture/
│       ├── architecture.md
│       └── epics.md
├── features/
│   ├── specs/
│   │   └── .gitkeep
│   └── done/
│       └── .gitkeep
└── README.md
```

Ao escolher a ferramenta no menu final do `init`, o NexusSpec gera automaticamente as skills para a plataforma selecionada e abre o projeto nela.

### Projeto existente

```bash
cd meu-projeto-existente
nspec add
```

Adiciona a estrutura NexusSpec e gera skills via menu.

### Inicializar no diretório atual

```bash
nspec init .
```

### Sobrescrever skills existentes

```bash
nspec init meu-projeto --force
nspec add --force
```

### Abrir o projeto no editor

```bash
nspec open                # projeto no diretório atual
nspec open meu-projeto
```

Exibe o menu de ferramentas (Antigravity, Claude Code, Codex CLI, Cursor, VSCode) e abre o projeto na escolhida. Não gera nem altera skills.

### Ver skills disponíveis

```bash
nspec list
```

### Gerar skills manualmente

```bash
nspec skills add --tool vscode
nspec skills add --tool codex
nspec skills add --tool claude --force
nspec skills add --tool cursor --skill prd
```

Ferramentas aceitas em `--tool`: `antigravity`, `claude`, `codex`, `cursor`, `vscode`. Sem `--force`, arquivos já existentes são mantidos.

### Remover skills de uma ferramenta

```bash
nspec skills remove --tool cursor
nspec skills remove --tool codex --skill prd
nspec skills remove --tool antigravity --yes
nspec skills remove --tool vscode --skill prd
```

### Atualizar as skills do projeto

```bash
nspec update                 # regenera todas as ferramentas com skills instaladas
nspec update --tool claude   # regenera só uma ferramenta
```

Sem `--tool`, o comando detecta quais ferramentas já têm skills no projeto (pelos diretórios `.github/skills`, `.claude/commands`, `.agents/skills`, `.cursor/rules` e `.agent/skills`) e regenera todas, **sobrescrevendo** os arquivos. Não abre o editor.

> `nspec update` atualiza as skills do projeto, não a CLI. Para atualizar a CLI, veja [Atualizar a CLI](#atualizar-a-cli).

### Gerenciar features

```bash
nspec task new --name autenticacao-usuario     # cria features/specs/autenticacao-usuario/
nspec task status                              # progresso ([x]/total) de cada feature
nspec task done autenticacao-usuario 1         # conclui a 1ª task pendente
nspec task done autenticacao-usuario "login"   # conclui a task pendente que contém "login"
nspec task archive autenticacao-usuario        # move a feature para features/done/
nspec task archive autenticacao-usuario --yes  # arquiva sem confirmação
```

- `task new` cria `spec.md`, `design.md`, `task.md` e `verify.md` na pasta da feature.
- `task done <feature> <índice-ou-texto>` marca o item do `task.md` como `[x]` e o move para a seção `## Concluído`. O índice conta apenas as tasks pendentes, a partir de 1; o texto é comparado sem diferenciar maiúsculas e precisa identificar uma única task.
- `task archive` pede confirmação quando o `task.md` ainda tem tasks pendentes; use `--yes` para pular.

Todos os subcomandos de `task` aceitam `--target <diretório>` para operar em um projeto fora do diretório atual.

### Customizar os templates (pasta `prompts/`)

Por padrão as skills são geradas a partir dos templates empacotados com o NexusSpec. Se o projeto tiver uma pasta `prompts/` na raiz, **somente** os arquivos `*.md` dessa pasta são usados no lugar dos templates internos:

```
meu-projeto/
└── prompts/
    ├── prd.md        ← substitui o template prd
    └── review.md     ← skill nova, gerada como "review"
```

O nome do arquivo define o nome da skill. Se o template tiver frontmatter com `name` e `description`, esses valores são usados nos arquivos gerados; caso contrário, cada provider usa um valor padrão. Para partir dos templates originais, copie-os de `src/nexusspec/templates/`.

---

## Integração automática de skills

Durante `nspec init` e `nspec add`, ao selecionar a ferramenta no menu, os templates são convertidos para o formato de skills correspondente.

### GitHub Copilot / VSCode

Cada prompt vira uma skill em:

```text
.github/skills/<nome-da-skill>/SKILL.md
```

Exemplo: `.github/skills/prd/SKILL.md`

### Claude Code

Cada prompt vira um comando em:

```text
.claude/commands/<nome-da-skill>.md
```

### OpenAI Codex

Cada prompt vira uma skill local do repositório em:

```text
.agents/skills/<nome-da-skill>/SKILL.md
```

O frontmatter sempre contém `name` e `description`. As skills podem ser usadas explicitamente no Codex com `$nome-da-skill` ou descobertas automaticamente a partir do campo `description`.

### Cursor

Cada prompt vira uma regra em:

```text
.cursor/rules/<nome-da-skill>.mdc
```

O frontmatter da regra (`description`, `globs`, `alwaysApply`) é mesclado ao frontmatter do template.

### Antigravity

Cada prompt vira uma skill em:

```text
.agent/skills/<nome-da-skill>/SKILL.md
```

---

## Como funciona a geração de skills

A geração de skills fica em `src/nexusspec/integrations/skills/` e separa **o que** é gerado (os templates) de **como** cada ferramenta espera recebê-lo (os providers). São quatro peças:

```
 cli.py  ──►  SkillsGeneratorService  ──►  SkillProviderFactory  ──►  SkillProvider (Protocol)
                     │                                                  ├─ CopilotSkillProvider
                     ▼                                                  ├─ ClaudeCodeSkillProvider
               prompt_loader                                            ├─ CodexSkillProvider
        (templates do pacote ou prompts/)                               ├─ CursorSkillProvider
                     │                                                  └─ AntigravitySkillProvider
                     ▼
          list[PromptTemplate]  ─────────────────────────────────────────►  GenerationReport
```

**1. `prompt_loader` — carregamento dos templates** (`providers/shared/prompt_loader.py`)

`load_prompt_templates(project_dir)` decide a origem dos templates: a pasta `prompts/` do projeto, se existir, ou os templates empacotados em `nexusspec.templates` (ignorando os arquivos `_legacy_*`). Cada arquivo vira um `PromptTemplate` imutável com `name`, `stem`, `source_path`, `content` e, lidos do frontmatter YAML por `read_template_metadata`, os campos opcionais `skill_name` e `description`.

**2. `SkillProvider` — contrato por ferramenta** (`contracts/provider.py`)

`SkillProvider` é um `typing.Protocol` com um atributo `name` e um método `generate(project_dir, prompts, overwrite) -> GenerationReport`. Cada ferramenta tem uma classe que satisfaz o contrato por tipagem estrutural, sem herança: ela conhece apenas o caminho e o formato de arquivo da sua plataforma. Os providers que precisam de frontmatter próprio (Cursor, Antigravity, Codex) usam `shared/frontmatter.py` para **mesclar** seus campos aos do template, evitando blocos duplicados. O `GenerationReport` devolve os arquivos criados e os pulados (já existentes sem `--force`).

**3. `SkillProviderFactory` — resolução do provider** (`factories/provider_factory.py`)

Traduz a escolha do usuário — o rótulo do menu (`"Claude Code"`) ou a chave do `--tool` (`"claude"`) — para a instância do provider correspondente. Adicionar uma ferramenta nova exige apenas criar o provider e registrá-lo na factory.

**4. `SkillsGeneratorService` — orquestração** (`services/skills_generator.py`)

Ponto de entrada usado pela CLI: resolve o provider pela factory, carrega os templates (ou recebe uma lista já filtrada, como no `--skill`) e delega a geração. A CLI só lida com interação e mensagens; o service não conhece detalhes de nenhuma ferramenta.

Esse desenho aplica o princípio aberto/fechado: o fluxo de geração é o mesmo para todas as ferramentas, e as diferenças entre plataformas ficam isoladas nos providers.

---

## Fluxo recomendado

Depois de rodar `nspec init`, use as skills instaladas na sua ferramenta de IA na ordem:

1. **prd** — gera `docs/prd/`
2. **specify** — gera `features/specs/[feature]/spec.md` e `design.md`
3. **task** — gera `features/specs/[feature]/task.md`
4. **apply** — implementa as tasks pendentes
5. **verify** — valida a implementação e recomenda arquivamento

Detalhes e exemplos no [tutorial](docs/tutorial.md).

---

## Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip
- VS Code com GitHub Copilot, Claude Code, ou outro agente de IA compatível

---

## Desenvolvimento

```bash
uv sync           # instala dependências, incluindo o grupo dev (pytest, pyyaml)
uv run pytest     # roda a suíte de testes
```

---

## Estrutura do repositório

```
NexusSpec/
├── src/
│   └── nexusspec/
│       ├── __init__.py
│       ├── cli.py                    ← lógica dos comandos
│       ├── integrations/
│       │   └── skills/
│       │       ├── contracts/        ← PromptTemplate, GenerationReport, SkillProvider
│       │       ├── factories/        ← SkillProviderFactory
│       │       ├── providers/        ← um provider por ferramenta
│       │       │   └── shared/       ← prompt_loader e frontmatter
│       │       └── services/         ← SkillsGeneratorService
│       └── templates/                ← templates de skills empacotados
│           ├── prd.md
│           ├── specify.md
│           ├── task.md
│           ├── apply.md
│           └── verify.md
├── tests/                            ← suíte pytest
├── CHANGELOG.md
├── docs/
│   └── tutorial.md
├── pyproject.toml
└── README.md
```

---


## Licença

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Este projeto está sob a licença MIT. 
Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
