#!/usr/bin/env python3
"""
Simple test script without external dependencies
"""

import os
import sys
from pathlib import Path

def test_file_structure():
    """Test if all required files exist"""
    print("🔍 Testing file structure...")

    required_files = [
        'config.yml',
        'domain.yml',
        'data/nlu.yml',
        'data/stories.yml',
        'data/rules.yml',
        'actions/actions.py',
        'templates/index.html',
        'app.py',
        'requirements.txt',
        'endpoints.yml',
        'credentials.yml'
    ]

    missing_files = []
    existing_files = []

    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)

    print(f"✅ Found {len(existing_files)} files")
    if missing_files:
        print(f"❌ Missing {len(missing_files)} files: {missing_files}")
        return False

    print("✅ All required files found")
    return True

def test_python_syntax():
    """Test Python syntax for Python files"""
    print("\n🔍 Testing Python syntax...")

    python_files = [
        'app.py',
        'actions/actions.py',
        'run_chatbot.py'
    ]

    syntax_errors = []

    for python_file in python_files:
        try:
            with open(python_file, 'r') as f:
                code = f.read()
                compile(code, python_file, 'exec')
            print(f"✅ {python_file}")
        except SyntaxError as e:
            print(f"❌ {python_file} - Syntax Error: {e}")
            syntax_errors.append(python_file)
        except Exception as e:
            print(f"❌ {python_file} - Error: {e}")
            syntax_errors.append(python_file)

    if syntax_errors:
        print(f"❌ {len(syntax_errors)} files have syntax errors")
        return False

    print("✅ All Python files have valid syntax")
    return True

def test_html_structure():
    """Test HTML file has basic structure"""
    print("\n🔍 Testing HTML structure...")

    try:
        with open('templates/index.html', 'r') as f:
            html_content = f.read()

        required_elements = ['<!DOCTYPE html>', '<html', '<head>', '<body>', '<script']
        missing_elements = []

        for element in required_elements:
            if element not in html_content:
                missing_elements.append(element)

        if missing_elements:
            print(f"❌ Missing HTML elements: {missing_elements}")
            return False

        print("✅ HTML structure looks good")
        return True

    except Exception as e:
        print(f"❌ Error reading HTML: {e}")
        return False

def test_requirements():
    """Test requirements file"""
    print("\n🔍 Testing requirements...")

    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip()

        if not requirements:
            print("❌ Requirements file is empty")
            return False

        required_packages = ['rasa', 'flask']
        found_packages = []

        for package in required_packages:
            if package in requirements.lower():
                found_packages.append(package)

        if len(found_packages) < 2:
            print(f"❌ Missing required packages. Found: {found_packages}")
            return False

        print(f"✅ Requirements file has necessary packages: {found_packages}")
        return True

    except Exception as e:
        print(f"❌ Error reading requirements: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Solar Chatbot Tests")
    print("=" * 40)

    tests = [
        test_file_structure,
        test_python_syntax,
        test_html_structure,
        test_requirements
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your chatbot is ready to run.")
        print("\n📋 NEXT STEPS:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Train the model: rasa train")
        print("3. Start the chatbot: python run_chatbot.py")
        print("4. Choose option 4 for full setup")
        print("5. Open http://localhost:5000 in your browser")
        print("\n📚 For detailed instructions, see README.md")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()