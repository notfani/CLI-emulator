import unittest
import os
import tarfile
import shutil
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем тестовую файловую систему"""
        os.makedirs("test_fs/test_dir", exist_ok=True)
        with open("test_fs/test_file.txt", "w") as f:
            f.write("hello")
        with tarfile.open("test_fs.tar", "w") as tar:
            tar.add("test_fs", arcname=os.path.basename("test_fs"))

    def setUp(self):
        """Создаем экземпляр эмулятора для тестов"""
        self.shell = ShellEmulator("test_host", "test_fs.tar")

    def test_ls(self):
        self.shell.ls()  # Ожидается "test_dir\ntest_file.txt"

    def test_cd_and_ls(self):
        self.shell.cd("test_dir")
        self.assertEqual(self.shell.current_dir, "/test_dir")
        self.shell.ls()  # Ожидается пустая директория

    def test_cp(self):
        self.shell.cp("test_file.txt", "copy_test_file.txt")
        self.assertTrue(os.path.exists(os.path.join(self.shell.fs_root, "copy_test_file.txt")))

    def test_find(self):
        self.shell.find("test_file.txt")  # Ожидается путь к файлу

    def test_echo(self):
        self.shell.echo("test")  # Ожидается "test"

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовые файлы и директории"""
        os.remove("test_fs.tar")
        shutil.rmtree("test_fs")
        shutil.rmtree("virtual_fs")

if __name__ == "__main__":
    unittest.main()
