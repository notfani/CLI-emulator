import os
import tarfile
import shutil
import sys


class ShellEmulator:
    def __init__(self, hostname, tar_path):
        self.hostname = hostname
        self.current_dir = '/'
        self.root = '/tmp/virtual_fs'
        self.setup_filesystem(tar_path)

    def setup_filesystem(self, tar_path):
        # Распаковка архива tar во временную директорию
        if not tarfile.is_tarfile(tar_path):
            print("Ошибка: файл не является tar-архивом.")
            sys.exit(1)

        if os.path.exists(self.root):
            shutil.rmtree(self.root)  # Удаление старого содержимого

        os.mkdir(self.root)
        with tarfile.open(tar_path) as tar:
            tar.extractall(self.root)

    def start(self):
        # Основной цикл работы оболочки
        while True:
            command = input(f"{self.hostname}:{self.current_dir}$ ")
            self.run_command(command)

    def run_command(self, command):
        parts = command.strip().split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if cmd == 'exit':
            sys.exit(0)
        elif cmd == 'ls':
            self.ls(args)
        elif cmd == 'cd':
            self.cd(args)
        elif cmd == 'cp':
            self.cp(args)
        elif cmd == 'find':
            self.find(args)
        elif cmd == 'echo':
            self.echo(args)
        else:
            print(f"Команда не найдена: {cmd}")

    def ls(self, args):
        dir_to_list = self.get_full_path(args[0] if args else self.current_dir)
        try:
            for entry in os.listdir(dir_to_list):
                print(entry)
        except FileNotFoundError:
            print(f"Ошибка: каталог {dir_to_list} не найден.")

    def cd(self, args):
        if len(args) == 0:
            print("Ошибка: отсутствует аргумент для команды cd.")
            return

        new_dir = self.get_full_path(args[0])
        if os.path.isdir(new_dir):
            self.current_dir = new_dir.replace(self.root, '')
        else:
            print(f"Ошибка: {new_dir} не является каталогом.")

    def cp(self, args):
        if len(args) != 2:
            print("Ошибка: cp требует два аргумента.")
            return
        src = self.get_full_path(args[0])
        dst = self.get_full_path(args[1])
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        except FileNotFoundError:
            print(f"Ошибка: {src} или {dst} не найдены.")

    def find(self, args):
        if len(args) == 0:
            print("Ошибка: find требует хотя бы один аргумент.")
            return
        search_dir = self.get_full_path(args[0] if len(args) > 0 else self.current_dir)
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                print(os.path.join(root, file))

    def echo(self, args):
        print(" ".join(args))

    def get_full_path(self, path):
        # Преобразование относительных путей в абсолютные
        if path.startswith('/'):
            return os.path.join(self.root, path.lstrip('/'))
        else:
            return os.path.join(self.root, self.current_dir.lstrip('/'), path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python ShellEmulator.py <hostname> <tar_path>")
        sys.exit(1)

    hostname = sys.argv[1]
    tar_path = sys.argv[2]

    emulator = ShellEmulator(hostname, tar_path)
    emulator.start()
