Você é um engenheiro sênior. Vou te passar informações sobre uma tarefa para criar a TechSpec.

Leia o contexto em:
- @docs/PRD_GERAL.md
- @docs/tarefas/tarefa-00X/PRD_TAREFA_00X.md

Faça as perguntas **uma de cada vez**, oferecendo sugestões em cada uma.
Aguarde minha resposta antes de continuar.

Comece agora com a pergunta 1.

---

**Pergunta 1:** Onde esta funcionalidade será implementada?

> Sugestões baseadas no projeto:
> - A) Nova tela/página independente (Frontend)
> - B) Componente dentro de uma tela existente (Frontend)
> - C) Serviço de backend (API/endpoint)
> - D) Frontend + Backend juntos
> - E) Outro — descreva

---

### 🔹 BLOCO FRONTEND (perguntar apenas se resposta da Pergunta 1 for A, B ou D)

**Pergunta 2:** Qual linguagem será utilizada no frontend?

> Sugestões:
> - A) JavaScript
> - B) TypeScript
> - C) Outro — descreva

---

**Pergunta 3:** Qual framework ou biblioteca será utilizada no frontend?

> Sugestões:
> - A) React
> - B) Vue
> - C) Angular
> - D) Nenhum (vanilla)
> - E) Outro — descreva

---

### 🔹 BLOCO BACKEND (perguntar apenas se resposta da Pergunta 1 for C ou D)

**Pergunta 4:** Qual linguagem será utilizada no backend?

> Sugestões:
> - A) JavaScript (Node.js)
> - B) TypeScript
> - C) Java
> - D) Python
> - E) Outro — descreva

---

**Pergunta 5:** Qual framework será utilizado no backend?

> Sugestões:
> - A) Express
> - B) NestJS
> - C) Spring Boot
> - D) Laravel
> - E) Outro — descreva

---

**Pergunta 6:** Qual banco de dados será utilizado?

> Sugestões:
> - A) MySQL
> - B) PostgreSQL
> - C) MongoDB
> - D) SQLite
> - E) Firebase
> - F) Nenhum
> - G) Outro — descreva

---

**Pergunta 7:** Como os dados desta tarefa serão armazenados?

> Sugestões:
> - A) Banco de dados (tabela nova)
> - B) Banco de dados (tabela existente)
> - C) Armazenamento local do navegador
> - D) Sem persistência — apenas em memória
> - E) Outro — descreva

---

**Pergunta 8:** Esta tarefa envolve comunicação entre partes distintas do sistema?
(ex: frontend chamando backend, sistema chamando API externa)

> Sugestões:
> - A) Sim — frontend chama API interna do projeto
> - B) Sim — sistema integra com API externa (ex: autenticação, pagamento, e-mail)
> - C) Não — tudo acontece dentro de uma única parte do sistema
> - D) Ainda não sei — me ajude a decidir

> ⚠️ Se responder A ou B, farei perguntas adicionais sobre o contrato da interface.

---

**[Condicional — perguntar apenas se resposta da pergunta 8 for A ou B]**

**Pergunta 8a:** Qual é a operação principal desta interface?

> Sugestões:
> - A) Criar um novo registro (POST)
> - B) Buscar dados (GET)
> - C) Atualizar um registro (PUT/PATCH)
> - D) Remover um registro (DELETE)
> - E) Mais de uma operação — descreva

---

**[Condicional — perguntar apenas se resposta da pergunta 8 for A ou B]**

**Pergunta 8b:** O que deve ser retornado em caso de erro?

> Sugestões:
> - A) Mensagem de erro genérica (ex: "Algo deu errado")
> - B) Mensagem específica por tipo de erro (ex: "E-mail já cadastrado")
> - C) Código de erro para o frontend tratar e exibir a mensagem
> - D) Outro — descreva

---

**Pergunta 9:** Quais são os maiores riscos técnicos desta implementação?

> Sugestões:
> - A) Conflito com código existente
> - B) Performance com grande volume de dados
> - C) Segurança (ex: autenticação, permissões, dados sensíveis)
> - D) Sem riscos relevantes para esta tarefa
> - E) Outro — descreva

---

**Pergunta 10:** Como esta tarefa será testada?

> Sugestões:
> - A) Testes unitários nos componentes principais
> - B) Testes de integração entre frontend e backend
> - C) Testes manuais pelo time de QA
> - D) Combinação das anteriores
> - E) Outro — descreva

---

Com base nas respostas e no PRD da tarefa, gere a TechSpec com estas seções:

1. **Resumo técnico** — abordagem escolhida e principal trade-off

2. **Componentes** — o que será criado ou modificado e a responsabilidade de cada parte

3. **Modelo de dados** — campos, tipos e relacionamentos envolvidos

4. **Contrato de interface** — incluir SOMENTE se a pergunta 8 foi respondida com A ou B:
   - Endpoint: método + caminho (ex: `POST /api/usuarios`)
   - Request: campos, tipos e obrigatoriedade
   - Response de sucesso: estrutura e status code
   - Response de erro: estrutura, status codes e mensagens esperadas

5. **Ordem de implementação** — passo a passo numerado, cada etapa indicando do que depende

6. **Testes** — o que testar, como e onde

7. **Riscos e mitigações** — riscos identificados e como lidar com cada um

8. **Diagrama** — escolha o tipo mais adequado para esta tarefa:
   - Use **diagrama de atividade** se a tarefa envolve um fluxo de ações do usuário
   - Use **diagrama de estado** se a tarefa envolve mudança de estados
   - Gere em Mermaid

   Para diagrama de atividade:
```mermaid
flowchart TD
  A([Início]) --> B[Ação do usuário]
  B --> C{Validação}
  C -->|válido| D[Salvar dados]
  C -->|inválido| E[Exibir erro]
  D --> F([Fim])