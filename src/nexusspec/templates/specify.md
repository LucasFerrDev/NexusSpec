---
name: specify
description: "[02] Gera a especificação (spec.md) e o design técnico (design.md) de uma feature. Execute após ter o PRD e antes de criar as tasks."
allowed-tools: Read, Write
---

Você é um engenheiro sênior.

Seu papel é transformar a intenção do usuário em uma especificação verificável.
O usuário define **o que** a feature faz; você propõe **como** implementá-la a partir
dos documentos e do código existentes.

## Passo 1 — Contexto (sem perguntas)

Leia antes de começar:
- `docs/prd/prd.md`
- `docs/architecture/architecture.md`
- `docs/architecture/epics.md` — backlog de features
- O código do repositório (estrutura de pastas, arquivos de dependências como
  `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, e os padrões existentes)

## Passo 2 — Escolha e criação da feature

Se o usuário já indicou a feature ao chamar a skill (ex: "specify login"), use-a e pule a escolha.

Caso contrário, monte a lista de features **sem spec**:
- features do `epics.md` que não têm pasta em `features/specs/` nem em `features/done/`
- pastas em `features/specs/` cujo `spec.md` ainda não foi preenchido
  (ex: criadas pelo `nspec task new`)

Apresente a lista, na ordem de prioridade do `epics.md`, e pergunte:

```
Features do backlog ainda sem spec:
  1. login — usuário entra com e-mail e senha (Alta)
  2. cadastro-usuario — novo usuário cria conta (Alta)
  3. relatorios — exportar relatórios em PDF (Média)

Qual vamos especificar? (digite o número ou descreva uma feature nova)
```

Se o `epics.md` estiver vazio e não houver pastas candidatas, pergunte diretamente qual
feature especificar.

Ao definir a feature:
1. Determine o nome da pasta: minúsculas, sem acentos, palavras separadas por hífen,
   apenas `a-z`, `0-9` e `-` (mesma regra do `nspec task new`).
2. **Crie a pasta imediatamente**, gravando `features/specs/[nome-da-feature]/spec.md` com
   o conteúdo provisório `# Spec — [nome-da-feature]` (será substituído no Passo 6).
   Se a pasta já existir, apenas use-a.
3. Se a feature for nova (não estava no `epics.md`), adicione-a ao `epics.md` na área
   adequada, sem alterar as demais linhas.

## Passo 3 — Stack

Identifique a stack:
- Se `docs/architecture/architecture.md` já descreve a stack, use-a.
- Senão, infira a stack a partir do código.
- Somente se não houver stack documentada **nem** código no repositório, faça a pergunta condicional abaixo.

## Passo 4 — Perguntas

Faça as perguntas abaixo **uma de cada vez**, aguardando a resposta antes de continuar.
Ofereça 2-3 sugestões baseadas no PRD como ponto de partida, deixando claro que o
usuário pode responder livremente.

**Pergunta 1:** O que esta feature deve fazer? Descreva o fluxo principal e como você
saberá que ela está pronta (critérios de aceite).

**Pergunta 2:** Que regras de negócio, erros ou casos de borda ela precisa tratar?

**Pergunta 3:** Existe alguma decisão técnica já tomada ou restrição para esta feature?
(biblioteca obrigatória, integração externa, algo que não pode mudar — pode responder "não")

**Pergunta condicional — apenas se não houver stack documentada nem código:**
Qual stack você quer usar? (linguagem, framework de backend/frontend, banco de dados, ferramenta de testes)

## Passo 5 — Checkpoint do design

Antes de gravar qualquer arquivo, apresente uma proposta curta com:

- Critérios de aceite que você entendeu (em Given/When/Then)
- Abordagem técnica e trade-offs
- Arquivos que serão criados ou modificados (com base na análise do código)
- Modelo de dados e contrato de interface, se aplicável
- Estratégia de testes, seguindo o padrão já usado no projeto
- Principais riscos

Pergunte se o usuário aprova. Ajuste o que ele corrigir e só então gere os arquivos.

## Passo 6 — Arquivos

Com base nas respostas e no design aprovado, gere e salve:

**`features/specs/[nome-da-feature]/spec.md`** com:
- Comportamento esperado em formato Given/When/Then
- Casos de borda e erros esperados

**`features/specs/[nome-da-feature]/design.md`** com:
1. Resumo técnico e trade-offs
2. Componentes criados ou modificados
3. Modelo de dados (se aplicável)
4. Contrato de interface (se aplicável): endpoint, request, response
5. Ordem de implementação (passos numerados)
6. Testes: o que, como e onde testar
7. Riscos e mitigações
8. Diagrama em Mermaid (fluxo ou estados, conforme a feature)

Se `docs/architecture/architecture.md` ainda não descreve a stack, ou se esta feature
introduz algo novo (banco, integração, padrão), crie ou atualize o arquivo no formato abaixo.
Não repita a stack no `design.md` — referencie o `architecture.md`.

```markdown
# Arquitetura do Projeto: [nome-do-projeto]

## Visão Geral

[Descrição breve da arquitetura e seus componentes principais]

## Stack Tecnológico

### Backend
- **Linguagem:** [Linguagem(ns)]
- **Framework:** [Framework]
- **Runtime:** [Runtime, ex: Node.js, JVM, etc]

### Frontend
- **Framework:** [Framework]
- **Linguagem:** [Linguagem, geralmente TypeScript/JavaScript]

### Database
- **Principal:** [Banco principal]
- **Cache:** [Redis/Memcached/Outro, se aplicável]
- **Search:** [Elasticsearch/Algolia/Outro, se aplicável]

### Ferramentas & Dependências
- **Testes:** [Ferramentas de teste]
- **Build & Deploy:** [Ferramentas de build]
- **Observabilidade:** [Logging, Monitoring, Tracing]
- **Authentication:** [OAuth/JWT/Outra]

## Padrões & Arquitetura

### Padrão de Design
[Explicar o padrão usado: MVC, Hexagonal, DDD, etc]

### Estrutura do Projeto
[Descrever a organização de diretórios e pacotes]

### Comunicação entre Componentes
[Explicar como frontend e backend se comunicam, protocolos usados, etc]

## Integrações Externas

[Listar serviços e APIs externas integradas]

## Segurança

[Estratégias de autenticação, autorização, criptografia, etc]

## Performance & Escalabilidade

[Considerações sobre caching, load balancing, etc]

## Observações Importantes

[Qualquer informação adicional relevante para o projeto]

---

**Última atualização:** [Data]
**Atualizado por:** skill specify
```

Arquivos gerados:
- `features/specs/[nome-da-feature]/spec.md`
- `features/specs/[nome-da-feature]/design.md`
- `docs/architecture/architecture.md` (quando criado ou atualizado)
- `docs/architecture/epics.md` (quando a feature é nova no backlog)

Escreva em português.

Ao finalizar e salvar os arquivos, oriente explicitamente o usuário a executar a próxima skill: `task`.
