# Engenharia de ia

Prompt → PRD Geral
Prompt → PRD Tarefa
Prompt → TechSpec
Prompt → Plano
Skill  → Clean Code (durante implementação)
Rules  → copilot-instructions.md (sempre ativo)
MCP    → context7


# Passos para criação:

Mude para modo Agent

## 1- Crie o PRD Geral

Referencie o arquivo prompts/pdr_geral.md
```bash
#pdr_geral.md
```

## 2- Crie o PRD da tarefa

Referencie o arquivo prompts/pdr_tarefa.md
```bash
#pdr_tarefa.md
```


## 3- Crie o techspec da tarefa

Referencie o arquivo prompts/techspec_tarefa.md
```bash
#techspec_tarefa.md
```

***MCP(avançado):***
obs.: caberia aqui usar o mcp do conetxt7 como documentação
https://context7.com/ 
https://github.com/upstash/context7
***----***

## 4- Crie o plano da tarefa

Mude para modo Plan
Referencie os arquivos da pasta da tarefa
```bash
crie um plano para a tarefa001 e leia os arquivos #PRD_TAREFA_001.md #TECHSPEC_TAREFA_001.md 
```

Salve o plano na pasta desejada

Mude para modo Agent
```bash
salve o plano na pasta #tarefa-001 
```

## 5- Implementação

modo Agent
```bash
Impemente o plano salvando os arquivos na raiz do projeto
```


***rules:***
## 6- Vamos criar as rules:

No VS Code com GitHub Copilot, as rules ficam em um arquivo `.github/copilot-instructions.md` na raiz do projeto. Ele é lido automaticamente pelo Copilot em todo o workspace.

A estrutura do projeto ficaria assim:

```
.github/
└── copilot-instructions.md   ← rules globais do projeto
docs/
└── tarefas/
    └── tarefa-001/
prompts/
└── prd_geral.md
```

Um exemplo de `copilot-instructions.md` para o seu contexto:

```markdown
# Instruções do projeto

## Estrutura de documentação
- PRD Geral: `docs/PRD_GERAL.md`
- PRD por tarefa: `docs/tarefas/tarefa-00X/PRD_TAREFA_00X.md`
- TechSpec por tarefa: `docs/tarefas/tarefa-00X/TECHSPEC_TAREFA_00X.md`
- Plano por tarefa: `docs/tarefas/tarefa-00X/PLANO_TAREFA_00X.md`

## Comportamento esperado
- Sempre leia o PRD_GERAL.md para entender o contexto do produto
- Sempre leia os arquivos da pasta da tarefa antes de sugerir código
- Nunca implemente algo que não esteja descrito na TechSpec da tarefa
- Siga a ordem de implementação definida no plano da tarefa

## Padrões do projeto
- Idioma: português para documentação, inglês para código
- Commits devem referenciar o número da tarefa (ex: `feat: tarefa-001 - cadastro de usuário`)
```

## 6- Adicioando rules para design:

No mesmo `.github/copilot-instructions.md`, numa seção de **Frontend**:

```markdown
# Instruções do projeto

## Estrutura de documentação
- PRD Geral: `docs/PRD_GERAL.md`
- PRD por tarefa: `docs/tarefas/tarefa-00X/PRD_TAREFA_00X.md`
- TechSpec por tarefa: `docs/tarefas/tarefa-00X/TECHSPEC_TAREFA_00X.md`
- Plano por tarefa: `docs/tarefas/tarefa-00X/PLANO_TAREFA_00X.md`

## Comportamento esperado
- Sempre leia o PRD_GERAL.md para entender o contexto do produto
- Sempre leia os arquivos da pasta da tarefa antes de sugerir código
- Nunca implemente algo que não esteja descrito na TechSpec da tarefa
- Siga a ordem de implementação definida no plano da tarefa

## Padrões do projeto
- Idioma: português para documentação, inglês para código
- Commits devem referenciar o número da tarefa (ex: `feat: tarefa-001 - cadastro de usuário`)

## Frontend
- Framework de CSS: Bootstrap 5
- Sempre use classes do Bootstrap — nunca escreva CSS customizado para layout
- Componentes preferidos: `card`, `form-control`, `btn`, `alert`, `modal`
- Breakpoints: mobile-first, usar `col-12 col-md-6 col-lg-4` como padrão de grid
- Ícones: Bootstrap Icons (`bi bi-`)
- Cores: usar apenas as variáveis do Bootstrap (ex: `text-primary`, `bg-danger`)
- Nunca use `style=""` inline — prefira classes utilitárias do Bootstrap
```

---

Se o projeto crescer, você pode também separar em um arquivo dedicado:

```
.github/
├── copilot-instructions.md   ← regras gerais
└── instructions/
    ├── frontend.md           ← Bootstrap, componentes, padrões visuais
    ├── backend.md            ← padrões de API, banco, autenticação
    └── documentacao.md       ← estrutura de pastas e prompts
```

***Skills manualmente:***

Como criar uma skill no GitHub Copilot de forma mnual

## Onde colocar

── prompts/
│   ├── skills/
│   │   └── clean-code.md        ← skill aqui

Crie o arquivo clean-code.md dentro de prompts/skills/
Cole o conteúdo abaixo no arquivo clean-code.md
Cada skill é um arquivo `.md` separado.


Conteudo:

Início: ->

---
name: clean-code
description: Aplica princípios básicos de clean code durante a implementação de tarefas. Use sempre que estiver escrevendo ou revisando código no projeto.
allowed-tools: Read, Write, Edit
---

## Use este skill quando
- Estiver implementando qualquer tarefa do projeto
- Quiser revisar código já escrito antes de commitar
- O agente sugerir código que parece complexo demais

## Não use este skill quando
- A tarefa for apenas de documentação
- Estiver apenas lendo arquivos

---

## Princípios fundamentais

| Princípio | Regra |
|-----------|-------|
| **SRP** | Cada função faz uma coisa só |
| **DRY** | Não repita código — extraia e reutilize |
| **KISS** | A solução mais simples que funciona |
| **YAGNI** | Não construa o que não foi pedido na tarefa |

---

## Nomenclatura

| Elemento | Padrão |
|----------|--------|
| Variáveis | Revelam intenção: `userEmail` não `e` |
| Funções | Verbo + substantivo: `saveUser()` não `user()` |
| Booleanos | Forma de pergunta: `isValid`, `hasError`, `canSubmit` |
| Constantes | MAIÚSCULO_COM_UNDERSCORE: `MAX_ATTEMPTS` |

> Se precisar de comentário para explicar o nome, renomeie.

---

## Funções

- Máximo 20 linhas
- Máximo 3 argumentos
- Sem efeitos colaterais inesperados
- Use retorno antecipado para casos de erro (guard clauses)

```js
// ❌ Evite
function process(data) {
  if (data) {
    if (data.user) {
      if (data.user.email) {
        // lógica aqui
      }
    }
  }
}

// ✅ Prefira
function process(data) {
  if (!data?.user?.email) return
  // lógica aqui
}
```

---

## Anti-padrões — não faça

| ❌ Evite | ✅ Faça |
|---------|--------|
| Comentar cada linha | Deixe o código se explicar |
| Funções com 100+ linhas | Divida por responsabilidade |
| Nomes abreviados (`usr`, `fn`) | Nomes completos e claros |
| Números mágicos (`if x > 7`) | Constantes nomeadas (`MAX_DAYS`) |
| Aninhamento profundo | Guard clauses e retorno antecipado |
| Criar arquivo só para uma função | Coloque onde será usado |

---

## Antes de editar qualquer arquivo

Pergunte-se:
- Quem importa este arquivo? Precisa ser atualizado também?
- Esta é uma função compartilhada? Onde mais é usada?
- Minha mudança quebra alguma interface existente?

> Edite o arquivo e todos os dependentes na mesma tarefa. Nunca deixe imports quebrados.

---

## Checklist antes de concluir a tarefa

| | Verificação |
|-|-------------|
| ☐ | O código faz exatamente o que a tarefa pede? |
| ☐ | Todas as funções têm menos de 20 linhas? |
| ☐ | Os nomes estão claros sem precisar de comentário? |
| ☐ | Não há código duplicado? |
| ☐ | Não há nada implementado além do que foi pedido? |

> Se qualquer item falhar, corrija antes de concluir.

<- Fim 

o Copilot não ativa automaticamente skills neste formato
Você precisaria referenciar explicitamente no chat:

@workspace /prompts/skills/clean-code.md revise este código



## Skill (avançado)

Skills ficam em `.github/instructions/` e são ativadas automaticamente pelo Copilot
com base na descrição de cada arquivo.

**Passo a passo:**

1. Crie a pasta `.github` na raiz do projeto
2. Crie o arquivo `copilot-instructions.md` dentro de `.github`
3. Crie a pasta `instructions` dentro de `.github`
4. Cole os arquivos de skill dentro de `instructions`

```
.github/
├── copilot-instructions.md   ← regras globais sempre ativas
└── instructions/
    └── clean-code.md         ← skill ativada automaticamente
```

---

E o `copilot-instructions.md` para o seu projeto:

````markdown
# Instruções do projeto

## Estrutura de documentação
- PRD Geral: `docs/PRD_GERAL.md`
- PRD por tarefa: `docs/tarefas/tarefa-00X/PRD_TAREFA_00X.md`
- TechSpec por tarefa: `docs/tarefas/tarefa-00X/TECHSPEC_TAREFA_00X.md`
- Plano por tarefa: `docs/tarefas/tarefa-00X/PLANO_TAREFA_00X.md`

## Comportamento esperado
- Sempre leia o `PRD_GERAL.md` para entender o contexto do produto
- Sempre leia todos os arquivos da pasta da tarefa antes de sugerir código
- Nunca implemente algo que não esteja descrito na TechSpec da tarefa
- Siga a ordem de implementação definida no plano da tarefa

## Padrões do projeto
- Idioma: português para documentação, inglês para código
- Commits devem referenciar o número da tarefa (ex: `feat: tarefa-001 - cadastro de usuário`)

## Frontend
- Framework de CSS: Bootstrap 5
- Sempre use classes do Bootstrap — nunca escreva CSS customizado para layout
- Componentes preferidos: `card`, `form-control`, `btn`, `alert`, `modal`
- Ícones: Bootstrap Icons (`bi bi-`)
- Cores: usar apenas variáveis do Bootstrap (`text-primary`, `bg-danger`)
- Nunca use `style=""` inline — prefira classes utilitárias do Bootstrap

## Skills ativas
As seguintes skills estão configuradas e devem ser aplicadas automaticamente:

- `.github/instructions/clean-code.md` — padrões de código limpo aplicados em toda implementação

````