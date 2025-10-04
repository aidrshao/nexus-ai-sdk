import ast
import sys

files_to_check = [
    'nexusai/__init__.py',
    'nexusai/__version__.py',
    'nexusai/client.py',
    'nexusai/config.py',
    'nexusai/error.py',
]

print("Checking Python syntax...")
errors = 0

for filepath in files_to_check:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
            ast.parse(code)
        print(f"✓ {filepath}")
    except SyntaxError as e:
        print(f"✗ {filepath}: {e}")
        errors += 1
    except Exception as e:
        print(f"? {filepath}: {e}")

if errors == 0:
    print("\n✓ All checked files have valid Python syntax!")
else:
    print(f"\n✗ Found {errors} syntax errors")
    sys.exit(1)
