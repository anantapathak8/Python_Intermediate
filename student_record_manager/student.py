"""
=============================================================================
Student Record Manager - Student Models (OOP, Inheritance, Encapsulation)
=============================================================================

This module defines the student entity hierarchy:
- Student (Base class): Encapsulates student data, grade tracking, GPA logic.
- GraduateStudent (Subclass): Extends Student with research attributes and
  overridden evaluation policies.
- Custom domain exceptions for validation and retrieval errors.
"""

import re
from typing import Any, Dict, List, Optional


# =============================================================================
# Custom Domain Exceptions
# =============================================================================

class StudentRecordError(Exception):
    """Base exception for the student record management system."""
    pass


class ValidationError(StudentRecordError):
    """Raised when an attribute fails validation constraints."""
    pass


class StudentNotFoundError(StudentRecordError):
    """Raised when a student cannot be found in the system."""
    def __init__(self, student_id: str) -> None:
        super().__init__(f"Student with ID '{student_id}' does not exist.")
        self.student_id = student_id


class DuplicateStudentError(StudentRecordError):
    """Raised when trying to register an ID that is already present."""
    def __init__(self, student_id: str) -> None:
        super().__init__(f"A student with ID '{student_id}' is already registered.")
        self.student_id = student_id


# =============================================================================
# Base Student Class
# =============================================================================

class Student:
    """
    Base class representing an undergraduate student.

    Demonstrates:
    - Encapsulated private/protected attributes.
    - Property getters and setters with validation.
    - Grade calculation and letter grade mapping.
    - JSON serialization and deserialization.
    """

    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        enrollment_year: int,
        grades: Optional[Dict[str, float]] = None,
    ) -> None:
        self.student_id = student_id
        self.name = name
        self.email = email
        self.enrollment_year = enrollment_year
        self._grades: Dict[str, float] = {}

        if grades:
            for course, score in grades.items():
                self.add_grade(course, score)

    # --- Properties with Validation (Encapsulation) ---

    @property
    def student_id(self) -> str:
        """Unique student identification string."""
        return self._student_id

    @student_id.setter
    def student_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Student ID must be a non-empty string.")
        self._student_id = value.strip().upper()

    @property
    def name(self) -> str:
        """Full name of the student."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 2:
            raise ValidationError("Student name must be at least 2 characters long.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        """Student academic email address."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str) or not self.EMAIL_REGEX.match(value.strip()):
            raise ValidationError(f"Invalid email address format: '{value}'")
        self._email = value.strip().lower()

    @property
    def enrollment_year(self) -> int:
        """Year the student matriculated."""
        return self._enrollment_year

    @enrollment_year.setter
    def enrollment_year(self, value: int) -> None:
        if not isinstance(value, int) or value < 1950 or value > 2030:
            raise ValidationError(f"Enrollment year must be an integer between 1950 and 2030, got {value}.")
        self._enrollment_year = value

    @property
    def grades(self) -> Dict[str, float]:
        """Returns a copy of grades to preserve encapsulation."""
        return dict(self._grades)

    # --- Academic Logic & Methods ---

    def add_grade(self, course_code: str, score: float) -> None:
        """
        Adds or updates a course grade.

        Args:
            course_code: Course code, e.g., 'CS101'
            score: Percentage grade [0.0 - 100.0]
        """
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValidationError("Course code must be a non-empty string.")
        if not isinstance(score, (int, float)):
            raise ValidationError(f"Grade score must be numeric, got {type(score).__name__}.")
        if score < 0.0 or score > 100.0:
            raise ValidationError(f"Grade score must be between 0.0 and 100.0, received {score}.")

        self._grades[course_code.strip().upper()] = round(float(score), 2)

    def calculate_average(self) -> float:
        """Calculates arithmetic mean of course grades. Returns 0.0 if no grades."""
        if not self._grades:
            return 0.0
        return round(sum(self._grades.values()) / len(self._grades), 2)

    def get_letter_grade(self) -> str:
        """Maps student average to standard undergraduate letter grade."""
        avg = self.calculate_average()
        if not self._grades:
            return "N/A"
        if avg >= 90.0:
            return "A"
        elif avg >= 80.0:
            return "B"
        elif avg >= 70.0:
            return "C"
        elif avg >= 60.0:
            return "D"
        return "F"

    def get_status(self) -> str:
        """Academic standing for undergraduate students."""
        if not self._grades:
            return "No Grades Recorded"
        avg = self.calculate_average()
        if avg >= 60.0:
            return "Good Standing"
        return "Academic Probation"

    # --- Serialization & Deserialization ---

    def to_dict(self) -> Dict[str, Any]:
        """Serializes instance data to a dictionary."""
        return {
            "type": "undergraduate",
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "enrollment_year": self.enrollment_year,
            "grades": self.grades,
            "average": self.calculate_average(),
            "letter_grade": self.get_letter_grade(),
            "status": self.get_status(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """
        Factory method to reconstruct a Student or GraduateStudent from dictionary.
        Demonstrates polymorphism in deserialization.
        """
        record_type = data.get("type", "undergraduate")
        if record_type == "graduate":
            return GraduateStudent(
                student_id=data["student_id"],
                name=data["name"],
                email=data["email"],
                enrollment_year=data["enrollment_year"],
                thesis_title=data.get("thesis_title", "Untitled Thesis"),
                advisor=data.get("advisor", "Unassigned"),
                grades=data.get("grades", {}),
            )
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            enrollment_year=data["enrollment_year"],
            grades=data.get("grades", {}),
        )

    # --- Dunder Methods ---

    def __str__(self) -> str:
        return (
            f"[{self.student_id}] {self.name} | Avg: {self.calculate_average():.1f}% "
            f"({self.get_letter_grade()}) - {self.get_status()}"
        )

    def __repr__(self) -> str:
        return (
            f"Student(id='{self.student_id}', name='{self.name}', "
            f"email='{self.email}', year={self.enrollment_year})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return False
        return self.student_id == other.student_id


# =============================================================================
# Derived GraduateStudent Class (Inheritance & Overriding)
# =============================================================================

class GraduateStudent(Student):
    """
    Subclass representing a postgraduate / master's / PhD student.

    Demonstrates:
    - super() constructor chaining.
    - Subclass-specific attributes (thesis_title, advisor).
    - Overridden academic standing policy (higher threshold for graduate courses).
    - Overridden serialization.
    """

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        enrollment_year: int,
        thesis_title: str,
        advisor: str,
        grades: Optional[Dict[str, float]] = None,
    ) -> None:
        super().__init__(
            student_id=student_id,
            name=name,
            email=email,
            enrollment_year=enrollment_year,
            grades=grades,
        )
        self.thesis_title = thesis_title
        self.advisor = advisor

    @property
    def thesis_title(self) -> str:
        """Research thesis title."""
        return self._thesis_title

    @thesis_title.setter
    def thesis_title(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Thesis title cannot be empty.")
        self._thesis_title = value.strip()

    @property
    def advisor(self) -> str:
        """Assigned faculty advisor."""
        return self._advisor

    @advisor.setter
    def advisor(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Advisor name cannot be empty.")
        self._advisor = value.strip()

    # --- Method Overriding ---

    def get_letter_grade(self) -> str:
        """
        Overridden graduate letter grade policy:
        Graduate courses require >= 70.0 to pass (no D grade awarded).
        """
        avg = self.calculate_average()
        if not self._grades:
            return "N/A"
        if avg >= 90.0:
            return "A"
        elif avg >= 80.0:
            return "B"
        elif avg >= 70.0:
            return "C"
        return "F"  # Anything below 70 is failing for graduate studies

    def get_status(self) -> str:
        """
        Overridden graduate status:
        Graduate students require an average of 75.0 or above for good standing.
        """
        if not self._grades:
            return "Research Candidacy (No Coursework)"
        avg = self.calculate_average()
        if avg >= 75.0:
            return "Good Standing (Graduate Research)"
        return "Academic Warning (Graduate Minimum 75% Not Met)"

    def to_dict(self) -> Dict[str, Any]:
        """Overridden to include graduate-specific research fields."""
        data = super().to_dict()
        data["type"] = "graduate"
        data["thesis_title"] = self.thesis_title
        data["advisor"] = self.advisor
        return data

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} | Thesis: '{self.thesis_title}' (Advisor: {self.advisor})"

    def __repr__(self) -> str:
        return (
            f"GraduateStudent(id='{self.student_id}', name='{self.name}', "
            f"thesis='{self.thesis_title}', advisor='{self.advisor}')"
        )

