#!/usr/bin/env python3
"""Check if required dependencies are installed."""

import sys

print("Checking dependencies for Nexus AI SDK...")
print("=" * 60)

dependencies = {
    'httpx': '0.25.0',
    'pydantic': '2.5.0',
    'dotenv': '1.0.0',  # python-dotenv
}

missing = []
installed = []

for package, min_version in dependencies.items():
    try:
        if package == 'dotenv':
            # python-dotenv is imported as dotenv
            import dotenv
            installed.append(f"✓ python-dotenv (imported as dotenv)")
        elif package == 'httpx':
            import httpx
            installed.append(f"✓ httpx {httpx.__version__}")
        elif package == 'pydantic':
            import pydantic
            installed.append(f"✓ pydantic {pydantic.__version__}")
    except ImportError:
        missing.append(f"✗ {package} (required >= {min_version})")

# Print results
if installed:
    print("\nInstalled dependencies:")
    for item in installed:
        print(f"  {item}")

if missing:
    print("\nMissing dependencies:")
    for item in missing:
        print(f"  {item}")
    print("\nTo install missing dependencies:")
    print("  pip install httpx>=0.25.0 pydantic>=2.5.0 python-dotenv>=1.0.0")
    sys.exit(1)
else:
    print("\n" + "=" * 60)
    print("✓ All dependencies installed!")
    print("=" * 60)
    print("\nYou can now test the SDK import:")
    print("  python quick_test.py")
