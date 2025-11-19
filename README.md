# Chat with Mean Einstein 🧠

[![Tests](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/test.yml/badge.svg)](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/test.yml)
[![Code Quality](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/code-quality.yml/badge.svg)](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/code-quality.yml)
[![Security Scan](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/security.yml/badge.svg)](https://github.com/jeffreycrum/ai-assistant-einstein/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/jeffreycrum/ai-assistant-einstein/branch/main/graph/badge.svg)](https://codecov.io/gh/jeffreycrum/ai-assistant-einstein)

An interactive chatbot that lets you converse with a simulated Albert Einstein - complete with his genius, humor, and a mean streak!

## Features

- Chat with an AI-powered Einstein persona
- Built with Google's Gemini 2.5 Flash model via LangChain
- Clean, modern UI powered by Gradio
- Multi-turn conversations with chat history
- Einstein's signature wit and personality

## Installation

### Prerequisites
- Python 3.11+
- Google Gemini API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-assistant-einstein
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python main.py
```

The app will launch in your browser with a shareable Gradio link.

## Development

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Running Tests

Run the full test suite:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=. --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

Run specific test categories:
```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m "not slow"    # Skip slow tests
```

### Code Quality

Format code with Black:
```bash
black .
```

Lint with Flake8:
```bash
flake8 main.py tests/
```

Type check with MyPy:
```bash
mypy main.py
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The following workflows are configured:

### Automated Workflows

#### 🧪 Tests (`test.yml`)
- Runs on: Push to main/master/develop, Pull Requests
- Tests on Python 3.11
- Generates coverage reports and uploads to Codecov
- Enforces 80% minimum coverage threshold
- Uploads HTML coverage reports as artifacts

#### 🎨 Code Quality (`code-quality.yml`)
- Runs on: Push and Pull Requests
- Checks code formatting with Black
- Lints code with Flake8
- Type checks with MyPy
- Uploads linting reports as artifacts

#### 💬 PR Comments (`pr-comment.yml`)
- Runs on: Pull Requests only
- Posts automated coverage report as PR comment
- Updates existing comment on subsequent runs
- Shows pass/fail status based on coverage threshold

#### 🔒 Security (`security.yml`)
- Runs on: Push, Pull Requests, Weekly schedule (Mondays)
- Scans dependencies for known vulnerabilities with Safety
- Analyzes code for security issues with Bandit
- Uploads security reports as artifacts

#### 🤖 Dependabot (`dependabot.yml`)
- Automated dependency updates for Python packages (weekly)
- Automated GitHub Actions version updates (monthly)
- Auto-labels and assigns PRs

### Workflow Badges

The badges at the top of this README show the current status of:
- Test suite execution
- Code quality checks
- Security scanning
- Code coverage percentage

### Setting Up CI/CD

To use the CI/CD pipeline in your fork:

1. **Enable GitHub Actions** in repository settings
2. **Add secrets** (optional):
   - `CODECOV_TOKEN`: For uploading coverage to Codecov
   - `GEMINI_API_KEY`: If you want to run integration tests with real API
3. **Review Dependabot PRs** regularly to keep dependencies updated

### Manual Workflow Triggers

All workflows can be manually triggered via the GitHub Actions UI using the `workflow_dispatch` event.

## Project Structure

```
ai-assistant-einstein/
├── .github/
│   ├── workflows/
│   │   ├── test.yml          # Main test workflow
│   │   ├── code-quality.yml  # Linting and formatting
│   │   ├── pr-comment.yml    # PR coverage comments
│   │   └── security.yml      # Security scanning
│   └── dependabot.yml        # Dependency updates
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Shared test fixtures
│   ├── test_chat.py         # Chat function tests
│   ├── test_clear_chat.py   # Clear chat tests
│   ├── test_config.py       # Configuration tests
│   └── README.md            # Testing guide
├── main.py                  # Main application
├── einstein.png             # Einstein avatar
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pytest.ini               # Pytest configuration
├── .coveragerc             # Coverage configuration
├── Makefile                # Development commands
├── TESTING.md              # Testing documentation
└── .env                    # Environment variables (gitignored)
```

## Configuration

The Einstein persona is configured via the system prompt in `main.py`:
- Speaks from Einstein's first-person perspective
- Shares personal anecdotes and experiences
- Has a sense of humor with a mean edge
- Keeps responses brief (< 300 characters)

Model settings:
- Model: `gemini-2.5-flash`
- Temperature: `0.5`

## Testing

The project includes a comprehensive test suite covering:
- Unit tests for core functions (23+ tests)
- Integration tests for LangChain components
- Error handling and edge cases
- Environment configuration
- 80% minimum code coverage requirement

See [tests/README.md](tests/README.md) for quick testing guide and [TESTING.md](TESTING.md) for comprehensive testing documentation.

## License

[Add your license here]

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass (`make test`)
2. Code is formatted (`make format`)
3. Linting passes (`make lint`)
4. Coverage stays above 80%
5. Security scans are clean

Pull requests will automatically run the full CI/CD pipeline.
