import os
import shutil
import subprocess
import unittest

from ec_tools_cli.common.utils import logger_utils

logger = logger_utils.setup_logger()


def run(cmd: str):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True  # capture stdout & stderr  # decode bytes -> str
    )
    if result.returncode != 0:
        logger.error(f"Command failed: {cmd}\nStderr: {result.stderr.strip()}")
        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
    return result.stdout.strip()


class VaultTest(unittest.TestCase):
    data_path: str = "test/tmp/"

    def test_vault(self):
        os.makedirs(self.data_path, exist_ok=True)
        db_path = f"{self.data_path}/vault.db"
        run(f"ec-vault -db {db_path} list")
        run(f"ec-vault -db {db_path} insert -p 12345678 -k test -v 1234")
        run(f"ec-vault -db {db_path} list")
        self.assertEqual(run(f"ec-vault -db {db_path} get -p 12345678 -k test"), "1234")
        run(f"ec-vault -db {db_path} delete -k test")
        self.assertRaises(subprocess.CalledProcessError, run, f"ec-vault -db {db_path} get -p 12345678 -k test")
        run(f"ec-vault -db {db_path} list")

    def tearDown(self) -> None:
        if os.path.exists(self.data_path):
            shutil.rmtree(self.data_path)
        return super().tearDown()
