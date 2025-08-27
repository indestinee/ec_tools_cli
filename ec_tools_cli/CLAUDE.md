# CLAUDE.md

## Project Overview
This project is a collection of CLI tools for automation, backup, encryption, database management, and vault operations, based on [ec_tools](https://github.com/indestinee/ec_tools). It is modular, extensible, and designed for use in various automation and data management scenarios.

## Key Features
- **Auto-Run**: Automate running scripts or commands (Python, C++, etc.) via a unified CLI.
- **Backup Machine**: Backup, unload, and manage machine data with utilities for zipping and storage.
- **Database Tools**: CLI for database operations and management.
- **Encryption & Vault**: Secure encryption, decryption, and parameter management with vault support.
- **Common Utilities**: Logging and shared utility functions.

## Usage Examples
```bash
# Auto-run a Python script
python -m ec_tools_cli.auto_run.cli --file script.py

# Backup a machine
python -m ec_tools_cli.backup_machine.cli --backup --config config.json

# Encrypt a file
python -m ec_tools_cli.enc.cli --encrypt --input data.txt --output data.enc

# Vault parameter operations
python -m ec_tools_cli.vault.cli --set-param key value
```

## API Reference

### Main Modules
- `auto_run.cli`: Entry point for auto-run features. Supports running scripts with different runners (`py_runner`, `cpp_runner`).
- `backup_machine.cli`: CLI for backup operations. Uses `backup_machine.py`, `unload_machine.py`, and utilities for zipping and config management.
- `db.cli`: Database management CLI.
- `enc.cli`: Encryption/decryption CLI.
- `vault.cli`: Vault and parameter management CLI. Uses `encryption.py` and parameter submodules.

### Core Classes & Functions
- `auto_run.runner.py_runner.PyRunner`: Runs Python scripts.
- `auto_run.runner.cpp_runner.CppRunner`: Runs C++ programs.
- `backup_machine.backup_machine.BackupMachine`: Handles backup logic.
- `backup_machine.utils`: Utility functions for backup and zipping.
- `common.utils.logger_utils`: Logging utilities.
- `vault.encryption`: Encryption/decryption helpers.
- `vault.parameter.parameter`: Parameter management.

### Input/Output
- Most CLIs accept arguments via command line (see `--help` for each module).
- Input: file paths, config files, parameters.
- Output: processed files, encrypted data, backup archives, logs.

### Error Handling
- Errors are logged using `common.utils.logger_utils`.
- Most modules use try/except and print/log errors to the console or log files.

## Development Notes

### Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run CLI tools as Python modules (see Usage Examples).

### Testing Procedures
- Unit tests are in `test/` (e.g., `enc_test.py`, `vault_test.py`).
- Run tests with:
  ```bash
  python -m unittest discover test
  ```

### Known Limitations
- Some modules may require specific config files (see `backup_machine/data/config.py`).
- Not all features are fully documented; refer to code for advanced usage.

## File Structure
```
ec_tools_cli/
├── auto_run/
│   ├── cli.py
│   └── runner/
│       ├── auto_runner.py
│       ├── cpp_runner.py
│       └── py_runner.py
├── backup_machine/
│   ├── backup_machine.py
│   ├── cli.py
│   ├── unload_machine.py
│   ├── utils.py
│   ├── zip_storage.py
│   └── data/
│       ├── config.py
│       └── record.py
├── common/
│   └── utils/
│       └── logger_utils.py
├── db/
│   └── cli.py
├── enc/
│   └── cli.py
├── vault/
│   ├── cli.py
│   ├── encryption.py
│   └── parameter/
│       ├── args.py
│       ├── parameter.py
│       └── process.py
└── ...
```
