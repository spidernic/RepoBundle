#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
from datetime import datetime


def pack_repo(repo_path: str, output_file: str) -> None:
    if not os.path.isdir(repo_path):
        raise ValueError(f"Repository path '{repo_path}' does not exist or is not a directory")
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for root, dirs, files in os.walk(repo_path):
            # Skip .git directory
            dirs[:] = [d for d in dirs if d != '.git']
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                try:
                    with open(file_path, 'rb') as f:
                        encoded = base64.b64encode(f.read()).decode('ascii')
                except Exception as exc:
                    print(f"Skipping {file_path}: {exc}", file=sys.stderr)
                    continue
                record = {'path': rel_path, 'content': encoded}
                out_f.write(json.dumps(record) + '\n')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Pack a repository into a single text file.')
    parser.add_argument('repo', help='Path to the cloned repository')
    parser.add_argument('-o', '--output', help='Output file name (default uses timestamp)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output = args.output or f'output_{timestamp}.txt'
    try:
        pack_repo(args.repo, output)
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
