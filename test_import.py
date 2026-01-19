#!/usr/bin/env python
"""Test script to check langchain-openai import"""

import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("\nPython path:")
for path in sys.path:
    print(f"  {path}")

print("\n" + "="*60)
print("Testing langchain-openai import...")
print("="*60)

try:
    from langchain_openai import ChatOpenAI
    print("✓ SUCCESS: langchain_openai imported successfully!")
    print(f"  ChatOpenAI location: {ChatOpenAI.__module__}")
except ImportError as e:
    print(f"✗ FAILED: Cannot import langchain_openai")
    print(f"  Error: {e}")
