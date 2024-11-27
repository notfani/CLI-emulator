import os
import sys
import tarfile

class ShellEmulator:
    def __init__(self, computer_name, tar_path):
        self.computer_name = computer_name
        self.tar_path = tar_path
        self.current_path = '/'
        self.fs = {}  # Virtual file system (dictionary)
        self.load_tar()

    def load_tar(self):
        """Load the TAR archive into memory."""
        with tarfile.open(self.tar_path, "r") as tar:
            for member in tar.getmembers():
                self.fs[member.name.rstrip("/")] = {
                    "is_dir": member.isdir(),
                    "content": tar.extractfile(member).read() if member.isfile() else None,
                }

    def run(self):
        """Main emulator loop."""
        try:
            while True:
                cmd = input(f"{self.computer_name}:{self.current_path}$ ").strip()
                if cmd:
                    self.execute_command(cmd)
        except KeyboardInterrupt:
            print("\nExiting shell.")

    def execute_command(self, cmd):
        """Parse and execute a shell command."""
        parts = cmd.split()
        command = parts[0]
        args = parts[1:]

        if command == "ls":
            self.ls(args)
        elif command == "cd":
            self.cd(args)
        elif command == "cp":
            self.cp(args)
        elif command == "find":
            self.find(args)
        elif command == "echo":
            self.echo(args)
        elif command == "exit":
            print("Bye!")
            sys.exit(0)
        else:
            print(f"Unknown command: {command}")

    def ls(self, args):
        """List directory contents."""
        path = self.resolve_path(args[0] if args else self.current_path)
        if path not in self.fs or not self.fs[path]["is_dir"]:
            print(f"ls: cannot access '{path}': No such file or directory")
            return
        items = [p.split("/")[-1] for p in self.fs if p.startswith(path + "/")]
        print("\n".join(sorted(set(items))))

    def cd(self, args):
        """Change directory."""
        if not args:
            self.current_path = "/"
            return
        path = self.resolve_path(args[0])
        if path in self.fs and self.fs[path]["is_dir"]:
            self.current_path = path
        else:
            print(f"cd: no such file or directory: {path}")

    def cp(self, args):
        """Copy files."""
        if len(args) < 2:
            print("cp: missing file operand")
            return
        src = self.resolve_path(args[0])
        dest = self.resolve_path(args[1])
        if src in self.fs and not self.fs[src]["is_dir"]:
            self.fs[dest] = {"is_dir": False, "content": self.fs[src]["content"]}
        else:
            print(f"cp: cannot stat '{src}': No such file or directory")

    def find(self, args):
        """Find files and directories."""
        query = args[0] if args else ""
        results = [p for p in self.fs if query in p]
        print("\n".join(results))

    def echo(self, args):
        """Echo text."""
        print(" ".join(args))

    def resolve_path(self, path):
        """Resolve relative paths to absolute paths."""
        if path.startswith("/"):
            return path.rstrip("/")
        return f"{self.current_path.rstrip('/')}/{path}".rstrip("/")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--computer-name", required=True, help="Computer name for shell prompt")
    parser.add_argument("--tar-path", required=True, help="Path to the virtual filesystem tar file")
    args = parser.parse_args()

    emulator = ShellEmulator(args.computer_name, args.tar_path)
    emulator.run()
