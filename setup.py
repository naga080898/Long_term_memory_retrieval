#!/usr/bin/env python3
"""
Setup script for RAG System
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False


def test_imports():
    """Test if all required packages can be imported"""
    print("\nTesting imports...")
    required_packages = [
        "sentence_transformers",
        "faiss",
        "numpy",
        "pickle"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package}: {e}")
            return False
    
    return True


def download_model():
    """Download the sentence transformer model"""
    print("\nDownloading sentence transformer model...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Model downloaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error downloading model: {e}")
        return False


def main():
    """Main setup function"""
    print("=== RAG System Setup ===\n")
    
    # Check if virtual environment is activated
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment detected")
    else:
        print("⚠ Warning: No virtual environment detected. Consider using one.")
    
    # Install requirements
    if not install_requirements():
        print("\nSetup failed at package installation.")
        return False
    
    # Test imports
    if not test_imports():
        print("\nSetup failed at import testing.")
        return False
    
    # Download model
    if not download_model():
        print("\nSetup failed at model download.")
        return False
    
    print("\n=== Setup Complete! ===")
    print("\nYou can now run the example:")
    print("python example_usage.py")
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)