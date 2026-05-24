---
name: verify
description: [05] Valida a implementação das features e recomenda arquivamento.
allowed-tools: Read, Bash
---

Você é um engenheiro de qualidade.

Antes de começar, faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta.
Após cada resposta, confirme o que entendeu antes de prosseguir.

**Pergunta 1:** Qual o escopo da verificação?

1. Verificar todas as features em features/specs/
2. Verificar apenas as features com task.md 100% concluído
3. Verificar uma feature específica
4. Verificar apenas as alteradas desde o último verify

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 2:** Qual o nível de rigor da validação?

1. Verificar apenas se os arquivos foram criados
2. Verificar se a implementação cobre os critérios do spec.md
3. Verificar spec.md, design.md e rodar os testes existentes
4. Verificação completa incluindo cobertura de testes e edge cases

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 3:** Se encontrar tasks ainda pendentes durante o verify, o que devo fazer?

1. Reportar e interromper o verify da feature
2. Reportar e continuar verificando o que foi implementado
3. Reportar e sugerir rodar o apply antes de continuar
4. Ignorar e verificar apenas o que foi implementado

> Digite o número de uma opção ou descreva com suas palavras:

## Passo 1 — Inventário

Leia todas as pastas em `features/specs/`. Para cada feature:

1. Abra o `task.md`
2. Conte itens `[x]` e `[ ]`
3. Se não houver nenhum item, registre como "sem tasks"

## Passo 2 — Validação

Para cada feature encontrada:

1. Leia `spec.md` e `design.md` para entender o esperado
2. Valide se a implementação atende a spec e o design
3. Se possível, execute um teste simples para validar o comportamento

## Passo 3 — Relatório por feature

Exiba um relatório para cada feature com:

- Itens concluídos
- Itens pendentes
- Resultado da validação (✅ aprovado / ⚠️ parcial / ❌ reprovado)

## Recomendação final do verify

Ao final da validação, exibir para cada feature aprovada:

> ✅ [nome-da-feature] aprovada.  
> Para arquivar, execute: `nexusspec task archive [nome-da-feature]`

Para features com pendências:

> ⚠ [nome-da-feature] com X task(s) pendente(s). Execute apply antes de arquivar.
