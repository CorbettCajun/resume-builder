# GitHub Resume Generator

## Overview
A powerful tool to generate professional resumes directly from GitHub profiles.

## Features
- Extract GitHub profile information
- Generate resumes in multiple formats (JSON, Markdown, PDF)
- Analyze project contributions
- Highlight programming languages and skills

## Prerequisites
- Python 3.9+
- GitHub Personal Access Token

## Installation
1. Clone the repository
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set GitHub Token
Create a `.env` file in the project root:
```
GITHUB_TOKEN=your_github_personal_access_token
```

## Running the Application
```bash
flask run
```

## Usage
1. Navigate to `http://localhost:5000`
2. Enter GitHub username
3. Choose output format
4. Generate resume

## Testing
```bash
pytest tests/
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
