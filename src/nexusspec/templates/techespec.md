---
name: techespec
description: [02] Gera a TechSpec técnica de uma feature. Execute após ter o PRD e antes de criar as tasks.
allowed-tools: Read, Write
---

Você é um engenheiro sênior.

Antes de começar, leia:
- `.nexus/context.md`
- `specs/prd/prd.md`
- `specs/architecture/architecture.md`
- O arquivo `specs/changes/[nome-da-feature]/spec.md` se já existir

Faça as perguntas **uma de cada vez** com sugestões contextuais.

---

**Pergunta 1:** Qual é o nome da feature? (use o mesmo nome da pasta em specs/changes)

**Pergunta 2:** Esta feature é frontend, backend ou ambos?

Se a resposta for **backend** ou **ambos**, faça a próxima pergunta:

**Pergunta 3:** Para o backend, qual linguagem, framework e banco de dados serão utilizados?

Se a resposta for **frontend** ou **ambos**, faça a próxima pergunta:

**Pergunta 4:** Para o frontend, qual linguagem e framework serão utilizados?

**Pergunta 5:** Quais arquivos existentes serão modificados?

**Pergunta 6:** Esta feature introduz novos modelos de dados ou altera existentes?

**Pergunta 7:** Existe integração com serviços externos ou APIs?

**Pergunta 8:** Quais são os maiores riscos técnicos?

**Pergunta 9:** Como será testada?

---

Com base nas respostas, gere e salve:

**`specs/changes/[nome-da-feature]/spec.md`** com:
- Comportamento esperado em formato Given/When/Then
- Casos de borda e erros esperados

**`specs/changes/[nome-da-feature]/design.md`** com:
1. Resumo técnico e trade-offs
2. Componentes criados ou modificados
3. Modelo de dados (se aplicável)
4. Contrato de interface (se aplicável): endpoint, request, response
5. Ordem de implementação (passos numerados)
6. Testes: o que, como e onde testar
7. Riscos e mitigações
8. Diagrama em Mermaid (fluxo ou estados, conforme a feature)

Escreva em português.

Após salvar os arquivos, atualize `.nexus/context.md` com:
- Resumo da feature e objetivo técnico
- Stack definida (backend e/ou frontend)
- Decisões arquiteturais, integrações e riscos
- Arquivos criados/modificados
- Status da feature (ex: "TechSpec criada")

Ao finalizar todas as perguntas e salvar os arquivos, oriente explicitamente o usuário a executar a próxima skill: `/tasks.md`.
