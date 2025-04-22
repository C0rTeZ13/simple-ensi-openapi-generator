import re
from pathlib import Path


def to_snake_case(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def generate_paths_from_template(template_path, output_path, entity, append_mode=False):
    entity_lower = entity.lower()
    entity_camel = entity[0].lower() + entity[1:]
    snake_name = to_snake_case(entity) + 's'

    replacements = {
        # Schema file paths
        r'schemas/templates\.yaml': f'schemas/{snake_name}.yaml',
        r'/#/Template':            f"/#/{entity}",

        # Tags and special keywords
        r'tags:\s*\n\s*-\s*templates': f"tags:\n      - {snake_name}",
        r'objects? of Template':       f"objects of {entity}",

        # Core entity replacements
        r'\bTemplate\b':  entity,
        r'\bTemplates\b': f"{entity}s",
        r'\btemplate\b':  entity_lower,
        r'\btemplates\b': f"{entity_lower}s",

        # Operations and controllers
        r'SearchTemplates':       f"Search{entity}s",
        r'SearchTemplate':        f"Search{entity}",
        r'searchTemplates':       f"search{entity}s",
        r'searchTemplate':        f"search{entity}",
        r'CreateTemplate':        f"Create{entity}",
        r'createTemplate':        f"create{entity_camel}",
        r'GetTemplate':           f"Get{entity}",
        r'getTemplate':           f"get{entity_camel}",
        r'ReplaceTemplate':       f"Replace{entity}",
        r'replaceTemplate':       f"replace{entity_camel}",
        r'PatchTemplate':         f"Patch{entity}",
        r'patchTemplate':         f"patch{entity_camel}",
        r'DeleteTemplate':        f"Delete{entity}",
        r'deleteTemplate':        f"delete{entity_camel}",
        r'TemplatesSearch':       f"{entity}sSearch",
        r'TemplatesSearchOne':    f"{entity}sSearchOne",
        r'TemplatesOne':          f"{entity}sOne",
        r'TemplatesMassDelete':   f"{entity}sMassDelete",
        r'TemplatesController':   f"{entity}sController",

        # Requests and responses
        r'SearchTemplatesRequest':     f"Search{entity}sRequest",
        r'SearchTemplateRequest':      f"Search{entity}Request",
        r'SearchOneTemplateRequest':   f"SearchOne{entity}Request",
        r'CreateTemplateRequest':      f"Create{entity}Request",
        r'ReplaceTemplateRequest':     f"Replace{entity}Request",
        r'PatchTemplateRequest':       f"Patch{entity}Request",
        r'TemplateResponse':           f"{entity}Response",
        r'TemplatesResponse':          f"{entity}sResponse",
    }

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    op_pattern = re.compile(
        r'^(\s*operationId:\s*)(["\']?)([^"\']+)(["\']?)',
        flags=re.MULTILINE
    )
    def _lower_first(m):
        prefix, q1, val, q2 = m.groups()
        return f"{prefix}{q1}{val[0].lower()}{val[1:]}{q2}"
    content = op_pattern.sub(_lower_first, content)

    mode = 'a' if append_mode and Path(output_path).exists() else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        if mode == 'a' and f.tell() > 0:
            f.write('\n')
        f.write(content)
