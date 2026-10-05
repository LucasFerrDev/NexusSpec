"""Leitura, escrita e mescla do frontmatter YAML dos templates.

Suporta o subconjunto de YAML usado nos templates: pares ``chave: valor``
(com ou sem aspas) e listas simples (``- item``). Assim evitamos uma
dependência de parser YAML só para o cabeçalho.
"""

import json
import re

FrontmatterValue = str | list[str]

_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$")
_PLAIN_SCALAR_RE = re.compile(r"^[A-Za-z0-9_./(][^\n]*$")


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def _quote(value: str) -> str:
    """Mantém o valor sem aspas quando é seguro em YAML; senão usa aspas duplas."""
    is_plain = (
        _PLAIN_SCALAR_RE.match(value)
        and ": " not in value
        and " #" not in value
        and not value.endswith(":")
        and value == value.strip()
    )
    if is_plain:
        return value
    return json.dumps(value, ensure_ascii=False)


def split_frontmatter(content: str) -> tuple[dict[str, FrontmatterValue], str]:
    """Separa o frontmatter do corpo. Retorna ({}, content) se não houver frontmatter."""
    match = _FRONTMATTER_RE.match(content)
    if not match:
        return {}, content

    fields: dict[str, FrontmatterValue] = {}
    current_key: str | None = None
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key_match = _KEY_RE.match(line)
        if key_match and not line[0].isspace():
            current_key = key_match.group(1)
            fields[current_key] = _unquote(key_match.group(2).strip())
        elif current_key and stripped.startswith("- "):
            existing = fields[current_key]
            items = existing if isinstance(existing, list) else []
            items.append(_unquote(stripped[2:].strip()))
            fields[current_key] = items

    body = content[match.end():].lstrip("\r\n")
    return fields, body


def render_frontmatter(fields: dict[str, FrontmatterValue]) -> str:
    """Serializa os campos como bloco de frontmatter (``---`` ... ``---``)."""
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {_quote(item)}" for item in value)
        else:
            lines.append(f"{key}: {_quote(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def merge_frontmatter(content: str, fields: dict[str, FrontmatterValue]) -> str:
    """Gera um único frontmatter: ``fields`` primeiro (com precedência), depois as
    demais chaves já presentes no template, seguido do corpo do template."""
    existing, body = split_frontmatter(content)
    merged = dict(fields)
    for key, value in existing.items():
        merged.setdefault(key, value)
    return f"{render_frontmatter(merged)}\n{body}"
