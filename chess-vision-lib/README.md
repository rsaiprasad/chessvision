# Chess Vision Library

Core library for chess video analysis that extracts chess positions and moves from video recordings.

## Features

- Video processing and frame extraction
- Chess board detection and normalization
- Position extraction and validation
- Move tracking and chess logic
- PGN/FEN notation generation
- Visualization utilities

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chess-vision-lib.git
cd chess-vision-lib

# Install with Poetry
poetry install
```

## Usage

```python
from chess_vision.video.input import VideoInput
from chess_vision.board.detector import BoardDetector
from chess_vision.board.normalizer import BoardNormalizer
from chess_vision.position.extractor import PositionExtractor
from chess_vision.moves.tracker import MoveTracker
from chess_vision.notation.generator import NotationGenerator

# Initialize components
video_input = VideoInput("path/to/video.mp4")
board_detector = BoardDetector()
board_normalizer = BoardNormalizer()
position_extractor = PositionExtractor()
move_tracker = MoveTracker()
notation_generator = NotationGenerator()

# Process video frames
for frame in video_input.get_frames():
    # Detect chess board
    board_contour = board_detector.detect_board(frame)
    if board_contour is not None:
        # Extract and normalize board
        board_img = board_detector.extract_board(frame, board_contour)
        normalized_board = board_normalizer.normalize_board(board_img)
        
        # Extract position
        position = position_extractor.extract_position(normalized_board)
        
        # Track moves
        move = move_tracker.track_move(position)
        if move:
            # Generate notation
            pgn = notation_generator.add_move(move)
            print(f"Move detected: {move}, PGN: {pgn}")
```

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

## License

[MIT](LICENSE)
