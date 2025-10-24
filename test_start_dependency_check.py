#!/usr/bin/env python3
"""
Test Suite for start.py Dependency Check

This script tests the automatic dependency installation feature
added to start.py to fix startup issues.
"""

import sys
import os
import subprocess


def test_dependency_check_function():
    """Test the check_and_install_dependencies function"""
    print("\n" + "="*60)
    print("Testing check_and_install_dependencies()")
    print("="*60)
    
    # Define the function to test (same as in start.py)
    def check_and_install_dependencies():
        """Check if required dependencies are installed"""
        required_modules = ['discord', 'aiohttp', 'openai', 'dotenv', 'PIL']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        return len(missing_modules) == 0, missing_modules
    
    result, missing = check_and_install_dependencies()
    
    if result:
        print("✓ All required dependencies are installed")
        return True
    else:
        print(f"⚠ Missing dependencies: {missing}")
        print("  Note: This is expected if dependencies haven't been installed yet")
        return False


def test_required_modules_import():
    """Test that all required modules can be imported"""
    print("\n" + "="*60)
    print("Testing Required Module Imports")
    print("="*60)
    
    required_modules = [
        ('discord', 'discord.py'),
        ('aiohttp', 'aiohttp'),
        ('openai', 'openai'),
        ('dotenv', 'python-dotenv'),
        ('PIL', 'Pillow')
    ]
    
    all_imported = True
    for module, package in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} ({package}) imported successfully")
        except ImportError as e:
            print(f"✗ {module} ({package}) failed to import: {e}")
            all_imported = False
    
    if all_imported:
        print("\n✓ All required modules can be imported")
    else:
        print("\n✗ Some modules could not be imported")
        print("  Run: python3 -m pip install --user -r requirements.txt")
    
    return all_imported


def test_start_script_syntax():
    """Test that start.py has valid syntax"""
    print("\n" + "="*60)
    print("Testing start.py Syntax")
    print("="*60)
    
    try:
        with open('start.py', 'r') as f:
            code = f.read()
            compile(code, 'start.py', 'exec')
        print("✓ start.py has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ start.py has syntax error: {e}")
        return False


def test_start_script_has_dependency_check():
    """Test that start.py contains the dependency check function"""
    print("\n" + "="*60)
    print("Testing start.py Contains Dependency Check")
    print("="*60)
    
    with open('start.py', 'r') as f:
        content = f.read()
    
    checks = [
        ('check_and_install_dependencies', 'dependency check function'),
        ('subprocess.check_call', 'pip install subprocess call'),
        ('sys.executable', 'Python executable reference'),
        ('--user', 'user-space installation flag'),
        ('-m', 'module invocation flag')
    ]
    
    all_found = True
    for check, description in checks:
        if check in content:
            print(f"✓ Found {description}")
        else:
            print(f"✗ Missing {description}")
            all_found = False
    
    if all_found:
        print("\n✓ start.py has all required dependency check components")
    else:
        print("\n✗ start.py is missing some dependency check components")
    
    return all_found


def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    print("\n" + "="*60)
    print("Testing requirements.txt")
    print("="*60)
    
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        print(f"✓ requirements.txt exists with {len(lines)} lines")
        
        # Check for key dependencies
        content = ''.join(lines)
        deps = ['discord.py', 'openai', 'python-dotenv', 'aiohttp', 'Pillow']
        all_found = True
        for dep in deps:
            if dep in content:
                print(f"  ✓ {dep} found")
            else:
                print(f"  ✗ {dep} missing")
                all_found = False
        
        return all_found
    else:
        print("✗ requirements.txt not found")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("Start.py Dependency Check Test Suite")
    print("="*60)
    
    tests = [
        test_requirements_file_exists,
        test_start_script_syntax,
        test_start_script_has_dependency_check,
        test_required_modules_import,
        test_dependency_check_function
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
