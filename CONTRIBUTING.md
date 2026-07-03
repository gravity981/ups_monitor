# Contributing to UPS Monitor

Thank you for your interest in contributing to the UPS Monitor Home Assistant integration!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/gravity981/ups_monitor.git
cd ups_monitor
```

2. Install development dependencies:
```bash
pip install -r requirements_test.txt
```

## Running Tests

Run all tests with pytest:
```bash
pytest tests/ -v
```

## Code Quality

This project uses several tools to maintain code quality:

### Linting with Flake8

Check for code style issues:
```bash
flake8 custom_components/ups_monitor
```

### Code Formatting with Black

Check code formatting:
```bash
black --check --line-length 120 custom_components/ups_monitor tests/
```

Auto-format code:
```bash
black --line-length 120 custom_components/ups_monitor tests/
```

### Import Sorting with isort

Check import sorting:
```bash
isort --check-only --profile black --line-length 120 custom_components/ups_monitor tests/
```

Auto-fix import sorting:
```bash
isort --profile black --line-length 120 custom_components/ups_monitor tests/
```

### Run All Checks

Before submitting a pull request, ensure all checks pass:
```bash
# Critical errors check
flake8 custom_components/ups_monitor --count --select=E9,F63,F7,F82 --show-source --statistics

# Full flake8 check
flake8 custom_components/ups_monitor

# Formatting checks
black --check --line-length 120 custom_components/ups_monitor tests/
isort --check-only --profile black --line-length 120 custom_components/ups_monitor tests/

# Run tests
pytest tests/ -v
```

## Continuous Integration

The project uses GitHub Actions to automatically run tests and linting on all pull requests and commits to the main branch. The CI pipeline will:

- Run tests on Python 3.11 and 3.12
- Check code with flake8
- Verify code formatting with black
- Verify import sorting with isort

All checks must pass before a pull request can be merged.

## Configuration Files

- `.flake8` - Flake8 linter configuration
- `pyproject.toml` - Black and isort configuration
- `pytest.ini` - Pytest configuration
- `.github/workflows/ci.yml` - GitHub Actions CI pipeline

