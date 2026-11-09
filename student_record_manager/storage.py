"""
=============================================================================
Student Record Manager - Storage Engine (File Handling & JSON Persistence)
=============================================================================

This module handles persistent storage of student records:
- Safe reading and writing of JSON data using context managers.
- Serialization of Student / GraduateStudent objects to JSON format.
- Deserialization and polymorphic object reconstruction.
- Resilient error handling for missing files, empty files, and corrupted data.
- Timestamped file backups.
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Union

from .student import GraduateStudent, Student, StudentRecordError


class StorageError(StudentRecordError):
    """Raised when an error occurs during file or JSON storage operations."""
    pass


class StorageCorruptionError(StorageError):
    """Raised when stored JSON file is corrupted or contains invalid schemas."""
    pass


class StudentStorage:
    """
    Manages loading and saving Student entities to disk as JSON.

    Demonstrates:
    - Context managers ('with open(...)').
    - json.dump() and json.load().
    - pathlib.Path filesystem abstractions.
    - Defensive file handling and error containment.
    """

    DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "data" / "students.json"

    def __init__(self, file_path: Optional[Union[str, Path]] = None) -> None:
        """
        Initializes the storage manager with a target JSON file path.
        """
        if file_path is None:
            self.file_path = self.DEFAULT_DATA_PATH
        else:
            self.file_path = Path(file_path).resolve()

        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save_all(self, students: List[Student]) -> int:
        """
        Serializes a list of Student instances and writes them to the JSON file.

        Args:
            students: List of Student or GraduateStudent instances.

        Returns:
            Number of records successfully saved.
        """
        try:
            records = [student.to_dict() for student in students]
            payload = {
                "version": "1.0",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "count": len(records),
                "students": records,
            }

            # Write formatted JSON using context manager
            with open(self.file_path, mode="w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)

            return len(records)
        except OSError as e:
            raise StorageError(f"I/O error while writing to '{self.file_path}': {e}") from e
        except Exception as e:
            raise StorageError(f"Unexpected error serializing student data: {e}") from e

    def load_all(self) -> List[Student]:
        """
        Reads and deserializes all student records from the JSON file.

        Returns:
            List of reconstructed Student / GraduateStudent objects.
            Returns empty list if file does not exist yet.
        """
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, mode="r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)

            # Support both wrapped format {"students": [...]} and raw list [...]
            raw_students = data.get("students", []) if isinstance(data, dict) else data

            if not isinstance(raw_students, list):
                raise StorageCorruptionError(
                    f"Expected list of students in '{self.file_path.name}', found {type(raw_students).__name__}"
                )

            students: List[Student] = []
            for item in raw_students:
                if not isinstance(item, dict):
                    continue
                # Student.from_dict polymorphically handles Undergraduate and Graduate
                student_instance = Student.from_dict(item)
                students.append(student_instance)

            return students

        except json.JSONDecodeError as e:
            raise StorageCorruptionError(
                f"JSON syntax error in '{self.file_path.name}' at line {e.lineno}, col {e.colno}: {e.msg}"
            ) from e
        except OSError as e:
            raise StorageError(f"I/O error while reading '{self.file_path}': {e}") from e

    def backup(self, backup_dir: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """
        Creates a timestamped backup copy of the current storage file.
        """
        if not self.file_path.exists():
            return None

        target_dir = Path(backup_dir) if backup_dir else self.file_path.parent / "backups"
        target_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = target_dir / f"{self.file_path.stem}_{timestamp}.json"

        shutil.copy2(self.file_path, backup_file)
        return backup_file

