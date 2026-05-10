"""Safe code execution engine for PyTeach."""

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Tuple, Optional


class CodeRunner:
    """Safely execute Python code snippets with resource limits."""

    def __init__(self, timeout: float = 5.0, max_output: int = 10000):
        """Initialize the runner.

        Args:
            timeout: Maximum execution time in seconds
            max_output: Maximum output characters to capture
        """
        self.timeout = timeout
        self.max_output = max_output

    def run(self, code: str) -> Tuple[int, str, str]:
        """Execute code and return (exit_code, stdout, stderr).

        Args:
            code: Python code to execute

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            return result.returncode, result.stdout[: self.max_output], result.stderr[: self.max_output]
        except subprocess.TimeoutExpired:
            return 1, "", "Execution timed out (exceeded 5 seconds)"
        except Exception as e:
            return 1, "", str(e)
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def run_with_imports(self, code: str, imports: Optional[list] = None) -> Tuple[int, str, str]:
        """Run code with predefined imports.

        Args:
            code: Python code to execute
            imports: List of import statements to prepend

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        full_code = ""
        if imports:
            full_code = "\n".join(imports) + "\n\n"
        full_code += code
        return self.run(full_code)
