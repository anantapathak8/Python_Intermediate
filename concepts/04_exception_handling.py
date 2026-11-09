"""
=============================================================================
Concept 04: Exception Handling and Custom Exceptions in Python
=============================================================================

This module demonstrates:
1. try-except blocks: Catching specific standard exceptions.
2. Handling multiple exception types cleanly.
3. The 'else' block: Executing code only when no exceptions are raised.
4. The 'finally' block: Guaranteed cleanup execution regardless of outcome.
5. Raising exceptions intentionally with 'raise'.
6. Exception chaining using 'raise ... from ...'.
7. Defining a custom hierarchy of domain-specific exceptions.
"""

from typing import Dict, List, Optional


# =============================================================================
# Custom Exception Hierarchy
# =============================================================================

class StudentManagementError(Exception):
    """Base exception for all student management domain errors."""

    def __init__(self, message: str, error_code: str = "GENERIC_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


class InvalidScoreError(StudentManagementError):
    """Raised when a provided score or grade fails validation rules."""

    def __init__(self, score: object, reason: str) -> None:
        super().__init__(
            message=f"Invalid score '{score}': {reason}",
            error_code="INVALID_SCORE",
        )
        self.score = score
        self.reason = reason


class StudentNotFoundError(StudentManagementError):
    """Raised when looking up a student ID that does not exist."""

    def __init__(self, student_id: str) -> None:
        super().__init__(
            message=f"Student with ID '{student_id}' was not found.",
            error_code="STUDENT_NOT_FOUND",
        )
        self.student_id = student_id


class DuplicateStudentError(StudentManagementError):
    """Raised when attempting to add a student ID that already exists."""

    def __init__(self, student_id: str) -> None:
        super().__init__(
            message=f"Student with ID '{student_id}' already exists in the registry.",
            error_code="DUPLICATE_STUDENT",
        )
        self.student_id = student_id


# =============================================================================
# Business Logic Demonstrating Exception Handling
# =============================================================================

def validate_and_parse_score(raw_input: object) -> float:
    """
    Parses and validates a numerical grade.
    Demonstrates try / except / raise with custom exceptions and exception chaining.
    """
    try:
        score = float(raw_input)  # type: ignore
    except (ValueError, TypeError) as err:
        # Chain the original exception to preserve debugging context
        raise InvalidScoreError(raw_input, "Must be a numeric value or valid numeric string") from err

    if score < 0.0 or score > 100.0:
        raise InvalidScoreError(score, "Score must be strictly between 0.0 and 100.0")

    return round(score, 2)


def calculate_average_safe(scores: List[float]) -> float:
    """
    Demonstrates try, except, else, and finally blocks in a single workflow.
    """
    cleanup_executed = False
    result: Optional[float] = None

    print(f"\nEvaluating scores: {scores}")
    try:
        # Might raise ZeroDivisionError if scores is empty
        total = sum(scores)
        count = len(scores)
        result = total / count

    except ZeroDivisionError as e:
        print(f"  [EXCEPT] Caught ZeroDivisionError: Cannot divide by zero ({e})")
        result = 0.0

    except TypeError as e:
        print(f"  [EXCEPT] Caught TypeError: Non-numeric element in scores list ({e})")
        raise

    else:
        # Runs ONLY if no exception was raised in the try block
        print(f"  [ELSE] Calculation succeeded without errors! Average = {result:.2f}")

    finally:
        # ALWAYS runs, regardless of whether exceptions were raised or caught
        cleanup_executed = True
        print(f"  [FINALLY] Cleanup hook executed (cleanup_executed = {cleanup_executed})")

    return result


def find_student_record(registry: Dict[str, dict], student_id: str) -> dict:
    """
    Demonstrates KeyError catching and converting to domain-specific exception.
    """
    try:
        return registry[student_id]
    except KeyError:
        raise StudentNotFoundError(student_id)


# =============================================================================
# Demonstration Runner
# =============================================================================

def demo_exception_handling() -> None:
    """Demonstrates all exception handling patterns."""
    print("=" * 70)
    print("DEMO: 04 - Exception Handling & Custom Exceptions in Python")
    print("=" * 70)

    # 1. Custom Exceptions & Validation
    print("\n--- 1. Raising and Catching Custom Exceptions ---")
    test_scores = ["95.5", 88, -10, 105, "abc"]

    for item in test_scores:
        try:
            valid_score = validate_and_parse_score(item)
            print(f"  Success: '{item}' parsed as {valid_score}")
        except InvalidScoreError as err:
            print(f"  Caught {err.__class__.__name__}: {err} (Code: {err.error_code})")
            if err.__cause__:
                print(f"    Caused by underlying: {repr(err.__cause__)}")

    # 2. Comprehensive try / except / else / finally
    print("\n--- 2. Complete try / except / else / finally Workflow ---")
    
    # Case A: Successful execution (triggers try -> else -> finally)
    print("Case A: Valid list")
    avg_a = calculate_average_safe([85.0, 90.0, 95.0])
    print(f"  Returned: {avg_a}")

    # Case B: Zero division error (triggers try -> except -> finally)
    print("\nCase B: Empty list (Division by zero)")
    avg_b = calculate_average_safe([])
    print(f"  Returned: {avg_b}")

    # 3. Domain Exceptions with Dictionary Lookup
    print("\n--- 3. Lookup with Domain-Specific StudentNotFoundError ---")
    students_db = {
        "S001": {"name": "Alice Cooper", "gpa": 3.9},
        "S002": {"name": "Bob Dylan", "gpa": 3.4},
    }

    search_ids = ["S001", "S999"]
    for sid in search_ids:
        try:
            record = find_student_record(students_db, sid)
            print(f"  Found ID {sid}: {record['name']} (GPA: {record['gpa']})")
        except StudentNotFoundError as e:
            print(f"  Error: {e} (Target ID: {e.student_id})")

    # 4. Exception Hierarchy Check
    print("\n--- 4. Checking Custom Exception Hierarchy ---")
    print(f"issubclass(InvalidScoreError, StudentManagementError): {issubclass(InvalidScoreError, StudentManagementError)}")
    print(f"issubclass(InvalidScoreError, Exception):              {issubclass(InvalidScoreError, Exception)}")
    print(f"issubclass(StudentNotFoundError, Exception):           {issubclass(StudentNotFoundError, Exception)}")

    print("\n[OK] Concept 04 demonstration completed successfully.\n")


if __name__ == "__main__":
    demo_exception_handling()

