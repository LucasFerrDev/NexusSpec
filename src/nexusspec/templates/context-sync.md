---
name: context-sync
description: Gera ou atualiza os arquivos de contexto específicos de cada ferramenta de IA (CLAUDE.md, AGENTS.md, .cursorrules). Execute sempre que o context.md mudar.
allowed-tools: Read, Write
---

Você é um engenheiro de DevEx.

Leia `.nexus/context.md` e gere os seguintes arquivos na raiz do projeto,
cada um adaptado para sua ferramenta:

**`CLAUDE.md`** — para Claude Code:
- Resumo do produto em 2 frases
- Stack técnica
- Restrições de implementação
- Onde fica cada artefato do framework
- Como usar os prompts em `prompts/`

**`AGENTS.md`** — para Codex/OpenAI:
- Mesmo conteúdo do CLAUDE.md adaptado para o formato AGENTS.md

**`.cursorrules`** — para Cursor/Windsurf:
- Versão compacta das regras, focada em estilo de código e restrições

Mantenha todos em português e sincronizados com o mesmo conteúdo de `.nexus/context.md`.
