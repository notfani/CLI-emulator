import os
import tarfile
import shutil
import argparse

class ShellEmulator:
    def __init__(self, hostname, tar_path):
        self.hostname = hostname
        self.current_dir = '/'
        self.load_filesystem(tar_path)

    def load_filesystem(self, tar_path):
        """Загружает виртуальную файловую систему из tar-файла."""
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall('virtual_fs')
        self.fs_root = os.path.abspath('virtual_fs')

    def ls(self):
        """Список файлов и директорий в текущей директории."""
        path = os.path.join(self.fs_root, self.current_dir.lstrip('/'))
        print('\n'.join(os.listdir(path)))

    def cd(self, path):
        """Переход в другую директорию."""
        if path == '/':
            self.current_dir = '/'
        else:
            new_path = os.path.normpath(os.path.join(self.current_dir, path))
            abs_path = os.path.join(self.fs_root, new_path.lstrip('/'))
            if os.path.isdir(abs_path):
                self.current_dir = new_path
            else:
                print(f"{path}: Нет такой директории")

    def cp(self, src, dest):
        """Копирование файлов."""
        src_path = os.path.join(self.fs_root, self.current_dir.lstrip('/'), src)
        dest_path = os.path.join(self.fs_root, self.current_dir.lstrip('/'), dest)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            print(f"{src}: Файл не найден")

    def find(self, filename):
        """Поиск файлов по имени."""
        for root, dirs, files in os.walk(os.path.join(self.fs_root, self.current_dir.lstrip('/'))):
            if filename in files:
                print(os.path.join(root, filename))

    def echo(self, text):
        """Вывод текста."""
        print(text)

    def prompt(self):
        """Вывод приглашения к вводу."""
        return f"{self.hostname}:{self.current_dir}$ "

    def start(self):
        """Основной цикл обработки команд."""
        while True:
            command = input(self.prompt()).strip().split()
            if not command:
                continue
            cmd, *args = command
            if cmd == 'ls':
                self.ls()
            elif cmd == 'cd':
                if args:
                    self.cd(args[0])
                else:
                    print("cd: Ожидается аргумент")
            elif cmd == 'cp':
                if len(args) < 2:
                    print("cp: Ожидаются исходный и целевой файлы")
                else:
                    self.cp(args[0], args[1])
            elif cmd == 'find':
                if args:
                    self.find(args[0])
                else:
                    print("find: Ожидается имя файла")
            elif cmd == 'echo':
                print(' '.join(args))
            elif cmd == 'exit':
                break
            else:
                print(f"{cmd}: Команда не найдена")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор shell с виртуальной файловой системой.")
    parser.add_argument("hostname", help="Имя компьютера для приглашения")
    parser.add_argument("tar_path", help="Путь к tar-архиву с файловой системой")
    args = parser.parse_args()

    shell = ShellEmulator(args.hostname, args.tar_path)
    shell.start()
