# GitHub Resume Builder API Documentation

## Overview
The GitHub Resume Builder provides a comprehensive API for generating resumes from GitHub profiles.

## Authentication
- **Type**: GitHub Personal Access Token
- **Required Scopes**: 
  - `read:user`
  - `repo`

## Endpoints

### 1. Generate Resume
- **Method**: POST
- **Endpoint**: `/api/resume/generate`
- **Request Body**:
```json
{
  "username": "github_username",
  "format": ["json", "markdown", "pdf"],
  "options": {
    "include_contributions": true,
    "max_repositories": 50
  }
}
```
- **Response**:
```json
{
  "profile": {
    "name": "User Name",
    "email": "user@example.com",
    "location": "City, Country",
    "total_contributions": 1024,
    "total_repositories": 42
  },
  "skills": ["Python", "JavaScript", "TypeScript"],
  "repositories": [
    {
      "name": "Project Name",
      "language": "Python",
      "stars": 10,
      "forks": 5
    }
  ]
}
```

### 2. Export Resume
- **Method**: GET
- **Endpoint**: `/api/resume/export`
- **Query Parameters**:
  - `username`: GitHub username
  - `format`: Output format (json/markdown/pdf)

## Error Handling
- **400**: Invalid input
- **401**: Authentication failed
- **404**: User not found
- **429**: Rate limit exceeded
- **500**: Internal server error

## Rate Limiting
- **Limit**: 60 requests per hour
- **Per User**: Based on GitHub API limits

## Security Considerations
- Always use HTTPS
- Store tokens securely
- Implement token rotation
- Validate and sanitize all inputs

## Example Usage (Python)
```python
from github_resume_agent import GitHubResumeAgent

# Initialize with GitHub token
agent = GitHubResumeAgent(token='your_github_token')

# Generate resume
resume = agent.generate_resume('github_username')

# Export to different formats
json_resume = agent.export_resume(format='json')
markdown_resume = agent.export_resume(format='markdown')
```

## Webhook Integration
- Supports real-time resume generation notifications
- Configure webhook URL for async processing

## Versioning
- Current API Version: v1.0
- Semantic versioning applied
- Backward compatibility maintained
