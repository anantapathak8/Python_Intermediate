"""
=============================================================================
Concept 06: JSON Handling, Serialization, and Deserialization in Python
=============================================================================

This module demonstrates:
1. Difference between string and file operations:
   - json.dumps(): Serialize Python object to JSON formatted str.
   - json.loads(): Deserialize JSON formatted str to Python object.
   - json.dump():  Serialize Python object directly to an open file stream.
   - json.load():  Deserialize JSON data directly from an open file stream.
2. Serialization options: indent, sort_keys, ensure_ascii.
3. Custom Object Serialization:
   - Approach A: Custom JSONEncoder subclass.
   - Approach B: .to_dict() and .from_dict() model pattern.
   - Approach C: The 'default' callable argument.
4. Custom Object Deserialization via object_hook.
5. Handling non-standard types like datetime.
6. Error handling for malformed JSON using json.JSONDecodeError.
"""

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# =============================================================================
# Custom Domain Class for Serialization Demos
# =============================================================================

class AcademicCourse:
    """Represents a course to be serialized to and from JSON."""

    def __init__(self, code: str, name: str, credits: int, tags: List[str]) -> None:
        self.code = code
        self.name = name
        self.credits = credits
        self.tags = tags
        self.created_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convert object to JSON-serializable dictionary."""
        return {
            "code": self.code,
            "name": self.name,
            "credits": self.credits,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AcademicCourse":
        """Reconstruct an AcademicCourse instance from a dictionary."""
        instance = cls(
            code=data["code"],
            name=data["name"],
            credits=int(data["credits"]),
            tags=list(data.get("tags", [])),
        )
        if "created_at" in data:
            instance.created_at = datetime.fromisoformat(data["created_at"])
        return instance

    def __repr__(self) -> str:
        return f"AcademicCourse({self.code!r}, {self.name!r}, {self.credits}, tags={self.tags})"


class CustomCourseEncoder(json.JSONEncoder):
    """
    Subclasses json.JSONEncoder to teach Python how to serialize
    AcademicCourse instances and datetime objects.
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, AcademicCourse):
            return o.to_dict()
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


# =============================================================================
# Serialization & Deserialization Functions
# =============================================================================

def serialize_to_json_string(data: Any, indent: int = 2) -> str:
    """Serializes a Python object to a formatted JSON string (json.dumps)."""
    return json.dumps(data, indent=indent, sort_keys=True)


def parse_json_string(json_str: str) -> Any:
    """Parses a JSON string into Python data structures (json.loads)."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as err:
        raise ValueError(
            f"Invalid JSON at line {err.lineno}, column {err.colno}: {err.msg}"
        ) from err


def save_to_json_file(file_path: Path, data: Any, indent: int = 4) -> None:
    """Saves a Python object directly to a JSON file (json.dump)."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=str)


def load_from_json_file(file_path: Path) -> Any:
    """Loads and parses data directly from a JSON file (json.load)."""
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    with open(file_path, mode="r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as err:
            raise ValueError(
                f"Malformed JSON in {file_path.name} (line {err.lineno}, col {err.colno}): {err.msg}"
            ) from err


# =============================================================================
# Demonstration Runner
# =============================================================================

def demo_json_handling() -> None:
    """Demonstrates dumps, loads, dump, load, custom encoders, and error handling."""
    print("=" * 70)
    print("DEMO: 06 - JSON Handling, Serialization, & Deserialization in Python")
    print("=" * 70)

    # 1. In-Memory: json.dumps() and json.loads()
    print("\n--- 1. In-Memory String Operations (dumps & loads) ---")
    student_record = {
        "student_id": "STU-2026-001",
        "name": "Sophia Reynolds",
        "is_active": True,
        "gpa": 3.92,
        "enrolled_courses": ["CS101", "MATH201", "ENG105"],
        "advising_notes": None,
    }

    # Serialize to JSON string
    json_string = serialize_to_json_string(student_record, indent=2)
    print("Serialized JSON String:")
    print(json_string)

    # Deserialize back from JSON string
    deserialized = parse_json_string(json_string)
    print(f"\nDeserialized Python type: {type(deserialized).__name__}")
    print(f"Student name: {deserialized['name']}, Active: {deserialized['is_active']}")

    # 2. File-Based: json.dump() and json.load()
    print("\n--- 2. File-Based Operations (dump & load) ---")
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        target_file = temp_dir / "records.json"

        dataset = [
            {"id": 1, "title": "Data Structures", "credits": 4},
            {"id": 2, "title": "Operating Systems", "credits": 4},
            {"id": 3, "title": "Algorithms", "credits": 3},
        ]

        # Save to file
        save_to_json_file(target_file, dataset, indent=4)
        print(f"Successfully saved {len(dataset)} items to {target_file.name}")

        # Read back from file
        loaded_data = load_from_json_file(target_file)
        print(f"Loaded {len(loaded_data)} items back from file.")
        print(f"First item: {loaded_data[0]}")

    # 3. Custom Object Serialization via Custom Encoder & to_dict()
    print("\n--- 3. Custom Object Serialization ---")
    course = AcademicCourse("CS301", "Database Systems", 3, ["databases", "sql", "backend"])

    # Method A: Using .to_dict()
    course_dict = course.to_dict()
    serialized_a = json.dumps(course_dict, indent=2)
    print("Serialized via .to_dict():")
    print(serialized_a)

    # Method B: Using CustomCourseEncoder
    serialized_b = json.dumps(course, cls=CustomCourseEncoder, indent=2)
    print("\nSerialized via CustomCourseEncoder:")
    print(serialized_b)

    # Reconstructing object from JSON string
    parsed_course_dict = json.loads(serialized_b)
    reconstructed_course = AcademicCourse.from_dict(parsed_course_dict)
    print(f"\nReconstructed object: {repr(reconstructed_course)}")
    print(f"Reconstructed code: {reconstructed_course.code}, tags: {reconstructed_course.tags}")

    # 4. Error Handling: Malformed JSON
    print("\n--- 4. Handling json.JSONDecodeError ---")
    malformed_json = '{"name": "Alice", "age": 22, missing_closing_bracket: true'
    try:
        parse_json_string(malformed_json)
    except ValueError as err:
        print(f"Safely caught decode error:\n  {err}")

    print("\n[OK] Concept 06 demonstration completed successfully.\n")


if __name__ == "__main__":
    demo_json_handling()

