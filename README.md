# ec-tools-cli

`ec-tools-cli` is a small Python CLI collection for:

- file encryption and decryption
- encrypted local vault storage
- incremental encrypted backups
- quick SQLite inspection
- local code runners for Python and C/C++
- QR code generation and scanning

The package targets Python 3.11+ and is distributed with standard console entry points via `pyproject.toml`.

## Requirements

- Python 3.11 or newer
- `uv` for the locked workflow, or `pip` for a plain install
- `g++` if you want to use `auto-run` with `.c` or `.cpp` files
- system libraries required by `pyzbar` if you want to scan QR codes

## Installation

### Recommended: `uv`

```bash
uv sync
```

This installs the project and the default development environment from the lockfile.

To run commands through the managed environment:

```bash
uv run ec-enc --help
uv run pytest
```

### Plain `pip`

```bash
pip install -e .
```

If you only want the runtime dependencies without an editable install:

```bash
pip install -r requirements.txt
```

## Available Commands

- `ec-enc`: encrypt or decrypt files with AES-256-CBC
- `ec-sql`: open a simple interactive SQLite query shell
- `ec-vault`: store and retrieve encrypted key/value entries in a local SQLite database
- `ec-backup`: create and restore encrypted chunked backups
- `auto-run`: run Python files or compile and run C/C++ files
- `ec-qrcode`: generate QR codes or decode them from images

## Usage

### `ec-enc`

Encrypt a file:

```bash
ec-enc -e input.bin -o output.enc -p <password>
```

Decrypt a file:

```bash
ec-enc -d output.enc -o output.bin -p <password>
```

### `ec-sql`

Open a SQLite database and run ad hoc queries:

```bash
ec-sql -db /path/to/file.db
```

The CLI prints the discovered tables first, then starts an interactive prompt. Type `exit` to quit.

### `ec-vault`

By default the vault database lives at `~/.ec_tools/ec_tools.db`.

List stored keys:

```bash
ec-vault list
```

Insert a value from the command line:

```bash
ec-vault insert -p <password> -k <key> -v <value>
```

Insert a value from a file:

```bash
ec-vault insert -p <password> -k <key> -f /path/to/file
```

Read a value to stdout:

```bash
ec-vault get -p <password> -k <key>
```

Write a value to a file:

```bash
ec-vault get -p <password> -k <key> -o /path/to/output
```

Delete a key:

```bash
ec-vault delete -k <key>
```

Use `-db /path/to/vault.db` to override the default database location.

### `ec-backup`

Create an encrypted backup:

```bash
ec-backup -c config.json -p <password> backup
```

Restore a backup:

```bash
ec-backup -c config.json -p <password> unpack -o /path/to/output
```

Minimal config:

```json
{
  "db_path": "/path/to/index.db",
  "src_path": "/path/to/source",
  "zip_path": "/path/to/archives"
}
```

Supported optional config fields include:

- `sub_dirs`
- `extensions`
- `ignored_extensions`
- `max_pack_count`
- `max_pack_size`
- `chunk_size`
- `batch_size`
- `scan_logging_interval`
- `pack_logging_interval`
- `pbkdf2_iters`

Behavior notes:

- backup candidates are checked by modified time, file size, and MD5
- file content is encrypted chunk by chunk before being written into zip-based storage
- restore verifies content integrity by recalculating MD5 after decryption

### `auto-run`

Run a Python file:

```bash
auto-run path/to/file.py
```

Compile and run a C or C++ file:

```bash
auto-run path/to/file.cpp
```

Current behavior:

- Python files are run with `python3`
- C/C++ files are compiled with `g++ -O2 -Wall -std=c++17`
- if `<name>.in` exists, it is piped into the binary
- if both `<name>.in` and `<name>.txt` exist, output is also written to `<name>.out` and diffed against the expected text file

### `ec-qrcode`

Generate a QR code:

```bash
ec-qrcode generate -m "hello" -s 20 -o out.png
```

Scan a QR code image:

```bash
ec-qrcode scan -i in.png -o decoded.txt
```

If no output path is given:

- `generate` opens the generated image
- `scan` prints the decoded messages

## Developer Workflow

Install development dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

The repository currently includes tests for:

- encryption and decryption round trips
- basic vault insert, read, list, and delete flows

Format code:

```bash
uv run black .
```

## Helper Scripts

The repo still includes shell helpers for installing scripts from `ec_tools_cli/bin`:

```bash
./scripts/install_bin.sh
./scripts/uninstall_bin.sh
```

These copy or remove the shell scripts in that directory from `/usr/local/bin`, and may require `sudo`.

## One-Off Migration

To migrate backup database records so stored zip paths become relative:

```bash
python -m ec_tools_cli.one_off.migrate_db -c config.json
```
