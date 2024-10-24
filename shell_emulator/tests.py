import unittest
import os
import shutil
from ShellEmulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создание тестовой виртуальной файловой системы
        cls.emulator = ShellEmulator("test_host", "test_fs.tar")
        cls.test_dir = '/tmp/emulator/test_dir'
        os.makedirs(cls.test_dir, exist_ok=True)
        with open(os.path.join(cls.test_dir, 'file1.txt'), 'w') as f:
            f.write('Test file 1')

    def test_ls(self):
        # Проверяем вывод команды ls
        self.emulator.cwd = self.test_dir
        result = self.emulator.ls([])
        self.assertIn('file1.txt', result)

    def test_cd(self):
        # Проверяем работу cd
        self.emulator.cwd = '/tmp/emulator'
        self.emulator.cd(['test_dir'])
        self.assertEqual(self.emulator.cwd, self.test_dir)

    def test_cp(self):
        # Проверяем копирование файла
        self.emulator.cwd = self.test_dir
        self.emulator.cp(['file1.txt', 'file2.txt'])
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'file2.txt')))

    def test_find(self):
        # Проверяем работу команды find
        result = self.emulator.find([self.test_dir, 'file1'])
        self.assertIn('file1.txt', result)

    def test_echo(self):
        # Проверяем echo
        result = self.emulator.echo(['Hello, World!'])
        self.assertEqual(result, 'Hello, World!')

    @classmethod
    def tearDownClass(cls):
        # Удаление виртуальной файловой системы после тестов
        shutil.rmtree('/tmp/emulator')


if __name__ == '__main__':
    unittest.main()
