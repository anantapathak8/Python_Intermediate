"""
=============================================================================
Comprehensive Test Suite - Week 2 Intermediate Python Practice
=============================================================================

This test suite covers all Week 2 concepts and domain implementations:
1. Classes and Objects (concepts/01_classes_and_objects.py)
2. Inheritance and Encapsulation (concepts/02_inheritance_and_encapsulation.py)
3. Modules and Imports (concepts/03_modules_and_imports.py)
4. Exception Handling (concepts/04_exception_handling.py)
5. File Handling & Context Managers (concepts/05_file_handling.py)
6. JSON Handling & Serialization (concepts/06_json_handling.py)
7. Student Record Manager Package (student_record_manager)

Compatible with both 'unittest' (python test_week2.py) and 'pytest' (pytest test_week2.py).
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Dynamically import concept modules (handling numbered filenames)
def load_concept_module(filename: str, module_name: str):
    file_path = PROJECT_ROOT / "concepts" / filename
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


concept_01 = load_concept_module("01_classes_and_objects.py", "concept_01")
concept_02 = load_concept_module("02_inheritance_and_encapsulation.py", "concept_02")
concept_03 = load_concept_module("03_modules_and_imports.py", "concept_03")
concept_04 = load_concept_module("04_exception_handling.py", "concept_04")
concept_05 = load_concept_module("05_file_handling.py", "concept_05")
concept_06 = load_concept_module("06_json_handling.py", "concept_06")

# Import student_record_manager package
from student_record_manager import (
    DuplicateStudentError,
    GraduateStudent,
    StorageCorruptionError,
    StorageError,
    Student,
    StudentNotFoundError,
    StudentRecordError,
    StudentRecordManager,
    StudentStorage,
    ValidationError,
)


# =============================================================================
# 1. Tests for Concept 01: Classes and Objects
# =============================================================================

class TestClassesAndObjects(unittest.TestCase):
    """Tests class instantiation, attributes, methods, and dunder protocols."""

    def setUp(self) -> None:
        self.Course = concept_01.Course
        self.course = self.Course("CS101", "Intro to Programming", 3, "Dr. Hopper")

    def test_instance_attributes(self) -> None:
        self.assertEqual(self.course.course_code, "CS101")
        self.assertEqual(self.course.title, "Intro to Programming")
        self.assertEqual(self.course.credits, 3)
        self.assertEqual(self.course.instructor, "Dr. Hopper")
        self.assertEqual(self.course.enrolled_students, [])

    def test_enroll_and_drop_students(self) -> None:
        self.assertTrue(self.course.enroll_student("Ada"))
        self.assertEqual(self.course.get_enrollment_count(), 1)
        # Duplicate enrollment should return False
        self.assertFalse(self.course.enroll_student("Ada"))
        self.assertEqual(self.course.get_enrollment_count(), 1)

        # Drop student
        self.assertTrue(self.course.drop_student("Ada"))
        self.assertEqual(self.course.get_enrollment_count(), 0)
        self.assertFalse(self.course.drop_student("Ada"))

    def test_class_method_alternative_constructor(self) -> None:
        course = self.Course.from_string("BIO101, General Biology, 4, Dr. Mendel")
        self.assertEqual(course.course_code, "BIO101")
        self.assertEqual(course.credits, 4)
        self.assertEqual(course.instructor, "Dr. Mendel")

    def test_class_attribute_and_count(self) -> None:
        initial_count = self.Course.get_total_courses()
        _ = self.Course("TEST101", "Test Course", 1, "Staff")
        self.assertEqual(self.Course.get_total_courses(), initial_count + 1)
        self.assertEqual(self.course.university_name, "Apex Institute of Technology")

    def test_static_method_validation(self) -> None:
        self.assertTrue(self.Course.is_valid_course_code("CS101"))
        self.assertTrue(self.Course.is_valid_course_code("MATH201"))
        self.assertFalse(self.Course.is_valid_course_code("INVALID_CODE_123"))
        self.assertFalse(self.Course.is_valid_course_code("123CS"))

    def test_dunder_methods(self) -> None:
        str_repr = str(self.course)
        self.assertIn("CS101", str_repr)
        self.assertIn("Intro to Programming", str_repr)

        dev_repr = repr(self.course)
        self.assertIn("Course(course_code='CS101'", dev_repr)

        # Equality based on code
        same_code_course = self.Course("CS101", "Different Name", 4, "Someone Else")
        self.assertEqual(self.course, same_code_course)


# =============================================================================
# 2. Tests for Concept 02: Inheritance and Encapsulation
# =============================================================================

class TestInheritanceAndEncapsulation(unittest.TestCase):
    """Tests inheritance hierarchy, super(), encapsulation, and properties."""

    def setUp(self) -> None:
        self.Person = concept_02.Person
        self.Student = concept_02.Student
        self.Faculty = concept_02.Faculty

    def test_person_encapsulation_and_properties(self) -> None:
        person = self.Person("John Doe", "NAT-123456789", 1990)
        self.assertEqual(person.name, "John Doe")
        self.assertEqual(person.birth_year, 1990)
        self.assertEqual(person.age, 36)
        self.assertEqual(person.national_id_masked, "*********" + "6789")

        # Private attribute name mangling
        with self.assertRaises(AttributeError):
            _ = person.__birth_year  # type: ignore

    def test_student_inheritance_and_super(self) -> None:
        student = self.Student("Jane Smith", "NAT-987654321", 2002, "STU-500", "Physics")
        self.assertEqual(student.name, "Jane Smith")
        self.assertEqual(student.student_id, "STU-500")
        self.assertEqual(student.major, "Physics")
        self.assertEqual(student.gpa, 0.0)

        # Method overriding
        desc = student.get_role_description()
        self.assertIn("Jane Smith", desc)
        self.assertIn("STU-500", desc)
        self.assertIn("Physics", desc)

    def test_property_validation(self) -> None:
        student = self.Student("Jane Smith", "NAT-987654321", 2002, "STU-500", "Physics")
        student.gpa = 3.75
        self.assertEqual(student.gpa, 3.75)

        # Validation constraints
        with self.assertRaises(ValueError):
            student.gpa = 4.5
        with self.assertRaises(ValueError):
            student.gpa = -0.5
        with self.assertRaises(TypeError):
            student.gpa = "Not a number"  # type: ignore

    def test_polymorphism_and_isinstance(self) -> None:
        p = self.Person("Alex", "NAT-001", 1985)
        s = self.Student("Bob", "NAT-002", 2003, "S1", "Art")
        f = self.Faculty("Dr. Carol", "NAT-003", 1975, "Math", "Professor")

        self.assertTrue(isinstance(s, self.Person))
        self.assertTrue(isinstance(f, self.Person))
        self.assertTrue(issubclass(self.Student, self.Person))
        self.assertTrue(issubclass(self.Faculty, self.Person))

        # Uniform polymorphic call
        descriptions = [obj.get_role_description() for obj in [p, s, f]]
        self.assertEqual(len(descriptions), 3)


# =============================================================================
# 3. Tests for Concept 03: Modules and Imports
# =============================================================================

class TestModulesAndImports(unittest.TestCase):
    """Tests modular functions, aliases, and statistics utilities."""

    def test_letter_grade_conversion(self) -> None:
        fn = concept_03.calculate_letter_grade
        self.assertEqual(fn(95.0), "A")
        self.assertEqual(fn(85.0), "B")
        self.assertEqual(fn(75.0), "C")
        self.assertEqual(fn(65.0), "D")
        self.assertEqual(fn(55.0), "F")

        with self.assertRaises(ValueError):
            fn(105.0)
        with self.assertRaises(ValueError):
            fn(-5.0)
        with self.assertRaises(TypeError):
            fn("ninety")  # type: ignore

    def test_compute_statistics(self) -> None:
        fn = concept_03.compute_statistics
        data = [10.0, 20.0, 30.0, 40.0, 50.0]
        res = fn(data)
        self.assertEqual(res["count"], 5.0)
        self.assertEqual(res["mean"], 30.0)
        self.assertEqual(res["median"], 30.0)
        self.assertEqual(res["min"], 10.0)
        self.assertEqual(res["max"], 50.0)

    def test_empty_statistics_raises(self) -> None:
        with self.assertRaises(ValueError):
            concept_03.compute_statistics([])

    def test_inspect_module_environment(self) -> None:
        info = concept_03.inspect_module_environment()
        self.assertIn("python_version", info)
        self.assertIn("total_sys_paths", info)


# =============================================================================
# 4. Tests for Concept 04: Exception Handling
# =============================================================================

class TestExceptionHandling(unittest.TestCase):
    """Tests custom exceptions, try/except/else/finally, and chaining."""

    def test_custom_exception_hierarchy(self) -> None:
        self.assertTrue(issubclass(concept_04.InvalidScoreError, concept_04.StudentManagementError))
        self.assertTrue(issubclass(concept_04.StudentNotFoundError, concept_04.StudentManagementError))
        self.assertTrue(issubclass(concept_04.DuplicateStudentError, concept_04.StudentManagementError))
        self.assertTrue(issubclass(concept_04.StudentManagementError, Exception))

    def test_validate_and_parse_score_success(self) -> None:
        score = concept_04.validate_and_parse_score("92.5")
        self.assertEqual(score, 92.5)

    def test_validate_and_parse_score_failures(self) -> None:
        with self.assertRaises(concept_04.InvalidScoreError):
            concept_04.validate_and_parse_score(-10)

        with self.assertRaises(concept_04.InvalidScoreError):
            concept_04.validate_and_parse_score(150)

        # Exception chaining verification
        try:
            concept_04.validate_and_parse_score("invalid_str")
        except concept_04.InvalidScoreError as e:
            self.assertIsNotNone(e.__cause__)
            self.assertIsInstance(e.__cause__, ValueError)

    def test_calculate_average_safe(self) -> None:
        avg = concept_04.calculate_average_safe([80.0, 90.0, 100.0])
        self.assertEqual(avg, 90.0)

        # ZeroDivisionError caught safely
        zero_avg = concept_04.calculate_average_safe([])
        self.assertEqual(zero_avg, 0.0)


# =============================================================================
# 5. Tests for Concept 05: File Handling & Context Managers
# =============================================================================

class TestFileHandling(unittest.TestCase):
    """Tests file write, append, read, line streaming, and modes."""

    def test_file_lifecycle_in_tempdir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            test_file = temp_dir / "records.txt"

            # 1. Write
            chars = concept_05.write_text_file(test_file, "Line 1: Alpha\nLine 2: Beta\n")
            self.assertGreater(chars, 0)
            self.assertTrue(test_file.exists())

            # 2. Append
            concept_05.append_to_file(test_file, ["Line 3: Gamma", "Line 4: Delta\n"])

            # 3. Read entire file
            content = concept_05.read_entire_file(test_file)
            self.assertIn("Line 1: Alpha", content)
            self.assertIn("Line 4: Delta", content)

            # 4. Read lines list
            lines = concept_05.read_file_as_lines(test_file)
            self.assertEqual(len(lines), 4)
            self.assertEqual(lines[0], "Line 1: Alpha")
            self.assertEqual(lines[3], "Line 4: Delta")

            # 5. Stream line-by-line
            count = concept_05.stream_file_line_by_line(test_file)
            self.assertEqual(count, 4)

            # 6. Read-write mode
            updated = concept_05.demonstrate_read_write_mode(test_file)
            self.assertIn("[LOG ENTRY: Verification passed]", updated)

    def test_missing_file_raises_filenotfound(self) -> None:
        non_existent = Path("non_existent_folder_xyz/file_123.txt")
        with self.assertRaises(FileNotFoundError):
            concept_05.read_entire_file(non_existent)


# =============================================================================
# 6. Tests for Concept 06: JSON Handling & Serialization
# =============================================================================

class TestJsonHandling(unittest.TestCase):
    """Tests JSON dumps, loads, dump, load, encoders, and error handling."""

    def test_dumps_and_loads(self) -> None:
        data = {"id": 101, "course": "CS101", "active": True, "scores": [90, 85]}
        json_str = concept_06.serialize_to_json_string(data)
        self.assertIsInstance(json_str, str)
        self.assertIn('"course": "CS101"', json_str)

        deserialized = concept_06.parse_json_string(json_str)
        self.assertEqual(deserialized, data)

    def test_dump_and_load_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_str:
            file_path = Path(temp_dir_str) / "data.json"
            sample = [{"title": "Course A"}, {"title": "Course B"}]

            concept_06.save_to_json_file(file_path, sample)
            self.assertTrue(file_path.exists())

            loaded = concept_06.load_from_json_file(file_path)
            self.assertEqual(loaded, sample)

    def test_custom_object_serialization(self) -> None:
        course = concept_06.AcademicCourse("MATH101", "Calculus I", 4, ["math", "calculus"])
        
        # Test .to_dict()
        as_dict = course.to_dict()
        self.assertEqual(as_dict["code"], "MATH101")
        self.assertEqual(as_dict["credits"], 4)

        # Test CustomCourseEncoder
        json_str = json.dumps(course, cls=concept_06.CustomCourseEncoder)
        self.assertIn("MATH101", json_str)

        # Test from_dict
        reconstructed = concept_06.AcademicCourse.from_dict(as_dict)
        self.assertEqual(reconstructed.code, course.code)
        self.assertEqual(reconstructed.tags, course.tags)

    def test_malformed_json_raises_value_error(self) -> None:
        bad_json = '{"unclosed": "string'
        with self.assertRaises(ValueError):
            concept_06.parse_json_string(bad_json)


# =============================================================================
# 7. Tests for Student Record Manager Package
# =============================================================================

class TestStudentRecordManager(unittest.TestCase):
    """Tests domain entities, inheritance, persistence, and service layer."""

    def setUp(self) -> None:
        # Use isolated temporary storage for every test run
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test_students.json"
        self.storage = StudentStorage(file_path=self.test_file)
        self.manager = StudentRecordManager(storage=self.storage)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_student_validation(self) -> None:
        # Valid student
        s = Student("S001", "Franklin", "franklin@apex.edu", 2024)
        self.assertEqual(s.student_id, "S001")
        self.assertEqual(s.name, "Franklin")

        # Invalid ID (empty)
        with self.assertRaises(ValidationError):
            Student("", "Franklin", "franklin@apex.edu", 2024)

        # Invalid Email
        with self.assertRaises(ValidationError):
            Student("S002", "Franklin", "bad-email", 2024)

        # Invalid Year
        with self.assertRaises(ValidationError):
            Student("S003", "Franklin", "franklin@apex.edu", 1850)

    def test_student_grades_and_status(self) -> None:
        s = Student("S010", "Grace Hopper", "grace@apex.edu", 2023)
        self.assertEqual(s.calculate_average(), 0.0)
        self.assertEqual(s.get_letter_grade(), "N/A")

        s.add_grade("CS101", 95.0)
        s.add_grade("MATH201", 85.0)
        self.assertEqual(s.calculate_average(), 90.0)
        self.assertEqual(s.get_letter_grade(), "A")
        self.assertEqual(s.get_status(), "Good Standing")

        # Invalid grade validation
        with self.assertRaises(ValidationError):
            s.add_grade("CS101", 105.0)
        with self.assertRaises(ValidationError):
            s.add_grade("CS101", -5.0)

    def test_graduate_student_inheritance_and_polymorphism(self) -> None:
        grad = GraduateStudent(
            student_id="G100",
            name="Nikola Tesla",
            email="nikola@apex.edu",
            enrollment_year=2022,
            thesis_title="Wireless Power Transmission",
            advisor="Dr. Edison",
        )
        self.assertTrue(isinstance(grad, Student))
        self.assertEqual(grad.thesis_title, "Wireless Power Transmission")
        self.assertEqual(grad.advisor, "Dr. Edison")

        # Overridden letter grade: 65% is F for grad (undergrad would be D)
        grad.add_grade("EE701", 65.0)
        self.assertEqual(grad.get_letter_grade(), "F")
        self.assertEqual(grad.get_status(), "Academic Warning (Graduate Minimum 75% Not Met)")

        # Good standing at >= 75%
        grad.add_grade("EE701", 85.0)
        self.assertEqual(grad.get_letter_grade(), "B")
        self.assertEqual(grad.get_status(), "Good Standing (Graduate Research)")

    def test_serialization_and_deserialization(self) -> None:
        s = Student("S001", "Alice", "alice@apex.edu", 2024, {"CS101": 92.0})
        g = GraduateStudent("G001", "Bob", "bob@apex.edu", 2023, "Robotics AI", "Dr. Vance", {"CS701": 96.0})

        s_dict = s.to_dict()
        g_dict = g.to_dict()

        reconstructed_s = Student.from_dict(s_dict)
        reconstructed_g = Student.from_dict(g_dict)

        self.assertIsInstance(reconstructed_s, Student)
        self.assertNotIsInstance(reconstructed_s, GraduateStudent)
        self.assertIsInstance(reconstructed_g, GraduateStudent)
        self.assertEqual(reconstructed_g.thesis_title, "Robotics AI")

    def test_manager_crud_operations(self) -> None:
        s1 = Student("S101", "Diana Prince", "diana@apex.edu", 2024)
        self.manager.add_student(s1)
        self.assertEqual(self.manager.count(), 1)

        # Duplicate ID should raise DuplicateStudentError
        with self.assertRaises(DuplicateStudentError):
            self.manager.add_student(Student("S101", "Clone", "clone@apex.edu", 2024))

        # Retrieve student
        retrieved = self.manager.get_student("S101")
        self.assertEqual(retrieved.name, "Diana Prince")

        # Retrieve non-existent
        with self.assertRaises(StudentNotFoundError):
            self.manager.get_student("NON_EXISTENT")

        # Update student info
        self.manager.update_student_info("S101", name="Wonder Woman")
        self.assertEqual(self.manager.get_student("S101").name, "Wonder Woman")

        # Remove student
        removed = self.manager.remove_student("S101")
        self.assertEqual(removed.student_id, "S101")
        self.assertEqual(self.manager.count(), 0)

    def test_storage_persistence(self) -> None:
        s = Student("PERSIST_1", "Test Subject", "test@apex.edu", 2024, {"CS101": 88.0})
        self.manager.add_student(s)

        # Create brand new manager with the same storage file to test loading
        new_manager = StudentRecordManager(storage=StudentStorage(file_path=self.test_file))
        self.assertEqual(new_manager.count(), 1)
        loaded_student = new_manager.get_student("PERSIST_1")
        self.assertEqual(loaded_student.name, "Test Subject")
        self.assertEqual(loaded_student.calculate_average(), 88.0)

    def test_corrupt_storage_file_handling(self) -> None:
        # Write corrupted JSON to storage
        self.test_file.write_text("{corrupt: true", encoding="utf-8")
        corrupted_storage = StudentStorage(file_path=self.test_file)
        with self.assertRaises(StorageCorruptionError):
            corrupted_storage.load_all()

    def test_manager_analytics_and_statistics(self) -> None:
        s1 = Student("U1", "Student One", "s1@apex.edu", 2024, {"CS": 95.0})
        s2 = Student("U2", "Student Two", "s2@apex.edu", 2024, {"CS": 75.0})
        g1 = GraduateStudent("G1", "Grad One", "g1@apex.edu", 2023, "Thesis X", "Advisor Y", {"CS": 85.0})

        self.manager.add_student(s1)
        self.manager.add_student(s2)
        self.manager.add_student(g1)

        stats = self.manager.generate_statistics()
        self.assertEqual(stats["total_students"], 3)
        self.assertEqual(stats["undergraduate_count"], 2)
        self.assertEqual(stats["graduate_count"], 1)
        self.assertEqual(stats["class_average"], 85.0)
        self.assertEqual(stats["highest_average"], 95.0)
        self.assertEqual(stats["lowest_average"], 75.0)

        # Top students check
        top = self.manager.get_top_students(limit=2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].student_id, "U1")

        # Search check
        self.assertEqual(len(self.manager.search("Grad One")), 1)
        self.assertEqual(len(self.manager.search("Thesis X")), 1)


# =============================================================================
# Test Runner
# =============================================================================

def run_all_tests() -> bool:
    """Runs all test cases with a formatted text runner."""
    suite = unittest.TestLoader().loadTestsFromNames([
        "test_week2.TestClassesAndObjects",
        "test_week2.TestInheritanceAndEncapsulation",
        "test_week2.TestModulesAndImports",
        "test_week2.TestExceptionHandling",
        "test_week2.TestFileHandling",
        "test_week2.TestJsonHandling",
        "test_week2.TestStudentRecordManager",
    ])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
