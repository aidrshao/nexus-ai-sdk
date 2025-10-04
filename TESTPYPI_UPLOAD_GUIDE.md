# TestPyPI Upload Guide

This guide explains how to upload the Nexus AI SDK v0.1.0 to TestPyPI.

## Prerequisites

1. **Create TestPyPI Account**:
   - Visit https://test.pypi.org/account/register/
   - Complete email verification

2. **Generate API Token**:
   - Go to https://test.pypi.org/manage/account/token/
   - Click "Add API token"
   - Name: `nexus-ai-sdk-upload`
   - Scope: "Entire account" (or specific project if it exists)
   - Copy the token (starts with `pypi-`)

## Upload Steps

### Method 1: Using twine with token (Recommended)

```bash
# Navigate to project directory
cd c:\Users\junsh\Documents\GitHub\nexus-ai-sdk

# Activate virtual environment
venv\Scripts\activate

# Upload to TestPyPI (you'll be prompted for credentials)
python -m twine upload --repository testpypi dist/*

# When prompted:
# Username: __token__
# Password: <paste your TestPyPI API token>
```

### Method 2: Using environment variable

```bash
# Set environment variable (Windows)
set TWINE_PASSWORD=<your-testpypi-token>

# Upload
python -m twine upload --repository testpypi dist/* --username __token__
```

### Method 3: Using .pypirc file

Create `~/.pypirc` (or `%USERPROFILE%\.pypirc` on Windows):

```ini
[distutils]
index-servers =
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-testpypi-token>
```

Then upload:
```bash
python -m twine upload --repository testpypi dist/*
```

## Verify Upload

After successful upload, verify at:
- Package page: https://test.pypi.org/project/nexus-ai-sdk/
- Version 0.1.0: https://test.pypi.org/project/nexus-ai-sdk/0.1.0/

## Test Installation

```bash
# Create new test environment
python -m venv test_env
test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nexus-ai-sdk

# Test import
python -c "from nexusai import NexusAIClient; print('✓ Import successful')"
```

Note: `--extra-index-url https://pypi.org/simple` is needed because dependencies (httpx, pydantic, etc.) are on the main PyPI, not TestPyPI.

## Expected Output

```
Uploading distributions to https://test.pypi.org/legacy/
Uploading nexus_ai_sdk-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.0/29.0 kB • 00:00 • ?
Uploading nexus_ai_sdk-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.0/20.0 kB • 00:00 • ?

View at:
https://test.pypi.org/project/nexus-ai-sdk/0.1.0/
```

## Troubleshooting

### Error: "File already exists"
TestPyPI doesn't allow re-uploading the same version. If you need to make changes:
1. Increment version in `pyproject.toml` (e.g., 0.1.0 → 0.1.1)
2. Update `nexusai/__version__.py`
3. Rebuild: `python -m build`
4. Upload again

### Error: "Invalid credentials"
- Ensure username is `__token__` (with double underscores)
- Verify token is correct and includes `pypi-` prefix
- Check token hasn't expired

### Error: "Package name already taken"
If someone else registered `nexus-ai-sdk`:
- Try a different name in `pyproject.toml`: `nexus-ai-sdk-juncai` or similar
- Update all references
- Rebuild and upload

## Next Steps

After successful TestPyPI upload:
1. Share installation instructions with application development team (see `APP_DEV_INSTALL_GUIDE.md`)
2. Collect feedback from testing
3. Fix any issues
4. When ready, upload to production PyPI using same process but with:
   ```bash
   python -m twine upload dist/*
   ```
   (Without `--repository testpypi`)
