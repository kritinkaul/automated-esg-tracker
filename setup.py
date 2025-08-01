#!/usr/bin/env python3
"""
Setup script for ESG Data Tracker.
Helps users get started with the project quickly.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python3 -m venv venv", "Creating virtual environment")


def install_dependencies():
    """Install project dependencies."""
    # Determine the correct pip command
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -r requirements.txt", "Installing dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def create_env_file():
    """Create .env file from template."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys and database credentials")
        return True
    else:
        print("❌ env.example file not found")
        return False


def initialize_database():
    """Initialize the database with sample data."""
    # Determine the correct python command
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} scripts/init_database.py", "Initializing database")


def run_tests():
    """Run basic tests to ensure everything works."""
    # Determine the correct python command
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} -m pytest tests/ -v", "Running tests")


def main():
    """Main setup function."""
    print("🚀 Setting up ESG Data Tracker...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup can continue")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys and database credentials")
    print("2. Run the dashboard: streamlit run dashboard/main.py")
    print("3. Open your browser to http://localhost:8501")
    print("\n📚 For more information, see README.md")
    print("🔗 GitHub repository: https://github.com/yourusername/automated-esg-tracker")


if __name__ == "__main__":
    main() 