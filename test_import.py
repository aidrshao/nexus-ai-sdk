"""Quick test script to verify SDK import and structure."""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Test imports
print("Testing imports...")

try:
    import nexusai
    print(f"✓ nexusai imported successfully")
    print(f"  Version: {nexusai.__version__}")
except Exception as e:
    print(f"✗ Failed to import nexusai: {e}")
    sys.exit(1)

try:
    from nexusai import NexusAIClient
    print(f"✓ NexusAIClient imported")
except Exception as e:
    print(f"✗ Failed to import NexusAIClient: {e}")
    sys.exit(1)

try:
    from nexusai import config
    print(f"✓ config imported")
    print(f"  Default base_url: {config.base_url}")
except Exception as e:
    print(f"✗ Failed to import config: {e}")
    sys.exit(1)

try:
    from nexusai import error
    print(f"✓ error module imported")
    print(f"  Available exceptions: {[name for name in dir(error) if not name.startswith('_')]}")
except Exception as e:
    print(f"✗ Failed to import error: {e}")
    sys.exit(1)

# Test client initialization (without actually connecting)
try:
    import os
    os.environ['NEXUS_API_KEY'] = 'test_key'
    client = NexusAIClient()
    print(f"✓ NexusAIClient initialized")
    print(f"  Client has .images: {hasattr(client, 'images')}")
    print(f"  Client has .text: {hasattr(client, 'text')}")
    print(f"  Client has .sessions: {hasattr(client, 'sessions')}")
    print(f"  Client has .files: {hasattr(client, 'files')}")
    print(f"  Client has .audio: {hasattr(client, 'audio')}")
    print(f"  Client has .knowledge_bases: {hasattr(client, 'knowledge_bases')}")
except Exception as e:
    print(f"✗ Failed to initialize client: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All import tests passed!")
