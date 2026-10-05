# Tutorial: do PRD à feature arquivada

Este tutorial percorre o fluxo do NexusSpec do início ao fim:
**PRD → Specify → Task → Apply → Verify**. As skills são executadas no seu
agente de IA (Claude Code, Codex, Cursor, Copilot ou Antigravity); a CLI
`nspec` cuida da estrutura de pastas e do acompanhamento das features.

## 0. Preparar o projeto

```bash
nspec init meu-projeto
```

No menu final, escolha a ferramenta de IA. O NexusSpec cria `docs/` e
`features/`, gera as skills para a ferramenta e abre o projeto nela.

Para usar outra ferramenta depois, rode `nspec skills add --tool <ferramenta>`.

## 1. PRD — definir o produto

No agente, execute a skill **prd**. Ela faz perguntas guiadas, uma de cada
vez, e grava:

- `docs/prd/prd.md` — visão, objetivo, funcionalidades e escopo
- `docs/prd/personas.md` — perfis de usuário
- `docs/prd/metrics.md` — métricas de sucesso

O PRD é feito uma vez por produto e serve de contexto para todas as features.

## 2. Specify — especificar uma feature

Crie a pasta da feature pela CLI:

```bash
nspec task new --name autenticacao-usuario
```

Depois execute a skill **specify** no agente. Ela pergunta sobre stack,
componentes e arquivos afetados, e grava:

- `docs/architecture/architecture.md` — stack e padrões do projeto
- `features/specs/autenticacao-usuario/spec.md` — comportamento esperado (Given/When/Then)
- `features/specs/autenticacao-usuario/design.md` — design técnico

## 3. Task — gerar o checklist

Execute a skill **task**. Ela lê o PRD, a arquitetura, o `spec.md` e o
`design.md` e gera `features/specs/autenticacao-usuario/task.md`:

```markdown
# Tasks — autenticacao-usuario

## Pendente

- [ ] criar model de usuário
- [ ] criar endpoint de login

## Concluído
```

Acompanhe o progresso de todas as features com:

```bash
nspec task status
```

## 4. Apply — implementar

Execute a skill **apply**. Ela percorre `features/specs/`, implementa as tasks
pendentes e as move para `## Concluído` no `task.md`.

Se você implementar algo manualmente, marque a task pela CLI:

```bash
nspec task done autenticacao-usuario 1          # pela posição entre as pendentes
nspec task done autenticacao-usuario "login"    # por um trecho do texto
```

## 5. Verify — validar e arquivar

Execute a skill **verify**. Ela confere a implementação contra o `spec.md`, o
`design.md` e o `task.md` de cada feature e recomenda o arquivamento das que estão prontas.

```bash
nspec task archive autenticacao-usuario
```

A feature vai para `features/done/`. Se ainda houver tasks pendentes, a CLI
pede confirmação (use `--yes` para pular).

## Manter as skills atualizadas

Ao instalar uma versão nova do NexusSpec, regenere as skills do projeto:

```bash
uv tool upgrade nexusspec   # atualiza a CLI
nspec update                # regenera as skills das ferramentas instaladas
```
