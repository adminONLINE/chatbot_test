#!/usr/bin/env python3
"""
Simple test script to verify the chatbot configuration
"""

import os
import yaml
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
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False

    print("✅ All required files found")
    return True

def test_yaml_syntax():
    """Test YAML syntax for configuration files"""
    print("\n🔍 Testing YAML syntax...")

    yaml_files = [
        'config.yml',
        'domain.yml',
        'data/nlu.yml',
        'data/stories.yml',
        'data/rules.yml',
        'endpoints.yml',
        'credentials.yml'
    ]

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {yaml_file} - Valid YAML")
        except yaml.YAMLError as e:
            print(f"❌ {yaml_file} - YAML Error: {e}")
            return False
        except Exception as e:
            print(f"❌ {yaml_file} - Error: {e}")
            return False

    return True

def test_python_syntax():
    """Test Python syntax for Python files"""
    print("\n🔍 Testing Python syntax...")

    python_files = [
        'app.py',
        'actions/actions.py',
        'run_chatbot.py'
    ]

    for python_file in python_files:
        try:
            with open(python_file, 'r') as f:
                compile(f.read(), python_file, 'exec')
            print(f"✅ {python_file} - Valid Python")
        except SyntaxError as e:
            print(f"❌ {python_file} - Syntax Error: {e}")
            return False
        except Exception as e:
            print(f"❌ {python_file} - Error: {e}")
            return False

    return True

def test_domain_intents():
    """Test if domain has required intents"""
    print("\n🔍 Testing domain configuration...")

    try:
        with open('domain.yml', 'r') as f:
            domain = yaml.safe_load(f)

        required_intents = [
            'greet', 'goodbye', 'request_selling',
            'request_information', 'ask_price', 'ask_benefits'
        ]

        domain_intents = domain.get('intents', [])
        missing_intents = []

        for intent in required_intents:
            if intent not in domain_intents:
                missing_intents.append(intent)

        if missing_intents:
            print(f"❌ Missing intents: {missing_intents}")
            return False

        print(f"✅ Domain has {len(domain_intents)} intents")
        print(f"✅ Required intents present")
        return True

    except Exception as e:
        print(f"❌ Error reading domain: {e}")
        return False

def test_nlu_data():
    """Test NLU training data"""
    print("\n🔍 Testing NLU data...")

    try:
        with open('data/nlu.yml', 'r') as f:
            nlu_data = yaml.safe_load(f)

        nlu_intents = nlu_data.get('nlu', [])
        intent_count = len(nlu_intents)

        if intent_count == 0:
            print("❌ No intents found in NLU data")
            return False

        print(f"✅ NLU data has {intent_count} intents")

        # Check for examples
        total_examples = 0
        for intent_data in nlu_intents:
            examples = intent_data.get('examples', '')
            example_count = len(examples.split('\n')) if examples else 0
            total_examples += example_count

        print(f"✅ Total training examples: {total_examples}")
        return True

    except Exception as e:
        print(f"❌ Error reading NLU data: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Solar Chatbot Tests")
    print("=" * 40)

    tests = [
        test_file_structure,
        test_yaml_syntax,
        test_python_syntax,
        test_domain_intents,
        test_nlu_data
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
        print("\nTo start the chatbot:")
        print("1. Run: python run_chatbot.py")
        print("2. Choose option 4 for full setup")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()