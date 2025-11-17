# GitHub Actions Workflows Documentation

This document provides detailed information about the CI/CD workflows configured for the AI Assistant Einstein project.

## Overview

The project uses GitHub Actions for automated testing, code quality checks, security scanning, and dependency management. All workflows are located in `.github/workflows/`.

## Workflows

### 1. Tests Workflow (`test.yml`)

**Purpose**: Run the test suite on multiple Python versions and generate coverage reports.

**Triggers**:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches
- Manual trigger via `workflow_dispatch`

**What it does**:
1. Sets up Python environments (3.8, 3.9, 3.10, 3.11, 3.12)
2. Installs dependencies from `requirements-dev.txt`
3. Runs pytest with coverage reporting
4. Uploads coverage to Codecov (Python 3.11 only)
5. Uploads HTML coverage report as artifact
6. Checks that coverage meets 80% threshold
7. Generates test summary in GitHub UI

**Key Features**:
- Matrix testing across 5 Python versions
- Pip caching for faster runs
- Coverage threshold enforcement
- Codecov integration
- Artifact uploads for detailed reports

**Required Secrets** (optional):
- `CODECOV_TOKEN`: For uploading to Codecov
- `GEMINI_API_KEY`: Uses test key by default; provide real key for API tests

**Outputs**:
- Test results for each Python version
- Coverage percentage
- HTML coverage report (downloadable artifact)
- Pass/fail status

---

### 2. Code Quality Workflow (`code-quality.yml`)

**Purpose**: Enforce code quality standards through linting and formatting checks.

**Triggers**:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches
- Manual trigger via `workflow_dispatch`

**What it does**:
1. Checks code formatting with Black
2. Lints code with Flake8 (checks for syntax errors and PEP 8 violations)
3. Type checks with MyPy
4. Generates summaries in GitHub UI
5. Uploads linting reports as artifacts

**Code Quality Standards**:
- **Black**: Enforces consistent code formatting
- **Flake8**:
  - Critical errors (E9, F63, F7, F82) fail the build
  - Max line length: 100 characters
  - Other warnings don't fail build
- **MyPy**: Type checking (currently informational, doesn't fail build)

**Outputs**:
- Formatting check results
- Linting report with issue counts
- Type checking report
- Downloadable artifacts with detailed reports

**Fixing Issues**:
```bash
# Fix formatting
black main.py tests/

# Check linting
flake8 main.py tests/ --max-line-length=100

# Type check
mypy main.py --ignore-missing-imports
```

---

### 3. PR Comment Workflow (`pr-comment.yml`)

**Purpose**: Automatically post test coverage information as comments on pull requests.

**Triggers**:
- Pull requests to `main`, `master`, or `develop` branches

**Permissions Required**:
- `contents: read`
- `pull-requests: write`

**What it does**:
1. Runs tests with coverage
2. Extracts coverage metrics
3. Generates formatted coverage report
4. Posts comment on PR (or updates existing comment)
5. Shows pass/fail status based on 80% threshold

**Comment Format**:
```markdown
## ✅ Test Coverage Report

| Metric | Value |
|--------|-------|
| Coverage | 85.23% |
| Tests Passed | 23 |
| Status | ✅ PASSING |
| Threshold | 80% |
```

**Features**:
- Updates existing comment instead of creating duplicates
- Shows coverage percentage and test count
- Visual pass/fail indicator
- Threshold comparison

---

### 4. Security Workflow (`security.yml`)

**Purpose**: Scan for security vulnerabilities in dependencies and code.

**Triggers**:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches
- Weekly schedule (Mondays at 00:00 UTC)
- Manual trigger via `workflow_dispatch`

**What it does**:
1. **Safety**: Scans Python dependencies for known security vulnerabilities
2. **Bandit**: Analyzes code for security issues and common vulnerabilities
3. Generates security reports
4. Uploads reports as artifacts
5. Posts summaries to GitHub UI

**Security Checks**:
- **Safety**: Checks against CVE database for vulnerable packages
- **Bandit**: Detects:
  - Hardcoded passwords/secrets
  - SQL injection vulnerabilities
  - Use of insecure functions
  - Weak cryptography
  - And more...

**Outputs**:
- Vulnerability count by severity (High/Medium/Low)
- JSON reports for detailed analysis
- Downloadable artifacts

**Current Status**:
- Both checks set to `continue-on-error: true` (informational)
- Can be made strict by removing this setting

---

### 5. Dependabot Configuration (`dependabot.yml`)

**Purpose**: Automatically create PRs for dependency updates.

**Schedule**:
- **Python packages**: Weekly on Mondays at 09:00
- **GitHub Actions**: Monthly

**What it does**:
1. Checks for updates to Python packages in `requirements.txt` and `requirements-dev.txt`
2. Checks for updates to GitHub Actions versions
3. Creates PRs with version bumps
4. Labels PRs appropriately
5. Assigns to repository maintainers

**Configuration**:
- Max 10 open PRs for Python packages
- Max 5 open PRs for GitHub Actions
- Automatic labeling: `dependencies`, `python`, `github-actions`
- Commit message prefixes: `deps`, `deps-dev`, `ci`

**Reviewing Dependabot PRs**:
1. Check the changelog/release notes
2. Review test results from CI
3. Merge if tests pass and changes are safe
4. Can merge multiple Dependabot PRs at once

---

## Workflow Artifacts

All workflows upload artifacts that can be downloaded from the GitHub Actions UI:

| Workflow | Artifact | Retention |
|----------|----------|-----------|
| Tests | `coverage-report` (HTML) | 30 days |
| Code Quality | `linting-reports` (txt) | 30 days |
| Security | `security-reports` (JSON) | 30 days |

**Downloading Artifacts**:
1. Go to Actions tab in GitHub
2. Click on a workflow run
3. Scroll to "Artifacts" section
4. Click to download

---

## Workflow Status Badges

Add these badges to your README to show workflow status:

```markdown
[![Tests](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/test.yml/badge.svg)](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/test.yml)
[![Code Quality](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/code-quality.yml/badge.svg)](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/code-quality.yml)
[![Security Scan](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/security.yml/badge.svg)](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/security.yml)
```

---

## Manual Workflow Triggers

All workflows support manual triggering via `workflow_dispatch`:

1. Go to **Actions** tab in GitHub
2. Select the workflow from the left sidebar
3. Click **Run workflow** button
4. Select the branch
5. Click **Run workflow**

---

## Secrets Configuration

Some workflows use GitHub secrets for sensitive data:

### Required Secrets
None - all workflows work without secrets using defaults.

### Optional Secrets

| Secret | Purpose | Used By |
|--------|---------|---------|
| `CODECOV_TOKEN` | Upload coverage to Codecov | `test.yml` |
| `GEMINI_API_KEY` | Real API testing (optional) | `test.yml` |

**Adding Secrets**:
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Enter name and value
4. Click "Add secret"

---

## Debugging Failed Workflows

### Test Failures

1. Click on the failed workflow run
2. Expand the "Run tests with coverage" step
3. Review test output and error messages
4. Download coverage artifact for detailed report
5. Fix failing tests locally:
   ```bash
   pytest -v  # Run with verbose output
   pytest tests/test_name.py::test_function  # Run specific test
   ```

### Code Quality Failures

**Black formatting**:
```bash
black main.py tests/  # Auto-fix formatting
```

**Flake8 linting**:
```bash
flake8 main.py tests/ --max-line-length=100  # Check issues
# Fix manually based on output
```

### Security Issues

1. Review the security report artifact
2. For dependency vulnerabilities:
   - Update the vulnerable package
   - Or add to allowlist if false positive
3. For code issues:
   - Review Bandit output
   - Fix security issues or add `# nosec` comment if false positive

### Coverage Threshold Failures

If coverage drops below 80%:

1. Download coverage HTML artifact
2. Identify uncovered lines
3. Add tests for uncovered code:
   ```bash
   pytest --cov=. --cov-report=term-missing  # Show missing lines
   ```

---

## Performance Optimization

### Caching

Workflows use pip caching to speed up dependency installation:
```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'
```

### Matrix Strategy

Test workflow uses `fail-fast: false` to run all Python versions even if one fails.

### Conditional Steps

Some steps only run on specific conditions:
- Coverage upload: Python 3.11 only
- Artifacts: Only on specific Python versions
- PR comments: Only on pull requests

---

## Best Practices

### For Contributors

1. **Run tests locally** before pushing:
   ```bash
   make test
   ```

2. **Format code** before committing:
   ```bash
   make format
   ```

3. **Check linting**:
   ```bash
   make lint
   ```

4. **Ensure coverage** stays above 80%:
   ```bash
   make test-coverage
   ```

### For Maintainers

1. **Review Dependabot PRs** weekly
2. **Monitor security scans** for vulnerabilities
3. **Keep workflows updated** using Dependabot
4. **Review coverage trends** over time
5. **Update Python versions** as new versions release

---

## Customization

### Changing Coverage Threshold

Edit `.coveragerc`:
```ini
[report]
fail_under = 85  # Change from 80 to 85
```

### Adding Python Versions

Edit `test.yml`:
```yaml
matrix:
  python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
```

### Changing Lint Rules

Edit `code-quality.yml` to adjust Flake8 rules:
```yaml
flake8 main.py tests/ --ignore=E203,W503 --max-line-length=120
```

### Adjusting Dependabot Schedule

Edit `dependabot.yml`:
```yaml
schedule:
  interval: "daily"  # Change from weekly
```

---

## Troubleshooting

### Workflow Not Running

**Check**:
- Branch names in workflow triggers match your branches
- GitHub Actions is enabled in repository settings
- Workflow YAML syntax is valid

### Coverage Not Uploading to Codecov

**Check**:
- `CODECOV_TOKEN` secret is set
- Codecov repository is configured
- Coverage.xml file is generated

### PR Comments Not Posting

**Check**:
- Workflow has `pull-requests: write` permission
- GitHub token has necessary permissions
- No rate limiting from GitHub API

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Codecov Documentation](https://docs.codecov.io/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
