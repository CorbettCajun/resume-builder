# Project Directory Structure

```
resume-builder/
│
├── src/                    # Source code directory
│   ├── core/               # Core system components
│   │   ├── config.py       # Configuration management
│   │   ├── logging.py      # Logging utilities
│   │   └── error_handling.py  # Error handling and circuit breakers
│   │
│   ├── services/           # Service layer
│   │   ├── github_service.py   # GitHub API interaction
│   │   └── resume_service.py   # Resume generation logic
│   │
│   ├── github_resume_agent.py  # Main resume generation agent
│   └── resume_exporter.py      # Resume export functionality
│
├── tests/                  # Test suite
│   ├── test_github_service.py
│   ├── test_github_resume_agent.py
│   └── test_resume_exporter.py
│
├── docs/                   # Documentation (optional)
│
├── templates/              # Web templates
│   └── resume_template.html
│
├── static/                 # Static web assets
│   ├── css/
│   └── js/
│
├── scripts/                # Utility scripts
│   ├── generate_resume.py
│   └── export_resume.py
│
├── .github/                # CI/CD workflows
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── .gitignore
│
├── MASTER.md               # Central documentation
├── README.md               # Project overview
├── CHANGES.md              # Changelog
├── WORK-LOG.md             # Task tracking
├── DECISIONS.md            # Architectural decisions
└── TODO.md                 # Future tasks and roadmap
```

## Directory Purpose Breakdown

### `src/`
- Contains the core application logic
- Separated into modular components for maintainability

### `tests/`
- Comprehensive test suite
- Mirrors `src/` directory structure
- Ensures code quality and functionality

### `templates/` and `static/`
- Web interface resources
- Supports potential web-based resume generation

### `scripts/`
- Utility scripts for various operations
- Can be used for CLI or automated tasks

### `.github/`
- Continuous Integration and Deployment configurations
- Automated testing and deployment workflows

## Best Practices
- Keep source code modular
- Separate concerns between modules
- Maintain clear, descriptive naming conventions
- Document each directory's purpose
