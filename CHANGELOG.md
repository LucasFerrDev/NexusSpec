# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [0.2.0] - 2026-10-05

### Adicionado
- `nspec task done <feature> <índice-ou-texto>`: marca um item do `task.md` da feature como `[x]` e o move para `## Concluído`.
- `nspec update --tool <ferramenta>`; sem `--tool`, detecta as ferramentas com skills instaladas e regenera todas.
- `nspec task archive --yes`; sem a flag, o comando pede confirmação quando há tasks pendentes.
- `PromptTemplate` com os campos opcionais `skill_name` e `description`, lidos do frontmatter por `prompt_loader.read_template_metadata`.
- Módulo `providers/shared/frontmatter.py` para ler, gerar e mesclar frontmatter.
- Suíte de testes com pytest (`uv run pytest`).
- `docs/tutorial.md` com o fluxo PRD → Specify → Task → Apply → Verify.
- README: comandos `open`, `update` e `task`, override via `prompts/` e a seção "Como funciona a geração de skills".

### Alterado
- Perguntas das skills reduzidas de 29 para 7 (+1 condicional): o usuário define o "o quê"
  (problema, comportamento, limites) e a IA infere o "como" a partir dos docs e do código,
  apresentando checkpoints de aprovação. prd: 7 → 4; specify: 13 → 3 (+ stack só em projeto
  vazio); task, apply e verify: 3 → 0.
- specify passa a perguntar comportamento e critérios de aceite (antes inexistente) e não
  repete a stack a cada feature; prd passa a cobrir restrições e fora do escopo.
- verify grava o relatório em `features/specs/<feature>/verify.md`.
- prd grava o backlog de features em `docs/architecture/epics.md`; specify lista as
  features do backlog sem spec e cria a pasta da escolhida, sem precisar do terminal.
- `nspec task new` passa a ser opcional e gera o nome da pasta sem acentos
  (`Autenticação Usuário` → `autenticacao-usuario`).
- Nome da skill padronizado como `specify` (frontmatter do template, `nspec list`, README gerado, `task new` e metadados do Cursor).
- `nspec update` só regenera as skills, sempre sobrescrevendo, e não abre mais o editor. A opção `--force` foi removida.
- Cursor, Antigravity e Codex usam a `description` do template; os valores fixos anteriores viraram fallback.
- O frontmatter do provider é mesclado ao do template, sem gerar dois blocos (afetava Cursor e Antigravity).
- `_tool_menu` separado em `_select_tool` e `_open_tool`.

### Corrigido
- Claude Code não abria no terminal após o `init`/`open`: agora herda o terminal e usa o diretório do projeto como `cwd`, igual ao Codex (PR #8).
- `apply.md` sem o campo `name` no frontmatter.
- Codex: `SKILL.md` sempre tem `name` e `description`, inclusive para templates de `prompts/` sem frontmatter.
- Regra do Cursor para `specify` caía nos metadados genéricos.
- README: referência a `docs/tutorial.md` inexistente e `Specify.md` → `specify.md`.

### Removido
- Dependência do `task done` em `implementation_plan.md` (template legado `_legacy_plan.md`).
- `import shutil` duplicado em `task archive`.

## [0.1.0]

- Versão inicial.
