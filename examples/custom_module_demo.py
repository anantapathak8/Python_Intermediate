"""
=============================================================================
Example: Custom Module & Package Consumption Demo
=============================================================================

This script demonstrates how an external script or consumer application
imports and utilizes the 'student_record_manager' custom package.

Demonstrates:
1. Importing custom classes, functions, and exceptions from a local package.
2. Initializing domain objects (Student, GraduateStudent).
3. Utilizing business logic methods and properties.
4. Handling custom package exceptions (ValidationError, StudentNotFoundError).
5. Interacting with persistent JSON storage.
"""

import sys
import tempfile
from pathlib import Path

# Add project root directory to sys.path so student_record_manager can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from student_record_manager import (
    DuplicateStudentError,
    GraduateStudent,
    Student,
    StudentNotFoundError,
    StudentRecordManager,
    StudentStorage,
    ValidationError,
)


def run_custom_module_demo() -> None:
    """Demonstrates third-party usage of the student_record_manager package."""
    print("=" * 75)
    print("DEMO: Consuming 'student_record_manager' as an External Module")
    print("=" * 75)

    # 1. Using an isolated temporary storage instance for demonstration
    with tempfile.TemporaryDirectory() as temp_dir:
        demo_storage_path = Path(temp_dir) / "demo_students.json"
        storage = StudentStorage(file_path=demo_storage_path)
        manager = StudentRecordManager(storage=storage)
        print(f"\n[1] Initialized StudentRecordManager with isolated storage at:\n    {demo_storage_path}")

        # 2. Creating and Adding Undergraduate Students
        print("\n[2] Instantiating and adding undergraduate students...")
        s1 = Student(
            student_id="CS-101-01",
            name="Liam Neeson",
            email="liam.n@apex.edu",
            enrollment_year=2024,
        )
        s1.add_grade("CS101", 94.5)
        s1.add_grade("MATH101", 89.0)
        manager.add_student(s1)
        print(f"    Added: {s1}")

        # 3. Creating and Adding Graduate Students (Polymorphism)
        print("\n[3] Instantiating and adding a graduate researcher...")
        g1 = GraduateStudent(
            student_id="PHD-2024-09",
            name="Marie Curie",
            email="marie.curie@apex.edu",
            enrollment_year=2023,
            thesis_title="Advanced Radiation Sensing and Materials",
            advisor="Dr. Henri Becquerel",
        )
        g1.add_grade("PHYS701", 99.0)
        g1.add_grade("CHEM702", 97.5)
        manager.add_student(g1)
        print(f"    Added: {g1}")

        # 4. Property Validation and Exception Handling
        print("\n[4] Testing package validation & custom exception catching...")
        
        # Test A: Invalid Email
        try:
            print("    Attempting to create student with invalid email 'not-an-email'...")
            _ = Student("CS-102", "Invalid User", "not-an-email", 2024)
        except ValidationError as err:
            print(f"    [CAUGHT EXPECTED] ValidationError: {err}")

        # Test B: Invalid Grade range
        try:
            print("    Attempting to assign grade score 150.0 to Liam...")
            s1.add_grade("CS101", 150.0)
        except ValidationError as err:
            print(f"    [CAUGHT EXPECTED] ValidationError: {err}")

        # Test C: Duplicate Student ID
        try:
            print(f"    Attempting to register duplicate ID '{s1.student_id}'...")
            duplicate = Student("CS-101-01", "Imposter", "imposter@apex.edu", 2024)
            manager.add_student(duplicate)
        except DuplicateStudentError as err:
            print(f"    [CAUGHT EXPECTED] DuplicateStudentError: {err}")

        # Test D: Query non-existent student
        try:
            print("    Attempting lookup for non-existent ID 'GHOST-999'...")
            _ = manager.get_student("GHOST-999")
        except StudentNotFoundError as err:
            print(f"    [CAUGHT EXPECTED] StudentNotFoundError: {err}")

        # 5. Queries, Search, and Analytics
        print("\n[5] Querying manager records and calculating analytics...")
        all_students = manager.get_all_students()
        print(f"    Total registered: {len(all_students)}")
        for s in all_students:
            print(f"      - {s.student_id}: {s.name} ({type(s).__name__}) -> Avg: {s.calculate_average()}% [{s.get_letter_grade()}]")

        stats = manager.generate_statistics()
        print(f"\n    Class Mean:      {stats['class_average']:.2f}%")
        print(f"    Top Student:     {manager.get_top_students(1)[0].name}")

        # 6. Verifying Persistence
        print("\n[6] Verifying JSON file persistence on disk...")
        print(f"    File exists: {demo_storage_path.exists()}")
        print(f"    File size:   {demo_storage_path.stat().st_size} bytes")

        # Reload into a fresh manager instance from disk
        fresh_manager = StudentRecordManager(storage=storage)
        print(f"    Fresh manager loaded {fresh_manager.count()} records successfully from JSON.")

    print("\n" + "=" * 75)
    print("Example demonstration completed successfully!")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    run_custom_module_demo()

