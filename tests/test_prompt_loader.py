import yaml

from nexusspec.integrations.skills.providers.shared.frontmatter import (
    merge_frontmatter,
    render_frontmatter,
    split_frontmatter,
)
from nexusspec.integrations.skills.providers.shared.prompt_loader import (
    load_prompt_templates,
    read_template_metadata,
)

from conftest import SKILL_STEMS


def test_carrega_templates_do_pacote_ignorando_legacy(tmp_path):
    templates = load_prompt_templates(project_dir=tmp_path)

    assert {t.stem for t in templates} == SKILL_STEMS
    assert not any(t.name.startswith("_") for t in templates)
    assert [t.name for t in templates] == sorted(t.name for t in templates)


def test_templates_do_pacote_tem_name_e_description(tmp_path):
    for template in load_prompt_templates(project_dir=tmp_path):
        assert template.skill_name == template.stem
        assert template.description


def test_override_da_pasta_prompts(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "prd.md").write_text(
        "---\nname: prd\ndescription: PRD customizado\n---\n\nCorpo próprio\n",
        encoding="utf-8",
    )
    (prompts_dir / "extra.md").write_text("Sem frontmatter\n", encoding="utf-8")
    (prompts_dir / "ignorado.txt").write_text("x", encoding="utf-8")

    templates = load_prompt_templates(project_dir=tmp_path)

    assert [t.stem for t in templates] == ["extra", "prd"]
    prd = templates[1]
    assert prd.source_path == prompts_dir / "prd.md"
    assert prd.description == "PRD customizado"
    assert "Corpo próprio" in prd.content
    assert templates[0].skill_name is None
    assert templates[0].description is None


def test_read_template_metadata():
    content = '---\nname: x\ndescription: "[01] com: dois pontos"\n---\ncorpo'
    assert read_template_metadata(content) == ("x", "[01] com: dois pontos")
    assert read_template_metadata("sem frontmatter") == (None, None)


def test_merge_frontmatter_nao_duplica_e_preserva_chaves():
    content = "---\nname: prd\ndescription: original\nallowed-tools: Read, Write\n---\n\nCorpo\n"

    merged = merge_frontmatter(content, {"description": "nova", "globs": ["**/*"]}, body_prefix="# T\n\n")

    assert merged.count("---\n") == 2
    fields, body = split_frontmatter(merged)
    assert fields == {
        "description": "nova",
        "globs": ["**/*"],
        "name": "prd",
        "allowed-tools": "Read, Write",
    }
    assert body == "# T\n\nCorpo\n"


def test_render_frontmatter_gera_yaml_valido():
    fields = {
        "name": "prd",
        "description": "[01] Gera: algo # com símbolos",
        "allowed-tools": "Read, Write",
        "globs": ["**/*"],
        "alwaysApply": "false",
    }

    parsed = yaml.safe_load(render_frontmatter(fields).strip("-\n"))

    assert parsed == {**fields, "alwaysApply": False}
