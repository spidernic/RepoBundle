#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
from pathlib import Path


def unpack_repo(input_file: str, output_dir: str) -> None:
    if not os.path.isfile(input_file):
        raise ValueError(f"Input file '{input_file}' does not exist")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                rel_path = record['path']
                content = base64.b64decode(record['content'].encode('ascii'))
            except Exception as exc:
                print(f"Skipping line {line_no}: {exc}", file=sys.stderr)
                continue
            dest_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            try:
                with open(dest_path, 'wb') as out_f:
                    out_f.write(content)
            except Exception as exc:
                print(f"Failed to write {dest_path}: {exc}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Unpack a repository from a packed text file.')
    parser.add_argument('input', help='Path to the packed text file')
    parser.add_argument('output', help='Directory to recreate the repository in')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        unpack_repo(args.input, args.output)
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
