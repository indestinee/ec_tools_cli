import os
import shutil
import unittest

from ec_rasp_tools.common.utils import logger_utils

logger = logger_utils.setup_logger()


class EncTest(unittest.TestCase):
    data_path: str = "test/tmp/"

    def test_enc(self):
        os.makedirs(self.data_path, exist_ok=True)
        logger.info("testing in path %s", os.path.abspath(self.data_path))
        test_file_size = [
            1024 * 1024 * 10,
            1024 * 1024 * 10 + 1024,
            1024 * 1024 * 10 + 2,
            1024 + 2,
            1024 * 1024,
            2,
        ]
        for size in test_file_size:
            self.enc_dec(size)

    def enc_dec(self, size: int):
        logger.info("testing enc/dec with size %s", size)
        fp = f"{self.data_path}/test.bin"
        with open(fp, "wb") as f:
            f.write(os.urandom(size))
        os.system(f"ec-enc -p 1234 -e {fp} -o {fp}.enc")
        os.system(f"ec-enc -p 1234 -d {fp}.enc -o {fp}.dec")
        with open(fp, "rb") as f:
            data = f.read()
        with open(f"{fp}.dec", "rb") as f:
            data_dec = f.read()
        self.assertEqual(data, data_dec)
        os.remove(fp)
        os.remove(f"{fp}.enc")
        os.remove(f"{fp}.dec")

    def tearDown(self) -> None:
        if os.path.exists(self.data_path):
            shutil.rmtree(self.data_path)
        return super().tearDown()
