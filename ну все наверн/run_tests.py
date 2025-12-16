#!/usr/bin/env python3
"""
Test runner script for the Flask application.

This script runs all unit and integration tests using pytest.
"""

import subprocess
import sys

def run_tests():
    """Run pytest on the tests directory."""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'tests/',
            '-v',
            '--tb=short'
        ], capture_output=True, text=True)

        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == '__main__':
    print("Running tests...")
    success = run_tests()
    sys.exit(0 if success else 1)