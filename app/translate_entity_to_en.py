import re
from googletrans import Translator

def translate_entity(file_path: str) -> None:
    translator = Translator()
    pattern = re.compile(r'^(\s*)(description|example):\s*(["\']?)(.*?)(\3)\s*$')

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        m = pattern.match(line.rstrip('\n'))
        if m:
            indent, key, quote, text, _ = m.groups()
            try:
                translated = translator.translate(text, src='ru', dest='en').text
            except Exception:
                translated = text
            new_line = f"{indent}{key}: {quote}{translated}{quote}\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
