import unittest
import tarfile
from io import BytesIO
from shell_emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.tar_data = BytesIO()
        with tarfile.open(fileobj=self.tar_data, mode="w") as tar:
            file_data = BytesIO(b"Hello, World!")
            tarinfo = tarfile.TarInfo("file.txt")
            tarinfo.size = len(file_data.getvalue())
            tar.addfile(tarinfo, file_data)

            dir_info = tarfile.TarInfo("folder/")
            dir_info.type = tarfile.DIRTYPE
            tar.addfile(dir_info)

        self.tar_data.seek(0)
        self.shell_emulator = ShellEmulator("test_pc", self.tar_data)

    def test_ls(self):
        output = self.shell_emulator.ls([])
        self.assertIn("file.txt", output)
        self.assertIn("folder/", output)

    def test_cd(self):
        self.shell_emulator.cd(["folder"])
        self.assertEqual(self.shell_emulator.current_path, "/folder")

    def tearDown(self):
        self.tar_data.close()


if __name__ == "__main__":
    unittest.main()
