import yaml
import csv

def _map_type(csv_type: str) -> (str, str):
    t = csv_type.strip().lower()
    if t in ('int', 'integer'):
        return 'integer', None
    if t in ('string', 'varchar', 'text'):
        return 'string', None
    if t in ('boolean', 'bool'):
        return 'boolean', None
    if t in ('datetime', 'date-time', 'timestamp'):
        return 'string', 'date-time'
    return t, None

def _replace_refs(obj: any, entity_name: str):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == '$ref' and isinstance(v, str) and v.startswith('#/'):
                ref_name = v[2:]
                new_ref = ref_name.replace('Template', entity_name)
                obj[k] = f"#/{new_ref}"
            else:
                _replace_refs(v, entity_name)
    elif isinstance(obj, list):
        for item in obj:
            _replace_refs(item, entity_name)

def generate_entity_from_template(
    template_path: str,
    output_path: str,
    csv_path: str,
    entity_name: str,
    append: bool = False
) -> None:
    with open(template_path, 'r', encoding='utf-8') as f:
        original = yaml.safe_load(f) or {}

    csv_properties = {}
    csv_required = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    for row in rows[1:]:
        name = row[0].strip()
        yaml_type, yaml_format = _map_type(row[1])
        field_schema = {'type': yaml_type}
        if yaml_format:
            field_schema['format'] = yaml_format
        desc = row[3].strip() if len(row) > 3 else ''
        if desc:
            field_schema['description'] = desc
        csv_properties[name] = field_schema
        nullable = row[2].strip().lower() if len(row) > 2 else ''
        if nullable in ('нет', 'no', 'false', '0'):
            csv_required.append(name)

    renamed = {}
    for old_key, section in original.items():
        new_key = old_key.replace('Template', entity_name)
        renamed[new_key] = section

    fill_key = f"{entity_name}FillableProperties"
    renamed[fill_key] = {
        'type': 'object',
        'properties': csv_properties
    }
    req_key = f"{entity_name}FillableRequiredProperties"
    renamed[req_key] = {'required': csv_required}

    for section in renamed.values():
        _replace_refs(section, entity_name)

    mode = 'a' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for key, section in renamed.items():
            yaml.dump({key: section}, f, allow_unicode=True, sort_keys=False)
            f.write('\n')
