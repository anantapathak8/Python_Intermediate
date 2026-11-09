"""
=============================================================================
Student Record Manager Package
=============================================================================

A modular, object-oriented Python package showcasing:
- OOP: Classes, inheritance, encapsulation, and polymorphism.
- Modular architecture with clean imports and exports.
- Robust exception handling and domain models.
- File handling and JSON persistence.
"""

from .manager import StudentRecordManager
from .storage import StorageCorruptionError, StorageError, StudentStorage
from .student import (
    DuplicateStudentError,
    GraduateStudent,
    Student,
    StudentNotFoundError,
    StudentRecordError,
    ValidationError,
)

__version__ = "1.0.0"

__all__ = [
    "Student",
    "GraduateStudent",
    "StudentRecordManager",
    "StudentStorage",
    "StudentRecordError",
    "ValidationError",
    "StudentNotFoundError",
    "DuplicateStudentError",
    "StorageError",
    "StorageCorruptionError",
]

