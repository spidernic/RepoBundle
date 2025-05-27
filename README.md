# RepoBundle

**Author:** Nic Cravino  
**Created:** May 25th, 2025  
**License:** Apache 2.0  

RepoBundle is a pair of small CLI utilities that let you turn a cloned Git repository into a single text file and recreate the repository from that file. The resulting file can easily be shared through email or other mediums without needing to send an entire archive.

## Features

**Preferred Tools:**

* **Export** a repository into a single, human-readable text file: `scripts/export_repo.py`.
* **Import** a repository from such a file: `scripts/import_repo.py`.
* Handles both text and binary files, with clear structure and error handling.

**Legacy Tools (archived in `scripts/old_version/`):**

* **Pack** a repository into a JSON-lines file (`pack_repo.py`).
* **Unpack** such a file (`unpack_repo.py`).
* These are retained for reference but are no longer recommended.

## Requirements

RepoBundle uses only Python's standard library (tested with Python 3.8+).

## Usage

### Exporting a Repository

Use `export_repo.py` to create a single, human-readable text file containing all files and structure of your repository:

```bash
python scripts/export_repo.py /path/to/your/repository
```
- This will generate a file like `yourrepo_export_YYYYMMDD_HHMMSS.txt` in the current directory.
- Binary files are base64 encoded; text files are included as plain text.

### Importing a Repository

Use `import_repo.py` to restore a repository from an exported file:

```bash
python scripts/import_repo.py yourrepo_export_YYYYMMDD_HHMMSS.txt /path/to/restore/location
```
- This will recreate the folder structure and files at the specified location.
- Both text and binary files will be restored appropriately.

Both scripts will print errors if issues occur (e.g., missing files, permission errors).

---

**Old Versions:**

Legacy scripts for packing/unpacking (JSON-lines format) are now in `scripts/old_version/` and are not recommended for new workflows.

## Project Layout

```
repo-root/
├── scripts/
│   ├── export_repo.py      # Preferred: export repo to readable text
│   ├── import_repo.py      # Preferred: import repo from export file
│   └── old_version/
│       ├── pack_repo.py    # Old: pack repo (JSON-lines)
│       └── unpack_repo.py  # Old: unpack repo (JSON-lines)
└── README.md
```

Legacy scripts are kept in `scripts/old_version/` for reference.


## Comparison: Old vs Preferred Tools

| Aspect                | pack_repo.py (Old)                          | export_repo.py (Preferred)                      |
|-----------------------|---------------------------------------------|-------------------------------------------------|
| Output Format         | JSON lines (machine-oriented)               | Structured text (human-oriented)                |
| Binary Handling       | All files base64-encoded                    | Text files shown as text, binaries as base64    |
| Headers/Metadata      | None                                        | Directory/file headers, timestamps, sizes       |
| CLI                   | Uses argparse                               | Uses sys.argv directly                          |
| Error Handling        | Skips unreadable files, prints to stderr    | Marks errors in output, prints errors           |
| Skips Hidden Files    | Only skips `.git` dir                       | Skips all hidden dirs/files (starting with .)   |

- **pack_repo.py**: Best for machine processing, backup, or exact restoration.
- **export_repo.py**: Best for human inspection, review, or documentation.

Feel free to adapt or extend these tools for your own workflow!

## License

This project is licensed under the [Apache License 2.0](LICENSE).
