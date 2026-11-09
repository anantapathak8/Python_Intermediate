"""
=============================================================================
Student Record Manager - CLI Application & Entry Point
=============================================================================

This module provides the main user interface for the Student Record Manager:
- Interactive console menu for all CRUD and analytics operations.
- Direct script execution and module execution (-m student_record_manager.main).
- Automated demo mode (--demo) for automated grading and unattended walkthroughs.
"""

import sys
from pathlib import Path

# Enable direct script execution by adding parent directory to sys.path if needed
if __package__ is None or __package__ == "":
    parent_dir = str(Path(__file__).resolve().parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from student_record_manager import (
    DuplicateStudentError,
    GraduateStudent,
    Student,
    StudentNotFoundError,
    StudentRecordError,
    StudentRecordManager,
    StudentStorage,
    ValidationError,
)


def print_banner() -> None:
    """Displays the welcome banner."""
    print("=" * 75)
    print("      ACADEMIC RECORD MANAGEMENT SYSTEM (Python Week 2 Showcase)      ")
    print("=" * 75)


def display_menu() -> None:
    """Displays interactive menu choices."""
    print("\nSelect an action:")
    print("  1. List All Students")
    print("  2. Add Undergraduate Student")
    print("  3. Add Graduate Student")
    print("  4. Search Student Records")
    print("  5. Add/Update Student Grade")
    print("  6. Remove Student Record")
    print("  7. View Class Analytics & Performance Report")
    print("  8. Run Automated System Walkthrough (Demo Mode)")
    print("  9. Exit")
    print("-" * 75)


def print_students_table(students: list[Student]) -> None:
    """Renders a formatted table of student records."""
    if not students:
        print("\n[!] No student records found.")
        return

    print("\n" + "=" * 90)
    print(f"{'ID':<10} {'Type':<12} {'Name':<22} {'Average':<10} {'Grade':<8} {'Status':<25}")
    print("-" * 90)
    for s in students:
        s_type = "Graduate" if isinstance(s, GraduateStudent) else "Undergrad"
        avg_str = f"{s.calculate_average():.1f}%" if s.grades else "N/A"
        print(f"{s.student_id:<10} {s_type:<12} {s.name:<22} {avg_str:<10} {s.get_letter_grade():<8} {s.get_status():<25}")
        if isinstance(s, GraduateStudent):
            print(f"   └── Thesis: '{s.thesis_title}' | Advisor: {s.advisor}")
    print("=" * 90)


def handle_list_all(manager: StudentRecordManager) -> None:
    """Action: Lists all registered students."""
    students = manager.get_all_students()
    print_students_table(students)
    print(f"Total enrolled: {len(students)} student(s)")


def handle_add_undergrad(manager: StudentRecordManager) -> None:
    """Action: Adds a new undergraduate student interactively."""
    print("\n--- Add New Undergraduate Student ---")
    try:
        sid = input("Enter Student ID (e.g., STU104): ").strip()
        name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        year_str = input("Enter Enrollment Year (e.g., 2024): ").strip()
        year = int(year_str)

        student = Student(student_id=sid, name=name, email=email, enrollment_year=year)
        manager.add_student(student)
        print(f"\n[+] Successfully registered undergraduate: {student.name} ({student.student_id})")
    except (ValidationError, DuplicateStudentError) as e:
        print(f"\n[ERROR] Failed to add student: {e}")
    except ValueError:
        print("\n[ERROR] Enrollment year must be a valid integer.")


def handle_add_graduate(manager: StudentRecordManager) -> None:
    """Action: Adds a new graduate student interactively."""
    print("\n--- Add New Graduate Student ---")
    try:
        sid = input("Enter Graduate Student ID (e.g., GRAD203): ").strip()
        name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        year_str = input("Enter Enrollment Year (e.g., 2024): ").strip()
        year = int(year_str)
        thesis = input("Enter Research Thesis Title: ").strip()
        advisor = input("Enter Faculty Advisor Name: ").strip()

        grad_student = GraduateStudent(
            student_id=sid,
            name=name,
            email=email,
            enrollment_year=year,
            thesis_title=thesis,
            advisor=advisor,
        )
        manager.add_student(grad_student)
        print(f"\n[+] Successfully registered graduate researcher: {grad_student.name} ({grad_student.student_id})")
    except (ValidationError, DuplicateStudentError) as e:
        print(f"\n[ERROR] Failed to add graduate student: {e}")
    except ValueError:
        print("\n[ERROR] Enrollment year must be a valid integer.")


def handle_search(manager: StudentRecordManager) -> None:
    """Action: Searches student records."""
    query = input("\nEnter search query (ID, Name, Email, or Thesis keyword): ").strip()
    results = manager.search(query)
    print(f"\nFound {len(results)} matching record(s) for '{query}':")
    print_students_table(results)


def handle_add_grade(manager: StudentRecordManager) -> None:
    """Action: Adds or updates a course grade for a student."""
    print("\n--- Add / Update Student Grade ---")
    sid = input("Enter Student ID: ").strip()
    try:
        student = manager.get_student(sid)
        print(f"Target Student: {student.name} (Current courses: {list(student.grades.keys())})")
        course = input("Enter Course Code (e.g., CS101): ").strip()
        score_str = input("Enter Score (0.0 - 100.0): ").strip()
        score = float(score_str)

        manager.add_grade(sid, course, score)
        print(f"\n[+] Grade recorded: {student.name} - {course.upper()} = {score:.1f}%")
        print(f"    New Average: {student.calculate_average():.1f}% ({student.get_letter_grade()})")
    except StudentNotFoundError as e:
        print(f"\n[ERROR] {e}")
    except (ValidationError, ValueError) as e:
        print(f"\n[ERROR] Invalid score input: {e}")


def handle_remove_student(manager: StudentRecordManager) -> None:
    """Action: Removes a student record."""
    sid = input("\nEnter Student ID to remove: ").strip()
    try:
        removed = manager.remove_student(sid)
        print(f"\n[-] Successfully removed student: {removed.name} ({removed.student_id})")
    except StudentNotFoundError as e:
        print(f"\n[ERROR] {e}")


def handle_view_statistics(manager: StudentRecordManager) -> None:
    """Action: Displays class-wide academic statistics and report."""
    stats = manager.generate_statistics()
    print("\n" + "=" * 60)
    print("               CLASS ACADEMIC PERFORMANCE REPORT             ")
    print("=" * 60)
    print(f"Total Enrolled Students : {stats['total_students']}")
    print(f"  - Undergraduate Count : {stats['undergraduate_count']}")
    print(f"  - Graduate Count      : {stats['graduate_count']}")
    print(f"  - Graded Students     : {stats['graded_students_count']}")
    print("-" * 60)
    print(f"Class-Wide Grade Mean   : {stats['class_average']:.2f}%")
    print(f"Highest Student Average : {stats['highest_average']:.2f}%")
    print(f"Lowest Student Average  : {stats['lowest_average']:.2f}%")
    print(f"Pass Rate               : {stats['pass_rate_percent']:.1f}%")
    print("-" * 60)
    print("Grade Distribution:")
    for grade, count in stats["grade_distribution"].items():
        bar = "#" * count
        print(f"  {grade}: {count:2d} {bar}")
    print("-" * 60)
    print("Top Performing Students:")
    top_students = manager.get_top_students(limit=3)
    for rank, s in enumerate(top_students, 1):
        print(f"  {rank}. {s.name} ({s.student_id}) - {s.calculate_average():.2f}% [{s.get_letter_grade()}]")
    print("=" * 60)


def run_demo_mode(manager: StudentRecordManager) -> None:
    """
    Automated demo performing end-to-end operations without user prompts.
    Ideal for testing, CI/CD, and project demonstrations.
    """
    print("\n" + "#" * 75)
    print("--- RUNNING AUTOMATED SYSTEM DEMONSTRATION ---")
    print("#" * 75)

    print("\nStep 1: Listing initial students from data/students.json:")
    handle_list_all(manager)

    print("\nStep 2: Performing search query for 'Eleanor':")
    results = manager.search("Eleanor")
    for r in results:
        print(f"  Found: {r.name} ({r.student_id}) - {r.get_status()}")

    print("\nStep 3: Calculating and displaying class statistics:")
    handle_view_statistics(manager)

    print("\nStep 4: Demonstrating polymorphism between Undergrad and Graduate:")
    for s in manager.get_all_students()[:3]:
        print(f"  {type(s).__name__:<16}: {s}")

    print("\n" + "#" * 75)
    print("--- DEMO COMPLETED SUCCESSFULLY ---")
    print("#" * 75 + "\n")


def main() -> None:
    """Main CLI execution loop."""
    print_banner()
    manager = StudentRecordManager()
    print(f"Storage loaded. Currently tracking {manager.count()} student record(s).")

    # If --demo flag is passed as CLI argument, run demo and exit
    if len(sys.argv) > 1 and "--demo" in sys.argv:
        run_demo_mode(manager)
        return

    while True:
        try:
            display_menu()
            choice = input("Enter choice (1-9): ").strip()
            if choice == "1":
                handle_list_all(manager)
            elif choice == "2":
                handle_add_undergrad(manager)
            elif choice == "3":
                handle_add_graduate(manager)
            elif choice == "4":
                handle_search(manager)
            elif choice == "5":
                handle_add_grade(manager)
            elif choice == "6":
                handle_remove_student(manager)
            elif choice == "7":
                handle_view_statistics(manager)
            elif choice == "8":
                run_demo_mode(manager)
            elif choice == "9":
                print("\nSaving and exiting. Thank you for using Student Record Manager!\n")
                break
            else:
                print("\n[!] Invalid selection. Please enter a number between 1 and 9.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation cancelled. Exiting cleanly.")
            break


if __name__ == "__main__":
    main()

