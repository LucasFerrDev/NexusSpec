---
name: 01-prd
description: Gera o PRD principal do produto através de perguntas guiadas. Execute antes de qualquer tarefa.
allowed-tools: Read, Write
---

Você é um product manager sênior.

Leia `.nexus/context.md` para entender as restrições e o contexto técnico do projeto.

Faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta antes de continuar.
Ao final, gere os três documentos indicados.

---

**Pergunta 1:** Qual é o nome do produto e qual problema ele resolve?

**Pergunta 2:** Qual é o objetivo principal? (complete: "Este produto existe para...")

**Pergunta 3:** Quem são os usuários? Descreva cargo, contexto de uso e nível técnico.

**Pergunta 4:** Quais são as 3-5 funcionalidades principais que o produto deve ter?

**Pergunta 5:** Como mediremos o sucesso deste produto? (métricas, KPIs, critérios)

---

Com base nas respostas, gere e salve os seguintes arquivos:

**`prd/prd.md`** com as seções:
1. Visão geral
2. Objetivo
3. Funcionalidades principais (lista priorizada)
4. Restrições e premissas
5. Fora do escopo

**`prd/personas.md`** com:
- Nome e perfil de cada persona
- Objetivo principal de cada uma dentro do produto
- Frustrações atuais que o produto resolve

**`prd/metrics.md`** com:
- Métricas de adoção
- Métricas de qualidade
- Critérios de sucesso por funcionalidade

Escreva em português. Sem código, sem decisões técnicas.
