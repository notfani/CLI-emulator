### **README.md**

# Shell Emulator

A shell emulator designed to mimic the behavior of a UNIX-like shell, operating entirely in memory. The emulator uses a TAR archive as a virtual file system, which is loaded into memory without unpacking it onto the disk.

This project supports the following shell commands:
- `ls` — List directory contents.
- `cd` — Change the current directory.
- `cp` — Copy files within the virtual file system.
- `find` — Search for files and directories by name.
- `echo` — Print messages to the terminal.
- `exit` — Exit the emulator.

The emulator runs in a Command Line Interface (CLI) and is suitable for learning, experimentation, and testing.

---

## **Features**

- **Virtual File System**: Works directly with a TAR archive loaded into memory, simulating a real file system.
- **UNIX-like Shell**: Provides a familiar shell experience with essential commands.
- **Efficient in Memory**: No disk unpacking; operations are performed entirely in RAM.
- **Test Coverage**: Includes unit tests for all commands to ensure functionality.

---

## **Getting Started**

### **Prerequisites**

- Python 3.7 or higher
- Basic understanding of the command line

---

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/shell_emulator.git
   cd shell_emulator
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### **Usage**

Run the emulator using the following command:
  ```bash
  python -m shell_emulator.emulator --computer-name <computer_name> --tar-path <path_to_tar>
   ```

- **`<computer_name>`**: The name to display in the shell prompt.
- **`<path_to_tar>`**: Path to the TAR file representing the virtual file system.

Example:
  ```bash
  python -m shell_emulator.emulator --computer-name my_pc --tar-path filesystem.tar
  ```

---

### **Commands**

#### **1. `ls`**
Lists the contents of the current or specified directory.

- Usage: `ls [path]`
- Example:
  ```bash
  ls           # List contents of the current directory
  ls folder/   # List contents of the 'folder/' directory
  ```

#### **2. `cd`**
Changes the current working directory.

- Usage: `cd [path]`
- Example:
  ```bash
  cd folder/   # Change to the 'folder/' directory
  cd /         # Change to the root directory
  ```

#### **3. `cp`**
Copies a file to a new location.

- Usage: `cp <source> <destination>`
- Example:
  ```bash
  cp file.txt folder/copied_file.txt  # Copy file.txt to folder/copied_file.txt
  ```

#### **4. `find`**
Searches for files or directories matching the specified pattern.

- Usage: `find <pattern>`
- Example:
  ```bash
  find file    # Find all files or directories containing 'file' in their name
  ```

#### **5. `echo`**
Prints the provided text to the terminal.

- Usage: `echo <text>`
- Example:
  ```bash
  echo Hello, World!  # Prints "Hello, World!"
  ```

#### **6. `exit`**
Exits the shell emulator.

- Usage: `exit`
- Example:
  ```bash
  exit  # Ends the emulator session
  ```

---

### **Testing**

The project includes unit tests to ensure all commands work as expected. To run the tests:

1. Run the following command in the root directory:
   ```bash
   python -m unittest discover shell_emulator/tests
   ```

2. The test suite will automatically discover and run all tests, producing output similar to:
   ```
   ....
   ----------------------------------------------------------------------
   Ran 4 tests in 0.002s

   OK
   ```

---

## **Examples**

### **Starting the Emulator**
  ```bash
  python -m shell_emulator.emulator --computer-name test_pc --tar-path test_filesystem.tar
  ```

### **Sample Commands**
1. List files:
   ```bash
   test_pc:/$ ls
   file.txt
   folder/
   ```
2. Change directory:
   ```bash
   test_pc:/$ cd folder
   test_pc:/folder$ 
   ```
3. Copy a file:
   ```bash
   test_pc:/folder$ cp ../file.txt copied_file.txt
   test_pc:/folder$ ls
   copied_file.txt
   ```
4. Find a file:
   ```bash
   test_pc:/folder$ find file
   /file.txt
   /folder/copied_file.txt
   ```

---

## **Project Structure**

The project is organized as follows:

```
shell_emulator/
├── shell_emulator/
│   ├── __init__.py            # Package initialization file
│   ├── emulator.py            # Core emulator logic
│   └── tests/
│       ├── __init__.py        # Package initialization for tests
│       └── test_emulator.py   # Unit tests for emulator functionality
├── README.md                  # Project documentation
├── requirements.txt           # Dependencies (empty in this case)
```

---

## **Future Enhancements**

- Support for additional commands (`mv`, `rm`, etc.).
- Enhanced `find` functionality with regex support.
- Improved error handling and user feedback.
- Interactive shell scripting support.

---

## **Contributing**

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes and submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.
```