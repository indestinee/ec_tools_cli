# ec-tools-cli

A small set of CLI tools for encryption, vault storage, backups, DB queries, auto-run, and QR codes.

## Install
```bash
pip install -r requirements.txt
pip install -e .
```

## Commands
- `ec-enc` — encrypt/decrypt files (AES-256-CBC).
- `ec-sql` — SQLite REPL.
- `ec-vault` — encrypted key/value vault.
- `ec-backup` — chunked encrypted backup + restore.
- `auto-run` — run `.py`, compile+run `.c/.cpp`.
- `ec-qrcode` — generate/scan QR codes.

## Usage

### `ec-enc`
```bash
# encrypt
ec-enc -e input.bin -o output.enc -p <password>

# decrypt
ec-enc -d output.enc -o output.bin -p <password>
```

### `ec-sql`
```bash
ec-sql -db /path/to/file.db
```
- Prints tables, then interactive SQL (`exit` to quit).

### `ec-vault`
```bash
# list keys
ec-vault list

# insert (value, file, or stdin)
ec-vault insert -p <password> -k <key> -v <value>
ec-vault insert -p <password> -k <key> -f /path/to/file

echo "secret" | ec-vault insert -p <password> -k <key>

# get (stdout or file)
ec-vault get -p <password> -k <key>
ec-vault get -p <password> -k <key> -o /path/to/output

# delete
ec-vault delete -k <key>
```
- Default DB: `~/.ec_tools/ec_tools.db`.

### `ec-backup`
```bash
# backup
ec-backup -c config.json -p <password> backup

# restore
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
Notes:
- Backs up by file hash/mtime/size; only changed files are packed.
- Files are encrypted in chunks and stored inside zipped packages.

### `auto-run`
```bash
auto-run path/to/file.py
auto-run path/to/file.cpp
```
- C/C++: compile with `g++ -O2 -Wall -std=c++17`, then run.
- If `<name>.in` and `<name>.txt` exist, it diffs output vs expected.

### `ec-qrcode`
```bash
# generate
ec-qrcode generate -m "hello" -s 20 -o out.png

# scan
ec-qrcode scan -i in.png -o decoded.txt
```

## One-off scripts
```bash
python -m ec_tools_cli.one_off.migrate_db -c config.json
```
- Migrates backup DB records to use relative zip paths.
