---
name: plan
description: Identifica automaticamente todas as tarefas sem plano de implementação e gera o plano para cada uma. Use sempre que quiser gerar ou atualizar o plano de implementação do projeto.
allowed-tools: Read, Write, Edit, ListDirectory
---

Você é um engenheiro sênior responsável por planejar a implementação de tarefas de software.

## Passo 1 — Leia o contexto do produto

Leia o arquivo `docs/PRD_GERAL.md` para entender o produto antes de qualquer coisa.

---

## Passo 2 — Descubra todas as tarefas existentes

Faça uma varredura no diretório `docs/tarefas/`.
Liste todas as subpastas no formato `tarefa-00X`.

Para cada pasta encontrada, registre:
- Nome da pasta (ex: `tarefa-001`)
- Se existe o arquivo `PRD_TAREFA_00X.md`
- Se existe o arquivo `TECHSPEC_TAREFA_00X.md`
- Se já existe o arquivo `PLANO_TAREFA_00X.md`

---

## Passo 3 — Identifique as tarefas sem plano

Uma tarefa está **pendente de plano** quando:
- Existe a pasta da tarefa
- Existe o `PRD_TAREFA_00X.md`
- Existe o `TECHSPEC_TAREFA_00X.md`
- **NÃO** existe ainda o `PLANO_TAREFA_00X.md`

Se todas as tarefas já tiverem plano, informe ao usuário e encerre.

---

## Passo 4 — Para cada tarefa pendente, gere o plano

Para cada tarefa identificada no Passo 3, faça o seguinte:

1. Leia `docs/tarefas/tarefa-00X/PRD_TAREFA_00X.md`
2. Leia `docs/tarefas/tarefa-00X/TECHSPEC_TAREFA_00X.md`
3. Gere o plano de implementação com a estrutura abaixo
4. Salve em `docs/tarefas/tarefa-00X/PLANO_TAREFA_00X.md`

### Estrutura do plano por tarefa

```markdown
# Plano de Implementação — Tarefa 00X: [Nome da Tarefa]

## Contexto
[Resumo do que esta tarefa entrega, extraído do PRD]

## Abordagem técnica
[Resumo da abordagem escolhida, extraído da TechSpec]

## Pré-requisitos
[Liste dependências externas, pacotes, configurações ou tarefas anteriores que precisam estar prontas]

## Passos de implementação

| # | Descrição | Depende de | Estimativa |
|---|-----------|------------|------------|
| 1 | [passo]   | —          | [tempo]    |
| 2 | [passo]   | Passo 1    | [tempo]    |
...

## Arquivos que serão criados ou modificados

| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `caminho/arquivo.ext` | criar | [o que faz] |
| `caminho/arquivo.ext` | modificar | [o que muda] |

## Critérios de conclusão
[Lista de verificações extraída dos Critérios de Aceite do PRD e da seção de Testes da TechSpec]

- [ ] [critério 1]
- [ ] [critério 2]

## Riscos e mitigações
[Extraído da seção de Riscos da TechSpec]
```

---

## Passo 5 — Atualize o `implementation_plan.md` na raiz do projeto

Após gerar (ou verificar) todos os planos individuais, atualize o arquivo `implementation_plan.md` na raiz do projeto.

Se o arquivo não existir, crie-o. Se já existir, atualize apenas as seções afetadas.

### Estrutura do `implementation_plan.md`

```markdown
# Plano de Implementação — [Nome do Produto]

> Gerado automaticamente com base nos PRDs e TechSpecs das tarefas.
> Última atualização: [data]

## Visão geral do produto
[Resumo extraído do PRD_GERAL.md]

## Status das tarefas

| Tarefa | Nome | Status | Plano |
|--------|------|--------|-------|
| tarefa-001 | [nome] | ⬜ pendente / 🔄 em andamento / ✅ concluída | [PLANO_TAREFA_001.md](docs/tarefas/tarefa-001/PLANO_TAREFA_001.md) |
| tarefa-002 | [nome] | ⬜ pendente | [PLANO_TAREFA_002.md](docs/tarefas/tarefa-002/PLANO_TAREFA_002.md) |

> **Legenda de status:**
> - ⬜ pendente — plano gerado, implementação não iniciada
> - 🔄 em andamento — implementação iniciada, não concluída
> - ✅ concluída — todos os critérios de aceite foram atendidos

## Próxima tarefa recomendada
[Indique qual tarefa deve ser executada a seguir, com base nas dependências entre tarefas]

## Dependências entre tarefas
[Se houver dependências, descreva aqui. Ex: "tarefa-002 depende de tarefa-001 estar concluída"]
```

---

## Regras gerais

- Nunca invente informações — use apenas o que está nos arquivos PRD e TechSpec da tarefa
- Se faltar o PRD ou a TechSpec de uma tarefa, informe ao usuário e pule essa tarefa
- Use português em toda a documentação gerada
- Mantenha os nomes de arquivo no padrão `PLANO_TAREFA_00X.md` (maiúsculas)
- O status inicial de toda tarefa recém-planejada é sempre **⬜ pendente**
