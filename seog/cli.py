import argparse
from pathlib import Path
import sys

from app.generate_paths import generate_paths_from_template
from app.generate_entity import generate_entity_from_template
from app.translate_entity_to_en import translate_entity

def main():
    parser = argparse.ArgumentParser(
        prog='seog',
        description='Simple Ensi OpenAPI Generator: a tool for working with Ensi API specifications'
    )

    subparsers = parser.add_subparsers(
        title='Commands',
        dest='command',
        required=True,
        help='Choose an action'
    )

    # generate-paths command
    gen_paths = subparsers.add_parser(
        'generate-paths',
        help='Generate API paths specification from template'
    )
    gen_paths.add_argument(
        'output',
        help='Output file path'
    )
    gen_paths.add_argument(
        '-e', '--entity',
        required=True,
        help='Entity name (e.g., Customer)'
    )
    gen_paths.add_argument(
        '-t', '--template',
        default='./examples/example-paths.yaml',
        help='Template file path (default: ./examples/example-paths.yaml)'
    )
    gen_paths.add_argument(
        '-a', '--append',
        action='store_true',
        help='Append to existing file instead of overwriting'
    )

    # generate-entity command
    gen_entity = subparsers.add_parser(
        'generate-entity',
        help='Generate entity specification from template'
    )
    gen_entity.add_argument(
        'output',
        help='Output file path'
    )
    gen_entity.add_argument(
        '--csv',
        required=True,
        help='Path to CSV file with field definitions'
    )
    gen_entity.add_argument(
        '-e', '--entity',
        required=True,
        help='Entity name (e.g., Customer)'
    )
    gen_entity.add_argument(
        '-t', '--template',
        default='./examples/example-entity.yaml',
        help='Template file path (default: ./examples/example-entity.yaml)'
    )
    gen_entity.add_argument(
        '-a', '--append',
        action='store_true',
        help='Append to existing file instead of overwriting'
    )

    # translate-entity command
    translate_cmd = subparsers.add_parser(
        'translate-entity',
        help='Translate all description and example fields in a YAML file from RU to EN'
    )
    translate_cmd.add_argument(
        'file',
        help='Path to the YAML file to translate'
    )

    args = parser.parse_args()

    try:
        if args.command == 'generate-paths':
            if not Path(args.template).exists():
                print(f"❌  Template file not found: {args.template}")
                sys.exit(1)

            generate_paths_from_template(
                args.template,
                args.output,
                args.entity,
                args.append
            )
            action = 'Appended' if args.append else 'Created'
            print(f"✅  {action} API paths for '{args.entity}' into {args.output}")

        elif args.command == 'generate-entity':
            if not Path(args.template).exists():
                print(f"❌  Template file not found: {args.template}")
                sys.exit(1)
            if not Path(args.csv).exists():
                print(f"❌  CSV file not found: {args.csv}")
                sys.exit(1)

            generate_entity_from_template(
                args.template,
                args.output,
                args.csv,
                args.entity,
                args.append
            )
            action = 'Appended' if args.append else 'Created'
            print(f"✅  {action} entity specification for '{args.entity}' into {args.output}")

        elif args.command == 'translate-entity':
            if not Path(args.file).exists():
                print(f"❌  File not found: {args.file}")
                sys.exit(1)

            translate_entity(args.file)
            print(f"✅  Translated descriptions and examples in {args.file}")

    except Exception as e:
        print(f"❌  Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
