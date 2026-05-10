"""Exercise grading engine using pytest."""

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any


class ExerciseGrader:
    """Grade exercises by running pytest against student code."""

    def __init__(self, timeout: float = 10.0):
        """Initialize grader.

        Args:
            timeout: Maximum test execution time
        """
        self.timeout = timeout

    def grade(self, student_code: str, test_code: str) -> Dict[str, Any]:
        """Grade student code by running tests.

        Args:
            student_code: Student's solution code
            test_code: Pytest test code

        Returns:
            Dictionary with results: {'passed': bool, 'score': int, 'output': str}
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            solution_file = tmpdir / "solution.py"
            solution_file.write_text(student_code)
            test_file = tmpdir / "test_solution.py"
            test_file.write_text(test_code)

            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", str(test_file), "-v"],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=str(tmpdir),
                )
                passed = result.returncode == 0
                return {
                    "passed": passed,
                    "score": 100 if passed else 0,
                    "output": result.stdout + result.stderr,
                }
            except subprocess.TimeoutExpired:
                return {"passed": False, "score": 0, "output": "Tests timed out"}
            except Exception as e:
                return {"passed": False, "score": 0, "output": str(e)}
