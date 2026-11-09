"""
=============================================================================
Student Record Manager - Service Manager (Business Logic & Orchestration)
=============================================================================

This module contains the StudentRecordManager class:
- Manages an in-memory collection of Student and GraduateStudent entities.
- Enforces uniqueness, business rules, and validation invariants.
- Coordinates persistent JSON storage via StudentStorage.
- Provides search, analytics, grade aggregation, and reporting features.
"""

from typing import Any, Dict, List, Optional

from .storage import StudentStorage
from .student import (
    DuplicateStudentError,
    GraduateStudent,
    Student,
    StudentNotFoundError,
    ValidationError,
)


class StudentRecordManager:
    """
    Core management class for student records.

    Demonstrates:
    - Association and Dependency Injection (StudentStorage).
    - In-memory collection management (dictionary lookup by ID).
    - Exception handling for domain invariants.
    - Complex data transformations and academic analytics.
    """

    def __init__(self, storage: Optional[StudentStorage] = None) -> None:
        """
        Initializes the manager and loads existing records from storage if available.
        """
        self.storage = storage if storage is not None else StudentStorage()
        self._students: Dict[str, Student] = {}
        self.reload()

    def reload(self) -> int:
        """
        Loads records from storage into memory.
        Returns the number of students loaded.
        """
        self._students.clear()
        loaded = self.storage.load_all()
        for student in loaded:
            self._students[student.student_id] = student
        return len(self._students)

    def save(self) -> int:
        """
        Persists all in-memory records to storage.
        """
        return self.storage.save_all(list(self._students.values()))

    # --- CRUD Operations ---

    def add_student(self, student: Student, auto_save: bool = True) -> Student:
        """
        Adds a new student to the registry and optionally persists to disk.

        Raises:
            DuplicateStudentError: If student_id already exists.
        """
        if not isinstance(student, Student):
            raise ValidationError(f"Expected Student instance, got {type(student).__name__}")

        if student.student_id in self._students:
            raise DuplicateStudentError(student.student_id)

        self._students[student.student_id] = student

        if auto_save:
            self.save()

        return student

    def get_student(self, student_id: str) -> Student:
        """
        Retrieves a student by ID.

        Raises:
            StudentNotFoundError: If no student matches the ID.
        """
        clean_id = student_id.strip().upper()
        if clean_id not in self._students:
            raise StudentNotFoundError(clean_id)
        return self._students[clean_id]

    def remove_student(self, student_id: str, auto_save: bool = True) -> Student:
        """
        Removes a student by ID and saves changes.

        Raises:
            StudentNotFoundError: If student is not found.
        """
        clean_id = student_id.strip().upper()
        if clean_id not in self._students:
            raise StudentNotFoundError(clean_id)

        removed = self._students.pop(clean_id)
        if auto_save:
            self.save()
        return removed

    def add_grade(self, student_id: str, course_code: str, score: float, auto_save: bool = True) -> Student:
        """
        Records a course grade for a student and persists updates.
        """
        student = self.get_student(student_id)
        student.add_grade(course_code, score)
        if auto_save:
            self.save()
        return student

    def update_student_info(
        self,
        student_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        enrollment_year: Optional[int] = None,
        auto_save: bool = True,
    ) -> Student:
        """Updates metadata for an existing student."""
        student = self.get_student(student_id)
        if name is not None:
            student.name = name
        if email is not None:
            student.email = email
        if enrollment_year is not None:
            student.enrollment_year = enrollment_year

        if auto_save:
            self.save()
        return student

    # --- Query & Search Operations ---

    def get_all_students(self) -> List[Student]:
        """Returns a list of all students sorted by student_id."""
        return sorted(self._students.values(), key=lambda s: s.student_id)

    def count(self) -> int:
        """Returns total number of students in the manager."""
        return len(self._students)

    def search(self, query: str) -> List[Student]:
        """
        Searches students by ID, Name, Email, or Thesis Title (case-insensitive).
        """
        clean_query = query.strip().lower()
        if not clean_query:
            return self.get_all_students()

        results: List[Student] = []
        for s in self._students.values():
            if (
                clean_query in s.student_id.lower()
                or clean_query in s.name.lower()
                or clean_query in s.email.lower()
            ):
                results.append(s)
            elif isinstance(s, GraduateStudent) and (
                clean_query in s.thesis_title.lower() or clean_query in s.advisor.lower()
            ):
                results.append(s)

        return sorted(results, key=lambda s: s.student_id)

    def filter_by_type(self, student_type: str) -> List[Student]:
        """
        Filters students by type ('undergraduate' or 'graduate').
        """
        target = student_type.strip().lower()
        if target == "graduate":
            return [s for s in self._students.values() if isinstance(s, GraduateStudent)]
        elif target == "undergraduate":
            return [s for s in self._students.values() if not isinstance(s, GraduateStudent)]
        raise ValueError("Invalid student_type. Choose 'undergraduate' or 'graduate'.")

    # --- Analytics & Reporting ---

    def calculate_class_average(self) -> float:
        """
        Calculates the aggregate average grade across all students who have grades.
        """
        students_with_grades = [s for s in self._students.values() if s.grades]
        if not students_with_grades:
            return 0.0

        total_sum = sum(s.calculate_average() for s in students_with_grades)
        return round(total_sum / len(students_with_grades), 2)

    def get_top_students(self, limit: int = 3) -> List[Student]:
        """
        Returns the top N performing students sorted by grade average in descending order.
        """
        students_with_grades = [s for s in self._students.values() if s.grades]
        sorted_students = sorted(
            students_with_grades,
            key=lambda s: s.calculate_average(),
            reverse=True,
        )
        return sorted_students[:limit]

    def generate_statistics(self) -> Dict[str, Any]:
        """
        Generates comprehensive academic analytics.
        """
        all_students = list(self._students.values())
        undergrads = [s for s in all_students if not isinstance(s, GraduateStudent)]
        grads = [s for s in all_students if isinstance(s, GraduateStudent)]
        graded_students = [s for s in all_students if s.grades]

        averages = [s.calculate_average() for s in graded_students]

        # Grade distribution breakdown
        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for s in graded_students:
            letter = s.get_letter_grade()
            if letter in distribution:
                distribution[letter] += 1

        pass_count = sum(1 for s in graded_students if s.get_letter_grade() in ("A", "B", "C", "D"))
        pass_rate = round((pass_count / len(graded_students) * 100), 1) if graded_students else 0.0

        return {
            "total_students": len(all_students),
            "undergraduate_count": len(undergrads),
            "graduate_count": len(grads),
            "graded_students_count": len(graded_students),
            "class_average": self.calculate_class_average(),
            "highest_average": max(averages) if averages else 0.0,
            "lowest_average": min(averages) if averages else 0.0,
            "pass_rate_percent": pass_rate,
            "grade_distribution": distribution,
        }

