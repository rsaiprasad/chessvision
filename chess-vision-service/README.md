# Chess Vision Service

Backend REST API service for chess video analysis that exposes the functionality of the Chess Vision Library through a web API.

## Features

- Video upload and processing
- Real-time video stream analysis
- REST API for chess position and move data
- PGN/FEN generation endpoints
- Authentication and authorization
- API documentation with Swagger/OpenAPI

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chess-vision-service.git
cd chess-vision-service

# Install with Poetry
poetry install
```

## Usage

```bash
# Start the service
poetry run start

# Or manually
poetry run uvicorn chess_vision_service.main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### Video Processing

- `POST /api/videos/upload` - Upload a video file for processing
- `POST /api/videos/stream` - Process a video stream
- `GET /api/videos/{video_id}/status` - Get processing status

### Chess Analysis

- `GET /api/videos/{video_id}/positions` - Get all detected positions
- `GET /api/videos/{video_id}/moves` - Get all detected moves
- `GET /api/videos/{video_id}/pgn` - Get PGN notation
- `GET /api/videos/{video_id}/fen` - Get current FEN

### Documentation

- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation
- `GET /openapi.json` - OpenAPI schema

## Development

```bash
# Run tests
poetry run pytest

# Format code
poetry run black src tests

# Type checking
poetry run mypy src

# Linting
poetry run flake8 src
```

## Configuration

Configuration is handled through environment variables:

```
CHESS_VISION_HOST=0.0.0.0
CHESS_VISION_PORT=8000
CHESS_VISION_DEBUG=true
CHESS_VISION_LOG_LEVEL=info
```

## License

[MIT](LICENSE)
