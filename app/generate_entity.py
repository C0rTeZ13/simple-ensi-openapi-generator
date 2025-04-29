import yaml
import csv
import re

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

    readonly = {'id', 'created_at', 'updated_at'}
    csv_properties = {}
    csv_required = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    for row in rows[1:]:
        name = row[0].strip()
        if name in readonly:
            continue
        yaml_type, yaml_format = _map_type(row[1])
        field = {'type': yaml_type}
        if yaml_format:
            field['format'] = yaml_format

        if len(row) > 3:
            desc = row[3].strip()
            if desc:
                field['description'] = desc

        flag = row[2].strip().lower() if len(row) > 2 else ''
        if flag in ('нет', 'no', 'false', '0'):
            field['nullable'] = True
        else:
            csv_required.append(name)

        csv_properties[name] = field

    renamed = {}
    for old_key, section in original.items():
        new_key = old_key.replace('Template', entity_name)
        renamed[new_key] = section

    renamed[f"{entity_name}FillableProperties"] = {
        'type': 'object',
        'properties': csv_properties
    }
    renamed[f"{entity_name}FillableRequiredProperties"] = {
        'required': csv_required
    }

    for section in renamed.values():
        _replace_refs(section, entity_name)

    ref_line_re = re.compile(r'^(\s*\$ref:\s*)(.*)$')

    mode = 'a' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for key, section in renamed.items():
            dumped = yaml.dump({key: section}, allow_unicode=True, sort_keys=False)
            for line in dumped.splitlines(keepends=True):
                m = ref_line_re.match(line)
                if m:
                    prefix, rhs = m.groups()
                    val = rhs.strip().strip('\'"')
                    f.write(f"{prefix}'{val}'\n")
                else:
                    f.write(line)
            f.write('\n')
