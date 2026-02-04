# llm_project

A FastAPI-based LLM utility service that integrates Google's Gemini AI with PostgreSQL for intelligent text generation.

## Features

- **FastAPI REST API** - Fast, modern Python web framework
- **Gemini AI Integration** - Google's generative AI for text responses
- **PostgreSQL Database** - Persistent data storage with SQLAlchemy ORM
- **Docker Support** - Containerized deployment with Docker Compose
- **Hot Reload** - Automatic code reloading during development
- **Environment Management** - Secure secret handling via environment variables and Docker secrets

## Project Structure

```
llm_project/
├── main.py                    # FastAPI application entry point
├── database.py                # Database configuration and session management
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image configuration
├── compose.yaml               # Docker Compose multi-container setup
├── models/
│   └── model.py               # Pydantic request/response models
│   └── db_model.py            # Database models
└── data/                      # Data files and scripts
```

## Setup & Installation

### Prerequisites

- Docker and Docker Compose installed
- Python 3.14+ (for local development)
- Google Gemini API key

### Environment Variables

```env
DB_PASSWORD=your_secure_password
DB_USER=postgres
DB_HOST=db
DB_NAME=databaseName
GENAI_KEY=api-key
```

### Running with Docker Compose

```bash
docker compose up
```

The API will be available at `http://localhost:8000`
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

### Local Development (without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Endpoints

### GET `/`
Health check endpoint
```json
{
  "Welcome to the LLM Project API!"
}
```



## Database Integration

The project uses **SQLAlchemy ORM** with PostgreSQL. Database sessions are managed through FastAPI dependency injection.


## Architecture & Key Patterns

### Configuration
- **Environment variables** stored in `.env` (local development)
- **Docker secrets** stored in `.env/` directory (production deployment)
- API keys passed via environment variables


## Troubleshooting

### Database Connection Issues
If you see PostgreSQL errors, ensure:
1. `.env` file exists with correct `DB_PASSWORD`
2. `.env/db_password.txt` file exists
3. Run `docker compose down -v` to reset volumes if upgrading PostgreSQL versions

### Code Changes Not Reloading
The project uses volume mounts for hot reload:
```yaml
volumes:
  - .:/app  # Mounts source code into container
```
uvicorn's `--reload` flag detects changes automatically.

### API Key Not Found
Ensure `GENAI_API_KEY` is set in `.env` and the container has access to the secret:
```bash
docker compose logs server  # Check if API_KEY is loaded
```

## Dependencies

- **fastapi** - Web framework
- **pydantic** - Data validation
- **sqlalchemy** - ORM
- **psycopg2-binary** - PostgreSQL driver
- **uvicorn** - ASGI server
- **google-generativeai** - Gemini AI SDK

See `requirements.txt` for versions.

## Docker Deployment

The `compose.yaml` includes:
- **server** - FastAPI application (Python 3.14-slim)
- **db** - PostgreSQL 18+ database
- **volumes** - Data persistence
- **secrets** - Secure credential management

For production deployments, remove the `--reload` flag from the Dockerfile CMD.