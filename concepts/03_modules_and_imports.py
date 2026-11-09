"""
=============================================================================
Concept 03: Modules, Packages, and Imports in Python
=============================================================================

This module demonstrates:
1. Standard library imports (math, datetime, pathlib, sys, statistics).
2. Import syntax variants:
   - import <module>
   - from <module> import <item>
   - import <module> as <alias>
   - from <module> import <item> as <alias>
3. The module search mechanism: sys.path, sys.modules cache.
4. Module metadata: __name__, __file__, __doc__, __all__.
5. The critical role of the 'if __name__ == "__main__":' execution guard.
6. Clean API design and __all__ exports.
"""

# Standard Library Imports
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

# Module Alias Imports
import statistics as stats


# __all__ specifies the public API exported when `from module import *` is used
__all__ = [
    "calculate_letter_grade",
    "compute_statistics",
    "format_iso_timestamp",
    "inspect_module_environment",
]


# =============================================================================
# Modular Helper Functions (Exported Functions)
# =============================================================================

def calculate_letter_grade(percentage: float) -> str:
    """
    Converts a numerical percentage score (0-100) into an academic letter grade.
    
    Args:
        percentage: Score between 0 and 100
        
    Returns:
        Letter grade string: 'A', 'B', 'C', 'D', or 'F'
    """
    if not isinstance(percentage, (int, float)):
        raise TypeError(f"Score must be numeric, got {type(percentage).__name__}")
    if percentage < 0 or percentage > 100:
        raise ValueError(f"Score must be between 0 and 100, got {percentage}")

    if percentage >= 90.0:
        return "A"
    elif percentage >= 80.0:
        return "B"
    elif percentage >= 70.0:
        return "C"
    elif percentage >= 60.0:
        return "D"
    return "F"


def compute_statistics(numbers: List[float]) -> Dict[str, float]:
    """
    Calculates summary statistics using the standard library 'statistics' module.
    
    Demonstrates using module aliases (stats.mean, stats.stdev).
    """
    if not numbers:
        raise ValueError("Cannot calculate statistics for an empty list.")

    mean_val = stats.mean(numbers)
    median_val = stats.median(numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    # Stdev requires at least 2 data points
    stdev_val = stats.stdev(numbers) if len(numbers) > 1 else 0.0

    return {
        "count": float(len(numbers)),
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "std_dev": round(stdev_val, 2),
    }


def format_iso_timestamp(dt: datetime | None = None) -> str:
    """
    Formats a datetime object to an ISO 8601 string with UTC timezone.
    Demonstrates standard library datetime operations.
    """
    target = dt if dt is not None else datetime.now(timezone.utc)
    return target.isoformat()


def inspect_module_environment() -> Dict[str, object]:
    """
    Inspects module runtime information: __name__, sys.path, and loaded modules.
    """
    return {
        "current_module_name": __name__,
        "python_version": sys.version.split()[0],
        "total_sys_paths": len(sys.path),
        "is_main_module": __name__ == "__main__",
        "current_file": str(Path(__file__).resolve()) if "__file__" in globals() else "interactive",
    }


# =============================================================================
# Demonstration / Execution Guard
# =============================================================================

def demo_modules_and_imports() -> None:
    """
    Demonstrates standard library imports, aliases, and module execution guard.
    """
    print("=" * 70)
    print("DEMO: 03 - Modules, Packages, and Imports in Python")
    print("=" * 70)

    # 1. Using Standard Library Functions
    print("\n--- 1. Using Standard Library: math & statistics (aliased) ---")
    scores = [88.5, 92.0, 79.5, 95.0, 68.0, 84.0, 91.5]
    computed_stats = compute_statistics(scores)
    print(f"Dataset: {scores}")
    for k, v in computed_stats.items():
        print(f"  {k:10s}: {v}")

    # Standard math module demo
    hypot = math.hypot(3.0, 4.0)
    print(f"\nmath.hypot(3, 4) = {hypot} (Expected: 5.0)")
    print(f"math.pi rounded  = {round(math.pi, 4)}")

    # 2. Letter Grade Module Function
    print("\n--- 2. Modular Grade Conversion Function ---")
    sample_scores = [98.5, 83.0, 72.5, 61.0, 45.0]
    for s in sample_scores:
        grade = calculate_letter_grade(s)
        print(f"  Score: {s:5.1f}% -> Grade: {grade}")

    # 3. Datetime and Pathlib Usage
    print("\n--- 3. Standard Library datetime & pathlib ---")
    current_time_iso = format_iso_timestamp()
    print(f"ISO Timestamp (UTC): {current_time_iso}")

    current_script_path = Path(__file__).resolve()
    print(f"Pathlib resolved path: {current_script_path}")
    print(f"Parent directory:      {current_script_path.parent}")
    print(f"File exists:           {current_script_path.exists()}")

    # 4. Module Introspection and __name__
    print("\n--- 4. Module Introspection and __name__ Guard ---")
    env_info = inspect_module_environment()
    for key, value in env_info.items():
        print(f"  {key:22s}: {value}")

    print("\nExplanation of 'if __name__ == \"__main__\":'")
    print("  - When this script is run directly (python 03_modules_and_imports.py),")
    print("    Python sets __name__ = '__main__', triggering this demo.")
    print("  - When another script executes 'import 03_modules_and_imports',")
    print("    __name__ is set to the module name, suppressing demo side effects.")

    print("\n[OK] Concept 03 demonstration completed successfully.\n")


# Execution Guard
if __name__ == "__main__":
    demo_modules_and_imports()

