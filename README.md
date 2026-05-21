# NexusSpec

> CLI para workflows de Spec-Driven Development com GitHub Copilot (e outros agentes de IA).

NexusSpec padroniza como times criam e mantêm documentação de produto antes de escrever código, seguindo o fluxo: **PRD Geral → PRD Tarefa → TechSpec → Plano → Implementação**.

---

## Instalação

**Via pip (a partir do GitHub):**
```bash
pip install git+https://github.com/LucasFerrDev/NexusSpec.git
```

**Via uv (recomendado):**
```bash
uv tool install git+https://github.com/LucasFerrDev/NexusSpec.git
```

Após instalar, o comando `nexusspec` estará disponível globalmente no terminal.

---

## Uso

### Novo projeto

```bash
nexusspec init meu-projeto
```

Cria a pasta `meu-projeto/` com toda a estrutura pronta:

```
meu-projeto/
├── docs/
│   └── tarefas/
├── prompts/
│   ├── pdr_geral.md
│   ├── prd_tarefa.md
│   ├── techspec_tarefa.md
│   └── plan.md
└── README.md
```

Ao escolher a ferramenta no menu final do `init`, o NexusSpec também gera automaticamente as skills a partir de `prompts/` para a plataforma selecionada.

### Projeto existente

```bash
cd meu-projeto-existente
nexusspec add
```

Adiciona os prompts na pasta `prompts/` sem sobrescrever nada que já existe.

### Inicializar no diretório atual

```bash
nexusspec init .
```

### Sobrescrever prompts existentes

```bash
nexusspec init meu-projeto --force
nexusspec add --force
```

### Ver prompts disponíveis

```bash
nexusspec list
```

### Gerar skills manualmente

```bash
nexusspec skills add --tool vscode
nexusspec skills add --tool claude --force
nexusspec skills add --tool cursor --skill prd
```

### Remover skills de uma ferramenta

```bash
nexusspec skills remove --tool cursor
nexusspec skills remove --tool antigravity --yes
nexusspec skills remove --tool vscode --skill prd
```

---

## Integração automática de skills

Durante `nexusspec init` e `nexusspec add`, ao selecionar a ferramenta no menu, os prompts são convertidos para o formato de skills correspondente.

### GitHub Copilot / VSCode

Cada prompt vira uma skill em:

```text
.github/skills/<nome-do-prompt>/SKILL.md
```

Exemplo:

```text
prompts/prd.md -> .github/skills/prd/SKILL.md
```

### Claude Code

Cada prompt vira um comando em:

```text
.claude/commands/<nome-do-prompt>.md
```

### Cursor

Cada prompt vira uma regra em:

```text
.cursor/rules/<nome-do-prompt>.mdc
```

### Antigravity

Cada prompt vira uma skill em:

```text
.agent/skills/<nome-do-prompt>/SKILL.md
```

---

## Fluxo recomendado

Depois de rodar `nexusspec init`, abra o projeto no VS Code com GitHub Copilot (modo Agent) e siga a sequência:

### 1. PRD Geral
```
#pdr_geral.md
```
Saída: `docs/PRD_GERAL.md`

### 2. PRD da tarefa
```
#prd_tarefa.md
```
Saída: `docs/tarefas/tarefa-001/PRD_TAREFA_001.md`

### 3. TechSpec da tarefa
```
#techspec_tarefa.md
```
Saída: `docs/tarefas/tarefa-001/TECHSPEC_TAREFA_001.md`

### 4. Plano automático
```
#plan.md
```
O agente varre `docs/tarefas/`, identifica quais tarefas ainda não têm plano e gera automaticamente.

Saídas:
- `docs/tarefas/tarefa-001/PLANO_TAREFA_001.md`
- `implementation_plan.md` (raiz do projeto — visão consolidada de todas as tarefas)

### 5. Implementação
```
Implemente o plano salvando os arquivos na raiz do projeto
```

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
│       └── templates/          ← prompts empacotados
│           ├── pdr_geral.md
│           ├── prd_tarefa.md
│           ├── techspec_tarefa.md
│           └── plan.md
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