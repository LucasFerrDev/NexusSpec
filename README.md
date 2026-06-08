# NexusSpec

> CLI para workflows de Spec-Driven Development com GitHub Copilot (e outros agentes de IA).

NexusSpec padroniza como times criam e mantêm documentação de produto antes de escrever código, seguindo o fluxo: **PRD → TechSpec → Task → Apply → Verify**.

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

Ao escolher a ferramenta no menu final do `init`, o NexusSpec gera automaticamente as skills para a plataforma selecionada.

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

### Ver skills disponíveis

```bash
nspec list
```

### Gerar skills manualmente

```bash
nspec skills add --tool vscode
nspec skills add --tool claude --force
nspec skills add --tool cursor --skill prd
```

### Remover skills de uma ferramenta

```bash
nspec skills remove --tool cursor
nspec skills remove --tool antigravity --yes
nspec skills remove --tool vscode --skill prd
```

---

## Integração automática de skills

Durante `nspec init` e `nspec add`, ao selecionar a ferramenta no menu, os templates internos são convertidos para o formato de skills correspondente.

### GitHub Copilot / VSCode

Cada prompt vira uma skill em:

```text
.github/skills/<nome-da-skill>/SKILL.md
```

Exemplo:

Exemplo: `.github/skills/prd/SKILL.md`

### Claude Code

Cada prompt vira um comando em:

```text
.claude/commands/<nome-da-skill>.md
```

### Cursor

Cada utility vira uma regra em:

```text
.cursor/rules/<nome-da-skill>.mdc
```

### Antigravity

Cada utility vira uma skill em:

```text
.agent/skills/<nome-da-skill>/SKILL.md
```

---

## Fluxo recomendado

Depois de rodar `nspec init`, use as skills instaladas na sua ferramenta de IA na ordem:

1. **prd** — gera `docs/prd/`
2. **techspec** — gera `features/specs/[feature]/spec.md` e `design.md`
3. **task** — gera `features/specs/[feature]/task.md`
4. **apply** — implementa as tasks pendentes
5. **verify** — valida a implementação e recomenda arquivamento

---

## Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip
- VS Code com GitHub Copilot, Claude Code, ou outro agente de IA compatível

---

## Estrutura do repositório

```
NexusSpec/
├── src/
│   └── nexusspec/
│       ├── __init__.py
│       ├── cli.py              ← lógica dos comandos
│       └── templates/          ← templates de skills empacotados
│           ├── prd.md
│           ├── techspec.md
│           ├── task.md
│           ├── apply.md
│           ├── verify.md
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