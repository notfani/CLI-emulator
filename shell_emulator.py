import tarfile
import os
import sys


class ShellEmulator:
    def __init__(self, hostname, tar_path):
        self.hostname = hostname
        self.cwd = '/tmp/emulator'  # Текущая директория по умолчанию
        self.root = '/tmp/emulator'  # Корневая директория для файловой системы
        self.load_tarfs(tar_path)

    def load_tarfs(self, tar_path):
        # Распаковка tar архива во временную директорию
        if not os.path.exists(self.root):
            os.makedirs(self.root)

        with tarfile.open(tar_path) as tar:
            tar.extractall(path=self.root)

    def prompt(self):
        return f"{self.hostname}:{self.cwd}$ "

    def run(self):
        while True:
            command = input(self.prompt())
            self.execute(command)

    def execute(self, command):
        parts = command.strip().split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'ls':
            self.ls(args)
        elif cmd == 'cd':
            self.cd(args)
        elif cmd == 'cp':
            self.cp(args)
        elif cmd == 'find':
            self.find(args)
        elif cmd == 'echo':
            self.echo(args)
        elif cmd == 'exit':
            sys.exit(0)
        else:
            print(f"{cmd}: command not found")

    def ls(self, args):
        path = self.cwd if not args else os.path.join(self.cwd, args[0])
        try:
            for item in os.listdir(path):
                print(item)
        except FileNotFoundError:
            print(f"ls: cannot access '{path}': No such file or directory")

    def cd(self, args):
        if not args:
            print("cd: missing argument")
            return
        new_dir = os.path.join(self.cwd, args[0])
        if os.path.isdir(new_dir):
            self.cwd = os.path.abspath(new_dir)
        else:
            print(f"cd: {new_dir}: No such file or directory")

    def cp(self, args):
        if len(args) != 2:
            print("cp: missing file operand")
            return
        src = os.path.join(self.cwd, args[0])
        dest = os.path.join(self.cwd, args[1])
        try:
            shutil.copy(src, dest)
        except Exception as e:
            print(f"cp: {e}")

    def find(self, args):
        search_path = self.cwd if not args else args[0]
        target = args[1] if len(args) > 1 else ''
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if target in file:
                    print(os.path.join(root, file))

    def echo(self, args):
        print(' '.join(args))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: emulator.py <hostname> <path_to_tar>")
        sys.exit(1)

    hostname = sys.argv[1]
    tar_path = sys.argv[2]

    emulator = ShellEmulator(hostname, tar_path)
    emulator.run()
