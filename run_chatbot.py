#!/usr/bin/env python3
"""
Solar Panel Chatbot Setup and Run Script
This script helps set up and run the complete chatbot system.
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def train_rasa_model():
    """Train the Rasa model"""
    print("Training Rasa model...")
    try:
        result = subprocess.run(
            ["rasa", "train"],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            print("✓ Rasa model trained successfully")
            return True
        else:
            print(f"Error training model: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Error: Training timed out after 5 minutes")
        return False
    except FileNotFoundError:
        print("Error: Rasa not found. Please install Rasa first.")
        return False

def start_rasa_servers():
    """Start Rasa action server and core server"""
    print("Starting Rasa servers...")

    # Start action server
    try:
        action_process = subprocess.Popen(
            ["rasa", "run", "actions"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)
        print("✓ Rasa Action Server started")

        # Start main server
        rasa_process = subprocess.Popen(
            ["rasa", "run", "--enable-api", "--cors", "*"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(5)
        print("✓ Rasa Core Server started")

        return action_process, rasa_process

    except FileNotFoundError:
        print("Error: Rasa not found. Please install Rasa first.")
        return None, None
    except Exception as e:
        print(f"Error starting Rasa servers: {e}")
        return None, None

def start_flask_app():
    """Start the Flask web application"""
    print("Starting Flask web application...")
    try:
        # Import and run the Flask app
        from app import app, rasa_manager

        # Start Rasa if not already running
        if not rasa_manager.rasa_running:
            rasa_thread = threading.Thread(target=rasa_manager.start_rasa, daemon=True)
            rasa_thread.start()
            time.sleep(8)

        print("✓ Flask application started")
        print("\n🌟 Solar Panel Chatbot is ready!")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("🔍 API Status: http://localhost:5000/api/status")

        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

    except Exception as e:
        print(f"Error starting Flask app: {e}")

def check_project_structure():
    """Check if all required files exist"""
    required_files = [
        'config.yml',
        'domain.yml',
        'data/nlu.yml',
        'data/stories.yml',
        'data/rules.yml',
        'actions/actions.py',
        'templates/index.html',
        'app.py',
        'requirements.txt'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("Error: Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False

    print("✓ All required files found")
    return True

def main():
    """Main setup and run function"""
    print("🌞 Solar Panel Chatbot Setup")
    print("=" * 40)

    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Check project structure
    if not check_project_structure():
        sys.exit(1)

    # Check Python version
    check_python_version()

    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Install dependencies only")
    print("2. Train model only")
    print("3. Start chatbot only")
    print("4. Full setup (install + train + start)")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ").strip()

    if choice == "1":
        install_dependencies()
    elif choice == "2":
        train_rasa_model()
    elif choice == "3":
        start_flask_app()
    elif choice == "4":
        # Full setup
        if not install_dependencies():
            print("Failed to install dependencies. Exiting.")
            sys.exit(1)

        if not train_rasa_model():
            print("Failed to train model. You can still run with existing model.")

        start_flask_app()
    elif choice == "5":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice. Starting full setup...")
        if not install_dependencies():
            print("Failed to install dependencies. Exiting.")
            sys.exit(1)

        if not train_rasa_model():
            print("Failed to train model. You can still run with existing model.")

        start_flask_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Chatbot stopped. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)