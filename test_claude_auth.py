#!/usr/bin/env python3
"""Test Claude Code authentication"""
import subprocess
import os
import sys

# Remove ANTHROPIC_API_KEY if it exists
os.environ.pop("ANTHROPIC_API_KEY", None)

# Test 1: Run with current environment (without ANTHROPIC_API_KEY)
print("Test 1: Running Claude with current environment (ANTHROPIC_API_KEY removed)...")
result = subprocess.run(
    ["C:\\Users\\amogh\\.local\\bin\\claude.exe", "-p", "What is 2+2?"],
    capture_output=True,
    text=True,
    timeout=60
)

print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout[:500]}")
print(f"Stderr: {result.stderr[:500]}")
print()

# Test 2: Run with minimal environment
print("Test 2: Running Claude with minimal environment...")
minimal_env = {
    "PATH": os.environ.get("PATH", ""),
    "HOME": os.environ.get("HOME", ""),
    "USER": os.environ.get("USER", ""),
    "PWD": os.getcwd(),
}

result2 = subprocess.run(
    ["C:\\Users\\amogh\\.local\\bin\\claude.exe", "-p", "What is 2+2?"],
    capture_output=True,
    text=True,
    env=minimal_env,
    timeout=60
)

print(f"Return code: {result2.returncode}")
print(f"Stdout: {result2.stdout[:500]}")
print(f"Stderr: {result2.stderr[:500]}")
