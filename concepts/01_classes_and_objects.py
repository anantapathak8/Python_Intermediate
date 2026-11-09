"""
=============================================================================
Concept 01: Classes and Objects (Object-Oriented Programming Fundamentals)
=============================================================================

This module demonstrates the core building blocks of Object-Oriented
Programming in Python:
1. Class definition and Object instantiation.
2. Initializer / Constructor (__init__).
3. Instance attributes vs. Class attributes.
4. Instance methods, Class methods (@classmethod), and Static methods (@staticmethod).
5. Special / Dunder methods (__str__, __repr__, __eq__).
6. Object identity and introspection.
"""

from typing import List, Optional


class Course:
    """
    Demonstrates class attributes, instance attributes, methods, and dunder methods.
    
    Class Attributes:
        total_courses_created (int): Tracks the total instances created across the application.
        university_name (str): Shared attribute across all Course instances.
    """

    # --- Class Attributes (shared by all instances) ---
    university_name: str = "Apex Institute of Technology"
    total_courses_created: int = 0
    _course_registry: List["Course"] = []

    def __init__(self, course_code: str, title: str, credits: int, instructor: str) -> None:
        """
        Initializer (constructor) for Course instances.
        
        Args:
            course_code: Unique code, e.g., 'CS101'
            title: Course title, e.g., 'Data Structures'
            credits: Credit hours, e.g., 3
            instructor: Name of instructor
        """
        # --- Instance Attributes (unique to each instance) ---
        self.course_code: str = course_code.upper().strip()
        self.title: str = title.strip()
        self.credits: int = credits
        self.instructor: str = instructor.strip()
        self.enrolled_students: List[str] = []

        # Update class-level state
        Course.total_courses_created += 1
        Course._course_registry.append(self)

    # --- Instance Methods (operate on self / instance state) ---
    def enroll_student(self, student_name: str) -> bool:
        """Enrolls a student if not already enrolled."""
        cleaned_name = student_name.strip()
        if not cleaned_name:
            raise ValueError("Student name cannot be empty.")
        if cleaned_name in self.enrolled_students:
            return False  # Already enrolled
        self.enrolled_students.append(cleaned_name)
        return True

    def drop_student(self, student_name: str) -> bool:
        """Drops a student if present in enrollment."""
        cleaned_name = student_name.strip()
        if cleaned_name in self.enrolled_students:
            self.enrolled_students.remove(cleaned_name)
            return True
        return False

    def get_enrollment_count(self) -> int:
        """Returns the number of enrolled students."""
        return len(self.enrolled_students)

    def get_summary(self) -> str:
        """Returns a formatted summary of the course."""
        return (
            f"[{self.course_code}] {self.title} ({self.credits} Credits) "
            f"- Instructor: {self.instructor} | Enrolled: {self.get_enrollment_count()}"
        )

    # --- Class Methods (operate on cls / class state) ---
    @classmethod
    def from_string(cls, course_csv: str) -> "Course":
        """
        Alternative constructor (Factory method) creating a Course from a CSV string.
        Format: 'CODE,TITLE,CREDITS,INSTRUCTOR'
        """
        parts = [p.strip() for p in course_csv.split(",")]
        if len(parts) != 4:
            raise ValueError(f"Expected 4 comma-separated values, got {len(parts)}: '{course_csv}'")
        code, title, credits_str, instructor = parts
        return cls(
            course_code=code,
            title=title,
            credits=int(credits_str),
            instructor=instructor,
        )

    @classmethod
    def get_total_courses(cls) -> int:
        """Returns the total number of courses instantiated."""
        return cls.total_courses_created

    @classmethod
    def find_by_code(cls, code: str) -> Optional["Course"]:
        """Search the class registry for a course by its code."""
        code_upper = code.upper().strip()
        for course in cls._course_registry:
            if course.course_code == code_upper:
                return course
        return None

    # --- Static Methods (independent utility functions bound to the class namespace) ---
    @staticmethod
    def is_valid_course_code(code: str) -> bool:
        """
        Validates if a course code matches standard format (2-4 letters followed by 3 digits).
        E.g., 'CS101', 'MATH201', 'ENG102'.
        """
        if not isinstance(code, str):
            return False
        code = code.strip()
        if len(code) < 5 or len(code) > 7:
            return False
        letters = "".join(ch for ch in code if ch.isalpha())
        digits = "".join(ch for ch in code if ch.isdigit())
        return len(letters) in (2, 3, 4) and len(digits) == 3 and (letters + digits == code)

    # --- Special / Dunder Methods ---
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.course_code}: {self.title} ({self.credits} cr)"

    def __repr__(self) -> str:
        """Unambiguous developer representation (can ideally reconstruct the object)."""
        return (
            f"Course(course_code='{self.course_code}', title='{self.title}', "
            f"credits={self.credits}, instructor='{self.instructor}')"
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on course_code."""
        if not isinstance(other, Course):
            return False
        return self.course_code == other.course_code


def demo_classes_and_objects() -> None:
    """Demonstrates all features of Course class in action."""
    print("=" * 70)
    print("DEMO: 01 - Classes and Objects in Python")
    print("=" * 70)

    # 1. Instantiation and Instance Attributes
    print("\n--- 1. Creating Instances ---")
    cs101 = Course("CS101", "Introduction to Computer Science", 4, "Dr. Ada Lovelace")
    math201 = Course("MATH201", "Calculus & Linear Algebra", 3, "Dr. Alan Turing")
    print(f"Created instance 1: {cs101}")
    print(f"Created instance 2: {math201}")

    # 2. Class Attributes
    print("\n--- 2. Class Attributes vs Instance Attributes ---")
    print(f"cs101.university_name:       {cs101.university_name}")
    print(f"math201.university_name:     {math201.university_name}")
    print(f"Course.university_name:      {Course.university_name}")
    print(f"Total courses created so far: {Course.get_total_courses()}")

    # 3. Instance Methods
    print("\n--- 3. Calling Instance Methods ---")
    cs101.enroll_student("Alice Johnson")
    cs101.enroll_student("Bob Smith")
    cs101.enroll_student("Charlie Brown")
    print(f"Enrolled in CS101: {cs101.enrolled_students}")
    print(f"Enrollment count: {cs101.get_enrollment_count()}")
    print(f"Course summary:   {cs101.get_summary()}")

    # 4. Class Method (Alternative Constructor)
    print("\n--- 4. Class Method / Factory Constructor ---")
    phys101 = Course.from_string("PHYS101, Classical Mechanics, 4, Dr. Isaac Newton")
    print(f"Constructed via from_string: {repr(phys101)}")
    print(f"Total courses now: {Course.get_total_courses()}")

    # 5. Static Method
    print("\n--- 5. Static Method Validation ---")
    test_codes = ["CS101", "MATH201", "INVALID_CODE", "123CS", "BIO100"]
    for code in test_codes:
        valid = Course.is_valid_course_code(code)
        print(f"Code '{code}': {'Valid' if valid else 'Invalid'}")

    # 6. Dunder Methods & Object Identity
    print("\n--- 6. Dunder Methods (__str__, __repr__, __eq__) ---")
    print(f"str(cs101):  {str(cs101)}")
    print(f"repr(cs101): {repr(cs101)}")
    
    # Equality check
    duplicate_cs101 = Course("CS101", "Different Title", 1, "Different Instructor")
    print(f"cs101 == duplicate_cs101 (same course code): {cs101 == duplicate_cs101}")
    print(f"cs101 is duplicate_cs101 (identity check):    {cs101 is duplicate_cs101}")

    print("\n[OK] Concept 01 demonstration completed successfully.\n")


if __name__ == "__main__":
    demo_classes_and_objects()

