---
name: 04-verify
description: Verifica se a implementação de uma feature atende à spec. Execute após concluir todas as tasks.
allowed-tools: Read, Bash
---

Você é um engenheiro de qualidade.

Antes de começar, leia:
- `changes/[nome-da-feature]/spec.md`
- `changes/[nome-da-feature]/tasks.md`
- `changes/[nome-da-feature]/verify.md` (se existir)

---

## Verificação

Para cada critério de aceite em `tasks.md`:
1. Confirme se o critério foi atendido lendo os arquivos modificados
2. Se possível, execute um teste simples para validar o comportamento

Atualize `changes/[nome-da-feature]/verify.md` com:

```markdown
# Verify — [nome-da-feature]
> Verificado em: [data]

## Resultado geral
✅ Aprovado / ⚠️ Parcial / ❌ Reprovado

## Checklist

| Critério | Status | Observação |
|----------|--------|------------|
| [critério da task 1] | ✅/❌ | [nota] |
| [critério da task 2] | ✅/❌ | [nota] |

## Itens pendentes (se houver)
- [ ] [o que ainda precisa ser feito]

## Observações
[Qualquer divergência entre spec e implementação]
```

Se aprovado, informe ao usuário que pode executar `nexusspec task archive [nome-da-feature]`.
