#!/usr/bin/env python3
"""
Automated test runner for the Flask application.
Runs unit and integration tests with coverage report.
"""

import subprocess
import sys

def run_tests():
    """Run pytest with coverage."""
    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=models",
        "--cov=routes",
        "--cov-report=html",
        "--cov-report=term",
        "tests/"
    ]

    result = subprocess.run(cmd, cwd=".")
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)