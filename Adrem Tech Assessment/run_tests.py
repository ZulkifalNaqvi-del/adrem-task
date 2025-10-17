#!/usr/bin/env python3
"""
Simple test runner script for E2E Checkout Flow automation
Usage: python run_tests.py
"""
import sys
import subprocess


def main():
    """Run the E2E test suite"""
    print("=" * 80)
    print("Starting E2E Checkout Flow Automation Test")
    print("=" * 80)
    
    # Run pytest with appropriate flags
    cmd = [
        "python", "-m", "pytest",
        "tests/test_05_complete_checkout_flow.py",
        "-v",
        "--html=reports/report.html",
        "--self-contained-html",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

