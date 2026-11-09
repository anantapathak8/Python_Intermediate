"""
=============================================================================
Concept 05: File Handling and Context Managers in Python
=============================================================================

This module demonstrates:
1. Context Managers ('with open(...) as f:'): Guaranteed deterministic closing.
2. File Modes:
   - 'w' (Write / Overwrite)
   - 'a' (Append)
   - 'r' (Read)
   - 'r+' (Read & Write)
   - 'x' (Exclusive creation)
3. Reading Techniques:
   - file.read(): Reads full file into memory
   - file.readline(): Reads a single line
   - file.readlines(): Reads all lines into a list
   - Line-by-line iteration: Memory-efficient streaming for large files
4. Writing Techniques:
   - file.write(): Writes a string
   - file.writelines(): Writes an iterable of string lines
5. Safe Path Management using pathlib.Path and error handling (FileNotFoundError).
"""

import tempfile
from pathlib import Path
from typing import List


# =============================================================================
# File Operations Functions
# =============================================================================

def write_text_file(file_path: Path, content: str) -> int:
    """
    Writes text to a file using 'w' mode with UTF-8 encoding.
    Overwrites the file if it already exists.
    Returns the number of characters written.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, mode="w", encoding="utf-8") as f:
        chars_written = f.write(content)
    return chars_written


def append_to_file(file_path: Path, lines: List[str]) -> None:
    """
    Appends multiple lines to an existing file using 'a' mode.
    Demonstrates file.writelines().
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, mode="a", encoding="utf-8") as f:
        formatted_lines = [line if line.endswith("\n") else f"{line}\n" for line in lines]
        f.writelines(formatted_lines)


def read_entire_file(file_path: Path) -> str:
    """
    Reads the full content of a file using 'r' mode and file.read().
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot read: File '{file_path}' does not exist.")

    with open(file_path, mode="r", encoding="utf-8") as f:
        return f.read()


def read_file_as_lines(file_path: Path) -> List[str]:
    """
    Reads all lines into a stripped list of strings using file.readlines().
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot read: File '{file_path}' does not exist.")

    with open(file_path, mode="r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


def stream_file_line_by_line(file_path: Path) -> int:
    """
    Streams a file line-by-line using iteration protocol.
    This is memory efficient for large files.
    Returns total line count.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot read: File '{file_path}' does not exist.")

    line_count = 0
    with open(file_path, mode="r", encoding="utf-8") as f:
        for _ in f:
            line_count += 1
    return line_count


def demonstrate_read_write_mode(file_path: Path) -> str:
    """
    Demonstrates 'r+' mode (reading and in-place updating).
    """
    with open(file_path, mode="r+", encoding="utf-8") as f:
        _ = f.readline()
        f.seek(0, 2)  # Seek to end of file
        f.write("[LOG ENTRY: Verification passed]\n")
        f.seek(0)
        return f.read()


# =============================================================================
# Demonstration Runner
# =============================================================================

def demo_file_handling() -> None:
    """Demonstrates write, append, read, context managers, and modes."""
    print("=" * 70)
    print("DEMO: 05 - File Handling and Context Managers in Python")
    print("=" * 70)

    # Use a safe temporary directory to avoid cloud sync file locks (e.g. OneDrive)
    with tempfile.TemporaryDirectory() as temp_dir_str:
        demo_dir = Path(temp_dir_str)
        demo_file = demo_dir / "student_logs.txt"

        # 1. Writing to a file ('w' mode)
        print("\n--- 1. Writing Initial Content ('w' mode) ---")
        initial_content = (
            "HEADER: Student Activity Log\n"
            "2026-11-09 09:00:00 | Student STU001 registered for CS101\n"
            "2026-11-09 09:15:00 | Student STU002 registered for MATH201\n"
        )
        chars = write_text_file(demo_file, initial_content)
        print(f"Wrote {chars} characters to {demo_file.name}")

        # 2. Appending to a file ('a' mode)
        print("\n--- 2. Appending New Records ('a' mode) ---")
        additional_entries = [
            "2026-11-09 10:00:00 | Student STU001 submitted Assignment 1",
            "2026-11-09 11:30:00 | Student STU003 registered for CS101",
        ]
        append_to_file(demo_file, additional_entries)
        print(f"Appended {len(additional_entries)} entries successfully.")

        # 3. Reading entire file ('r' mode with .read())
        print("\n--- 3. Reading Entire File (file.read()) ---")
        full_text = read_entire_file(demo_file)
        print("File contents:\n" + full_text.strip())

        # 4. Reading file line-by-line as list (file.readlines())
        print("\n--- 4. Reading Lines into List (file.readlines()) ---")
        lines = read_file_as_lines(demo_file)
        for idx, line in enumerate(lines, 1):
            print(f"  Line {idx}: {line}")

        # 5. Streaming line-by-line (Generator / Iterable)
        print("\n--- 5. Streaming Line-by-Line (Memory Efficient) ---")
        count = stream_file_line_by_line(demo_file)
        print(f"Total lines counted via generator stream: {count}")

        # 6. Read & Write in-place ('r+' mode)
        print("\n--- 6. Read and Write Mode ('r+' mode) ---")
        updated_content = demonstrate_read_write_mode(demo_file)
        print(f"File after 'r+' append and rewind:\n{updated_content.strip()}")

        # 7. Safe handling of missing file (FileNotFoundError)
        print("\n--- 7. Exception Handling for Missing Files ---")
        non_existent = demo_dir / "does_not_exist.txt"
        try:
            read_entire_file(non_existent)
        except FileNotFoundError as err:
            print(f"Properly caught expected exception: {err}")

    print("\n[OK] Concept 05 demonstration completed successfully.\n")


if __name__ == "__main__":
    demo_file_handling()
