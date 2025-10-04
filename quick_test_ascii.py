#!/usr/bin/env python3
"""Quick import test - ASCII version for Windows."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("NEXUS AI SDK - Import Test")
print("=" * 60)

# Test 1: Import nexusai package
print("\n[1/6] Testing: import nexusai")
try:
    import nexusai
    print("     [OK] SUCCESS")
    print(f"     Version: {nexusai.__version__}")
except ImportError as e:
    print(f"     [FAIL] {e}")
    sys.exit(1)

# Test 2: Import NexusAIClient
print("\n[2/6] Testing: from nexusai import NexusAIClient")
try:
    from nexusai import NexusAIClient
    print("     [OK] SUCCESS")
except ImportError as e:
    print(f"     [FAIL] {e}")
    sys.exit(1)

# Test 3: Import config
print("\n[3/6] Testing: from nexusai import config")
try:
    from nexusai import config
    print("     [OK] SUCCESS")
    print(f"     Default base_url: {config.base_url}")
except ImportError as e:
    print(f"     [FAIL] {e}")
    sys.exit(1)

# Test 4: Import error module
print("\n[4/6] Testing: from nexusai import error")
try:
    from nexusai import error
    print("     [OK] SUCCESS")
    exceptions = [
        'APIError', 'AuthenticationError', 'PermissionError',
        'NotFoundError', 'RateLimitError', 'InvalidRequestError',
        'ServerError', 'APITimeoutError', 'NetworkError'
    ]
    available = [e for e in exceptions if hasattr(error, e)]
    print(f"     Available exceptions: {len(available)}/9")
except ImportError as e:
    print(f"     [FAIL] {e}")
    sys.exit(1)

# Test 5: Initialize client (with dummy key)
print("\n[5/6] Testing: Initialize NexusAIClient")
try:
    os.environ['NEXUS_API_KEY'] = 'nxs_4K5rIBmsp4wNszg_BuZ-Kih4gLLbx41dGxwNk_mkfaw'
    client = NexusAIClient()
    print("     [OK] SUCCESS")
    print("     Client initialized")
except Exception as e:
    print(f"     [FAIL] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Check resource properties
print("\n[6/6] Testing: Client resource properties")
try:
    resources = ['images', 'text', 'sessions', 'files', 'audio', 'knowledge_bases']
    all_present = True
    for resource in resources:
        has_it = hasattr(client, resource)
        status = "[OK]" if has_it else "[FAIL]"
        print(f"     {status} client.{resource}: {has_it}")
        if not has_it:
            all_present = False

    if all_present:
        print("     [OK] SUCCESS")
    else:
        print("     [FAIL] Some resources missing")
        sys.exit(1)
except Exception as e:
    print(f"     [FAIL] {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("[OK] ALL IMPORT TESTS PASSED!")
print("=" * 60)
print("\nThe SDK is ready to use!")
print("Next step: Ensure your API server is running on http://localhost:8000")
