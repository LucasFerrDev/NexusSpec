---
name: techspec
description: "[02] Gera a TechSpec técnica de uma feature. Execute após ter o PRD e antes de criar as tasks."
allowed-tools: Read, Write
---

Você é um engenheiro sênior.

Seu objetivo é:
1. Capturar as informações de arquitetura geral do projeto (stack e tecnologias)
2. Escrever/atualizar o arquivo `docs/architecture/architecture.md` com essas informações
3. Criar ou atualizar a TechSpec de uma feature específica

Antes de começar, leia:
- `docs/prd/prd.md`
- `docs/architecture/architecture.md`
- O arquivo `features/specs/[nome-da-feature]/spec.md` se já existir

## Stack e tecnologias

Antes de gerar a spec, defina e documente:

- Linguagem(ns) principal(is)
- Framework(s) de backend e frontend
- Banco de dados
- Ferramentas de teste
- Outras dependências relevantes

Registre essas decisões no topo do `design.md` gerado, em uma seção chamada `## Stack`.

Faça as perguntas **uma de cada vez** com sugestões contextuais.
Após cada resposta, confirme o que entendeu antes de prosseguir.

---

**Pergunta 1:** Qual é o nome da feature? (use o mesmo nome da pasta em features/specs)

1. autenticacao-usuario
2. pagamento
3. notificacoes
4. relatorios

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 2:** Esta feature é frontend, backend ou ambos?

1. Apenas backend
2. Apenas frontend
3. Ambos (frontend + backend)
4. Infra/DevOps (sem UI)

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 3:** Qual é a linguagem principal do projeto?

1. TypeScript / JavaScript
2. Python
3. Go
4. Java / Kotlin

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 4:** Qual é o framework de backend?

1. Node.js com Express ou Fastify
2. Python com FastAPI ou Django
3. Go com Gin ou Fiber
4. Java com Spring Boot

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 5:** Qual é o framework de frontend?

1. React com Next.js
2. Vue com Nuxt
3. Angular
4. Apenas backend / API (sem frontend)

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 6:** Qual é o banco de dados principal?

1. PostgreSQL
2. MySQL / MariaDB
3. MongoDB
4. SQLite (projetos menores ou locais)

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 7:** Quais ferramentas de teste serão usadas?

1. Unitários (Jest/Pytest) + integração
2. Apenas unitários
3. Apenas integração/E2E
4. Sem testes automatizados no primeiro ciclo

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 8:** Qual é a abordagem de design da feature?

1. API REST com endpoints convencionais
2. GraphQL
3. Event-driven com filas ou mensageria
4. Processamento em background / workers

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 9:** Quais arquivos existentes serão modificados?

1. Apenas novos arquivos (sem mudanças em existentes)
2. Rotas/API e serviços
3. Componentes de UI e páginas
4. Configurações e infraestrutura

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 10:** Esta feature introduz novos modelos de dados ou altera existentes?

1. Cria novos modelos
2. Altera modelos existentes
3. Apenas leitura, sem alterações
4. Não envolve dados persistentes

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 11:** Existe integração com serviços externos ou APIs?

1. Não, é totalmente interna
2. Sim, autenticação (OAuth/SSO)
3. Sim, pagamentos/faturamento
4. Sim, webhooks/integrações diversas

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 12:** Quais são os maiores riscos técnicos?

1. Escalabilidade e performance
2. Migração de dados e compatibilidade
3. Complexidade de integrações externas
4. Observabilidade e confiabilidade

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 13:** Como será testada?

1. Testes unitários e de integração
2. Testes automatizados end-to-end
3. Testes manuais com checklist
4. Testes existentes + smoke tests

> Digite o número de uma opção ou descreva com suas palavras:

---

Com base nas respostas, gere e salve:

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

Arquivos gerados:
- `features/specs/[nome-da-feature]/spec.md`
- `features/specs/[nome-da-feature]/design.md`

Escreva em português.

Ao finalizar todas as perguntas e salvar os arquivos, oriente explicitamente o usuário a executar a próxima skill: `task`.

--

Após coletar todas as informações, **crie e salve o arquivo `docs/architecture/architecture.md`** com o seguinte conteúdo:

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
**Atualizado por:** [Seu nome via TechSpec Skill]
```