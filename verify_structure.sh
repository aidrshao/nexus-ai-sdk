#!/bin/bash
echo "Verifying Nexus AI SDK Structure..."
echo ""

# Count Python files
py_count=$(find nexusai -name "*.py" -type f | wc -l)
echo "✓ Python files in nexusai/: $py_count"

# Check core modules
echo ""
echo "Core modules:"
for file in __init__.py __version__.py client.py config.py constants.py error.py models.py types.py; do
    if [ -f "nexusai/$file" ]; then
        echo "  ✓ nexusai/$file"
    else
        echo "  ✗ nexusai/$file (MISSING)"
    fi
done

# Check internal modules
echo ""
echo "Internal modules:"
for file in __init__.py _client.py _poller.py; do
    if [ -f "nexusai/_internal/$file" ]; then
        echo "  ✓ nexusai/_internal/$file"
    else
        echo "  ✗ nexusai/_internal/$file (MISSING)"
    fi
done

# Check resource modules
echo ""
echo "Resource modules:"
for file in __init__.py images.py text.py sessions.py files.py audio.py knowledge_bases.py; do
    if [ -f "nexusai/resources/$file" ]; then
        echo "  ✓ nexusai/resources/$file"
    else
        echo "  ✗ nexusai/resources/$file (MISSING)"
    fi
done

# Check config files
echo ""
echo "Configuration files:"
for file in .env .env.example .gitignore pyproject.toml LICENSE README.md; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
    fi
done

echo ""
echo "Structure verification complete!"
