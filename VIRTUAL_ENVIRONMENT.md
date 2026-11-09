# Complete Guide to Python Virtual Environments

A comprehensive reference for creating, activating, managing, and troubleshooting isolated Python virtual environments across Windows, macOS, and Linux.

---

## 1. What is a Virtual Environment?

A **virtual environment** is a self-contained directory tree that contains a specific Python installation alongside an isolated set of additional third-party packages and dependencies.

### Why Virtual Environments are Essential

1. **Dependency Isolation**: Different projects frequently require different versions of the same library (e.g., Project A needs `pytest==7.1.0` while Project B requires `pytest==9.1.0`). Virtual environments prevent version conflicts.
2. **Prevent System Pollution**: Installing packages into your global system Python can break OS-level tools and utilities that rely on system-wide Python packages.
3. **Reproducibility**: With a virtual environment and a `requirements.txt` file, any collaborator, CI/CD pipeline, or deployment server can recreate the identical execution environment in seconds.
4. **Sandboxed Experimentation**: You can install, test, upgrade, and delete libraries without risking stability across other projects.

---

## 2. Anatomy: How `venv` Works Under the Hood

When you execute `python -m venv .venv`, Python creates the following directory structure:

```
.venv/
├── pyvenv.cfg          # Configuration pointing to base Python executable
├── Scripts/            # (Windows) Contains python.exe, pip.exe, and activate scripts
│   ├── activate
│   ├── activate.bat
│   ├── Activate.ps1
│   ├── pip.exe
│   └── python.exe
├── bin/                # (macOS/Linux equivalent of Scripts/)
│   ├── activate
│   ├── pip
│   └── python
└── Lib/
    └── site-packages/  # Where all third-party libraries (e.g. pytest) are installed
```

### How Activation Operates
When you run an activation script:
- It prepends `.venv\Scripts` (or `.venv/bin`) to your operating system's `PATH` environment variable.
- Whenever you type `python` or `pip`, your shell now executes the binaries inside `.venv` rather than the global Python.
- Your terminal prompt is prefixed with `(.venv)`.

---

## 3. Step-by-Step Setup Guide

### Step 1: Open Your Terminal
Open PowerShell, Command Prompt, or Bash in the root directory of this project:
```powershell
cd c:\Users\anant\OneDrive\Desktop\Python_Intermediate_Week02
```

### Step 2: Create the Virtual Environment
Run Python's built-in `venv` module:

```powershell
# Windows / macOS / Linux
python -m venv .venv
```

> **Note**: `.venv` is standard convention. The leading dot hides the folder in Unix-based file explorers and is pre-configured in `.gitignore`.

---

### Step 3: Activate the Virtual Environment

#### Option A: Windows PowerShell (Recommended)
```powershell
.\.venv\Scripts\Activate.ps1
```

If you encounter an execution policy error:
```powershell
# Resolve execution policy restriction for CurrentUser:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass flag for the current session:
powershell -ExecutionPolicy Bypass -File .\.venv\Scripts\Activate.ps1
```

#### Option B: Windows Command Prompt (`cmd.exe`)
```cmd
.\.venv\Scripts\activate.bat
```

#### Option C: Windows Git Bash / WSL
```bash
source .venv/Scripts/activate
```

#### Option D: macOS / Linux (bash / zsh)
```bash
source .venv/bin/activate
```

Once activated, your terminal prompt will display:
```
(.venv) PS C:\Users\anant\OneDrive\Desktop\Python_Intermediate_Week02>
```

---

### Step 4: Upgrade `pip` and Install Dependencies

With the virtual environment active:

```powershell
# Upgrade pip package installer
python -m pip install --upgrade pip

# Install project requirements (including pytest)
pip install -r requirements.txt
```

Verify installed packages:
```powershell
pip list
```

---

### Step 5: Run Code and Tests in the Virtual Environment

Run concept modules:
```powershell
python concepts/01_classes_and_objects.py
python concepts/02_inheritance_and_encapsulation.py
python concepts/03_modules_and_imports.py
python concepts/04_exception_handling.py
python concepts/05_file_handling.py
python concepts/06_json_handling.py
```

Run the interactive application:
```powershell
python -m student_record_manager.main
```

Run test suite:
```powershell
pytest test_week2.py -v
```

---

### Step 6: Deactivating the Environment
When you are done working on the project, deactivate the environment to return to your global shell:

```powershell
deactivate
```

The `(.venv)` prefix will disappear from your command prompt.

---

## 4. Managing Requirements with `pip`

| Task | Command |
| :--- | :--- |
| Install a specific library | `pip install <package-name>` |
| Install exact version | `pip install pytest==9.1.1` |
| Install minimum version | `pip install "pytest>=7.4.0"` |
| Export current environment | `pip freeze > requirements.txt` |
| Install from requirements file | `pip install -r requirements.txt` |
| Uninstall a library | `pip uninstall <package-name>` |
| Check for outdated packages | `pip list --outdated` |

---

## 5. Best Practices Checklist

- [x] **Never commit virtual environments to Git**: Always verify `.venv/` and `venv/` are listed in `.gitignore`. Virtual environments contain system-specific absolute symlinks and binaries that cannot be ported across machines.
- [x] **Always commit `requirements.txt`**: This is your lightweight, portable bill of materials.
- [x] **Use `.venv` for the environment name**: Standardized name recognized automatically by IDEs like VS Code and PyCharm.
- [x] **Recreate rather than move**: If you rename or move the project folder, delete `.venv` and recreate it. The internal scripts hardcode absolute file paths.
- [x] **Direct Python Execution**: You can execute scripts inside the environment without activating it by pointing directly to the virtual Python binary:
  ```powershell
  .\.venv\Scripts\python.exe test_week2.py
  ```

---

## 6. Troubleshooting Common Issues

### Issue 1: PowerShell `PSSecurityException` (Script Execution Disabled)
**Error Message**:
```
File C:\...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```
**Fix**:
Execute this one-time command in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 2: VS Code Not Using the Virtual Environment
**Fix**:
1. Press `Ctrl + Shift + P` in VS Code.
2. Type and select `Python: Select Interpreter`.
3. Choose the interpreter with `('.venv': venv)` in its path (e.g., `.\.venv\Scripts\python.exe`).

### Issue 3: `pip` Command Not Found
**Fix**:
Ensure you are using `python -m pip install <package>` rather than calling `pip` directly. This guarantees the package installs into the exact Python environment running the command.

