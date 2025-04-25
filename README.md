# Simple Ensi OpenAPI Generator (seog)
A simple command-line tool for generating and translating OpenAPI specifications for Ensi based on reusable templates.

## Requirements
- `Python 3.12+`
- `PyYAML`
- `googletrans==4.0.0-rc1` (for `translate-entity` command)
- `Poetry`

## Installation

```bash
git clone https://github.com/C0rTeZ13/simple-ensi-openapi-generator
cd simple-ensi-openapi-generator
poetry install
chmod +x seog
```

## Installation (with .venv)
```bash
git clone https://github.com/C0rTeZ13/simple-ensi-openapi-generator
cd simple-ensi-openapi-generator
python3 -m venv .venv
poetry config virtualenvs.in-project true
poetry install
source .venv/bin/activate
chmod +x seog
```

### ℹ️ If you want to use `seog` from anywhere, create a symlink
```
sudo ln -s /full/path/to/seog.sh /usr/local/bin/seog
```

## Usage
```
seog <command> [options]
```

### Available commands:
- generate-paths
- generate-entity
- translate-entity

## 1. generate-paths
Generate API paths specification from a template.

```
seog generate-paths OUTPUT_PATH -e ENTITY [-t TEMPLATE] [-a]
```

`OUTPUT_PATH` – path to write (or append) generated paths.

`-e, --entity` – entity name (e.g., Customer).

`-t, --template` – path to template file (default: ./examples/example-paths.yaml).

`-a, --append` – append to existing file instead of overwriting.


## 2. generate-entity
Generate entity schema specification from a template and CSV.

```
seog generate-entity OUTPUT_PATH --csv CSV_PATH -e ENTITY [-t TEMPLATE] [-a]
```

`OUTPUT_PATH` – path to write (or append) generated schema.

`--csv` – path to CSV file with field definitions.

`-e, --entity` – entity name (e.g., Customer).

`-t, --template` – path to template file (default: ./examples/example-entity.yaml).

`-a, --append` – append to existing file instead of overwriting.

## 3. translate-entity
Translate all `description` and `example` values in a YAML file from Russian to English.

```
seog translate-entity FILE_PATH
```

`FILE_PATH` – path to the YAML file to translate in place.

### ⚠️ Warning: Machine translation may be highly inaccurate. Always review and correct translated descriptions and examples manually.

## Project Structure
```
├── app
│   ├── __init__.py
│   ├── generate_paths.py
│   ├── generate_entity.py
│   └── translate_entity_to_en.py
├── examples
│   ├── example-paths.yaml
│   └── example-entity.yaml
├── seog
│   ├── __init__.py
│   └── cli.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## License
This project is licensed under the MIT License.
