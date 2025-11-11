#!/usr/bin/env python3

import subprocess
import sys

tests = [
    ("Chapter 4: Scanning", "test/test_chapter4_scanning.lox"),
    ("Chapter 6: Expressions", "test/test_chapter6_expressions.lox"),
    ("Chapter 7: Evaluation", "test/test_chapter7_evaluation.lox"),
    ("Chapter 8: Statements & State", "test/test_chapter8_statements.lox"),
    ("Chapter 9: Control Flow", "test/test_chapter9_control.lox"),
    ("Chapter 10: Functions", "test/test_chapter10_functions.lox"),
]


def run_test(name, file):
    print(f"\n{'=' * 60}")
    print(f"Testing: {name}")
    print('=' * 60)

    try:
        result = subprocess.run(
            ["python3", "lox.py", file],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {name} PASSED")
            return True
        else:
            print(result.stdout)
            if result.stderr:
                print("ERRORS:")
                print(result.stderr)
            print(f"❌ {name} FAILED")
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ {name} TIMED OUT")
        return False
    except Exception as e:
        print(f"❌ {name} ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("LOX INTERPRETER - TEST SUITE")
    print("Chapters 4-10")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, file in tests:
        if run_test(name, file):
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print('=' * 60)

    if failed == 0:
        print(" ALL TESTS PASSED! ")
        return 0
    else:
        print(f"❌  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())