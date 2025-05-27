# RepoBundle

RepoBundle is a pair of small CLI utilities that let you turn a cloned Git repository into a single text file and recreate the repository from that file. The resulting file can easily be shared through email or other mediums without needing to send an entire archive.

## Features

* **Pack** an existing repository into a timestamped `output_YYYYMMDD_HHMMSS.txt` file.
* **Unpack** such a file back into a folder structure.
* Files are stored using Base64 encoding inside newline separated JSON records.
* Skips the `.git` folder when packing.

## Requirements

RepoBundle uses only Python's standard library (tested with Python 3.8+).

## Usage

```bash
# Pack a repository
$ scripts/pack_repo.py path/to/repository

# Pack and specify output name
$ scripts/pack_repo.py path/to/repository -o mybundle.txt

# Unpack a previously generated file
$ scripts/unpack_repo.py mybundle.txt path/to/restore
```

Both commands provide basic error output if issues occur (missing files, permission errors, etc.).

## Project Layout

```
repo-root/
├── scripts/
│   ├── pack_repo.py    # CLI to pack repositories
│   └── unpack_repo.py  # CLI to unpack files
└── README.md
```

Feel free to adapt or extend these tools for your own workflow!
