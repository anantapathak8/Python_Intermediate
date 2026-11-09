"""
=============================================================================
Concept 02: Inheritance and Encapsulation in Python
=============================================================================

This module demonstrates:
1. Inheritance: Reusing and extending base class behavior.
2. super(): Calling parent class methods from derived classes.
3. Method Overriding: Replacing parent implementations with subclass logic.
4. Polymorphism: Interacting with different classes via a uniform interface.
5. Encapsulation & Access Conventions:
   - Public attributes (accessible everywhere: self.name)
   - Protected attributes (internal by convention: self._id)
   - Private attributes (name-mangled: self.__salary)
6. Managed Attributes using Properties (@property, @<name>.setter).
7. Type hierarchy introspection (isinstance, issubclass).
"""

from typing import List


class Person:
    """
    Base class representing a general person in an educational institution.
    
    Demonstrates:
    - Public, protected, and private attributes.
    - Properties with validation.
    """

    def __init__(self, name: str, national_id: str, birth_year: int) -> None:
        # Public attribute: freely accessible and mutable
        self.name: str = name

        # Protected attribute (convention: single leading underscore)
        # Signifies internal use within class and subclasses
        self._national_id: str = national_id

        # Private attribute (two leading underscores)
        # Subject to name mangling (_Person__birth_year) to prevent accidental collisions
        if birth_year < 1900 or birth_year > 2026:
            raise ValueError(f"Invalid birth year: {birth_year}")
        self.__birth_year: int = birth_year

    # --- Property Getter and Setter for managed access ---
    @property
    def birth_year(self) -> int:
        """Getter for private birth_year attribute."""
        return self.__birth_year

    @property
    def age(self) -> int:
        """Computed property derived from birth_year."""
        current_year = 2026
        return current_year - self.__birth_year

    @property
    def national_id_masked(self) -> str:
        """Returns masked ID (e.g. '***-**-6789') for privacy protection."""
        if len(self._national_id) >= 4:
            return "*" * (len(self._national_id) - 4) + self._national_id[-4:]
        return "****"

    def get_role_description(self) -> str:
        """Base method to be overridden by subclasses."""
        return f"Person: {self.name} (Age: {self.age})"

    def __str__(self) -> str:
        return f"{self.name} [ID: {self.national_id_masked}]"


class Student(Person):
    """
    Derived class inheriting from Person.
    
    Demonstrates:
    - super().__init__() invocation.
    - Adding subclass-specific attributes.
    - Property getters and setters with data validation.
    - Method overriding.
    """

    def __init__(self, name: str, national_id: str, birth_year: int, student_id: str, major: str) -> None:
        # Delegate initialization of common person attributes to the parent class
        super().__init__(name=name, national_id=national_id, birth_year=birth_year)
        
        self.student_id: str = student_id
        self.major: str = major
        self._gpa: float = 0.0  # Protected attribute managed via property

    # --- Property getter and setter with strict validation ---
    @property
    def gpa(self) -> float:
        """Getter for student's Grade Point Average."""
        return self._gpa

    @gpa.setter
    def gpa(self, value: float) -> None:
        """Setter ensuring GPA remains within academic scale [0.0, 4.0]."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"GPA must be a numeric value, got {type(value).__name__}")
        if value < 0.0 or value > 4.0:
            raise ValueError(f"GPA must be between 0.0 and 4.0, received: {value}")
        self._gpa = round(float(value), 2)

    # --- Method Overriding ---
    def get_role_description(self) -> str:
        """Overrides Person.get_role_description with Student specific details."""
        base_desc = super().get_role_description()
        return f"{base_desc} | Role: Student [{self.student_id}], Major: {self.major}, GPA: {self.gpa:.2f}"


class Faculty(Person):
    """
    Another derived class inheriting from Person.
    Demonstrates polymorphism alongside Student.
    """

    def __init__(self, name: str, national_id: str, birth_year: int, department: str, title: str) -> None:
        super().__init__(name=name, national_id=national_id, birth_year=birth_year)
        self.department: str = department
        self.title: str = title
        self.__salary: float = 0.0  # Private attribute

    def set_salary(self, amount: float, auth_key: str) -> bool:
        """Encapsulated method controlling access to private salary data."""
        if auth_key == "ADMIN_KEY":
            if amount < 0:
                raise ValueError("Salary cannot be negative.")
            self.__salary = amount
            return True
        return False

    def get_salary_band(self) -> str:
        """Exposes broad salary category without disclosing exact amount."""
        if self.__salary < 60000:
            return "Band A"
        elif self.__salary < 100000:
            return "Band B"
        return "Band C"

    # --- Method Overriding ---
    def get_role_description(self) -> str:
        """Overrides Person.get_role_description for Faculty."""
        return f"Faculty: {self.title} {self.name} | Dept: {self.department} (Age: {self.age})"


def demo_inheritance_and_encapsulation() -> None:
    """Demonstrates inheritance, super(), overriding, encapsulation, and properties."""
    print("=" * 70)
    print("DEMO: 02 - Inheritance and Encapsulation in Python")
    print("=" * 70)

    # 1. Base Class Creation
    print("\n--- 1. Base Class and Encapsulation ---")
    person = Person("Alex Morgan", "NAT-987654321", 1995)
    print(f"Base Person: {person}")
    print(f"Name (Public):           {person.name}")
    print(f"National ID (Protected): {person._national_id}")
    print(f"Masked ID (Property):    {person.national_id_masked}")
    print(f"Age (Calculated Prop):   {person.age}")

    # Inspecting private attribute name-mangling
    print("\nTesting private attribute access:")
    try:
        # Direct access to __birth_year will fail
        _ = person.__birth_year  # type: ignore
    except AttributeError as err:
        print(f"Direct access person.__birth_year raises: {err}")
    
    # Access via name mangling (demonstration only; not recommended practice)
    mangled_value = getattr(person, "_Person__birth_year")
    print(f"Mangled access person._Person__birth_year: {mangled_value}")

    # 2. Derived Class with super() and Method Overriding
    print("\n--- 2. Derived Class (Student) & super() ---")
    student = Student("Maya Patel", "NAT-112233445", 2003, "STU-1001", "Computer Science")
    print(f"Initial description: {student.get_role_description()}")

    # 3. Property Setter with Validation
    print("\n--- 3. Property Validation ---")
    student.gpa = 3.85
    print(f"Updated GPA: {student.gpa}")
    try:
        student.gpa = 4.5  # Invalid GPA!
    except ValueError as e:
        print(f"Validation caught invalid GPA: {e}")

    try:
        student.gpa = "High"  # type: ignore # Non-numeric!
    except TypeError as e:
        print(f"Validation caught non-numeric GPA: {e}")

    # 4. Polymorphism Demonstration
    print("\n--- 4. Polymorphism Across Subclasses ---")
    faculty = Faculty("Dr. Eleanor Vance", "NAT-556677889", 1980, "Robotics", "Professor")
    faculty.set_salary(95000, "ADMIN_KEY")

    community_members: List[Person] = [person, student, faculty]
    for member in community_members:
        # Uniform call to get_role_description works polymorphicly across Person, Student, Faculty
        print(f"-> {member.get_role_description()}")

    # 5. Type and Subclass Hierarchy Introspection
    print("\n--- 5. Type and Subclass Checking ---")
    print(f"isinstance(student, Student):  {isinstance(student, Student)}")
    print(f"isinstance(student, Person):   {isinstance(student, Person)}")
    print(f"isinstance(faculty, Student):  {isinstance(faculty, Student)}")
    print(f"issubclass(Student, Person):   {issubclass(Student, Person)}")
    print(f"issubclass(Faculty, Person):   {issubclass(Faculty, Person)}")

    print("\n[OK] Concept 02 demonstration completed successfully.\n")


if __name__ == "__main__":
    demo_inheritance_and_encapsulation()

