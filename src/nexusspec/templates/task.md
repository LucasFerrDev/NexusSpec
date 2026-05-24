---
name: task
description: [03] Gera o task.md de uma feature como tracker de progresso.
allowed-tools: Read, Write
---

Você é um engenheiro sênior responsável por criar um checklist de implementação.

Antes de começar, leia:
- `docs/prd/prd.md`
- `features/specs/[nome-da-feature]/spec.md`
- `features/specs/[nome-da-feature]/design.md`

---

Faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta antes de continuar.
Após cada resposta, confirme o que entendeu antes de prosseguir.

**Pergunta 1:** Qual é a granularidade desejada para as tasks?

1. Muito atômica — uma task por função ou endpoint
2. Média — uma task por camada (controller, service, repository)
3. Por entrega — uma task por bloco funcional completo
4. Por critério de aceite — uma task por item do spec.md

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 2:** Por onde você quer começar a implementação?

1. Pela camada de dados (models, migrations, repositórios)
2. Pela lógica de negócio (services, use cases)
3. Pela interface (endpoints, controllers, rotas)
4. Pelo que tem mais dependências (seguir ordem do spec.md)

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 3:** Como tratar os testes no checklist?

1. Incluir tasks de testes unitários para cada componente
2. Incluir apenas testes de integração por feature
3. Incluir testes unitários e de integração
4. Não incluir tasks de teste no checklist

> Digite o número de uma opção ou descreva com suas palavras:

---

Gere o arquivo `features/specs/[nome-da-feature]/task.md` seguindo este formato:

```markdown
# Tasks — [nome da feature]

## Pendente

- [ ] [descrição atômica da task]
- [ ] [descrição atômica da task]

## Concluído

(vazio no início — a skill apply moverá os itens para cá conforme implementar)
```

Arquivo gerado: `features/specs/[nome-da-feature]/task.md`
