# Chess Video Analyzer

A tool for analyzing chess games from video recordings, extracting positions, and tracking moves in real-time.

## Overview

Chess Video Analyzer is a Python application that processes chess game videos, identifies the chess board, extracts positions, and tracks moves as they occur. It outputs the game in standard chess notation (PGN/FEN) for further analysis.

## Features

- Process chess game videos (recorded files or streams)
- Identify and extract the chess board from video frames
- Recognize chess pieces and their positions
- Track moves as they occur in the video
- Output standard chess notation (PGN/FEN) for the game
- Visualize the detected board and positions

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenCV
- python-chess
- NumPy

### Setup with Poetry

```bash
# Clone the repository
git clone https://github.com/yourusername/chess-video-analyzer.git
cd chess-video-analyzer

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/chess-video-analyzer.git
cd chess-video-analyzer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

```bash
# Basic usage
python -m chess_video_analyzer.cli.main path/to/video.mp4

# Generate PGN output
python -m chess_video_analyzer.cli.main path/to/video.mp4 --pgn

# Generate FEN output
python -m chess_video_analyzer.cli.main path/to/video.mp4 --fen

# Show visualization during processing
python -m chess_video_analyzer.cli.main path/to/video.mp4 --visualize

# Save processed frames
python -m chess_video_analyzer.cli.main path/to/video.mp4 --save-frames

# Specify output directory
python -m chess_video_analyzer.cli.main path/to/video.mp4 --output results

# Process at specific FPS
python -m chess_video_analyzer.cli.main path/to/video.mp4 --fps 2

# Process a specific time range
python -m chess_video_analyzer.cli.main path/to/video.mp4 --start 10 --end 60
```

### Options

- `video_path`: Path to the video file
- `--output`, `-o`: Output directory for results (default: "output")
- `--pgn`: Generate PGN output
- `--fen`: Generate FEN output
- `--visualize`, `-v`: Show visualization during processing
- `--save-frames`: Save processed frames
- `--fps`: Target frames per second for processing (default: 1.0)
- `--start`: Start time in seconds (default: 0.0)
- `--end`: End time in seconds (default: None)

## Project Structure

```
chess_video_analyzer/
├── __init__.py
├── video/
│   ├── __init__.py
│   ├── input.py       # Video input handling
│   └── frame.py       # Frame extraction and processing
├── board/
│   ├── __init__.py
│   ├── detector.py    # Chess board detection
│   └── normalizer.py  # Board normalization
├── position/
│   ├── __init__.py
│   ├── extractor.py   # Position extraction
│   └── validator.py   # Position validation
├── moves/
│   ├── __init__.py
│   └── tracker.py     # Move tracking
├── notation/
│   ├── __init__.py
│   └── generator.py   # PGN/FEN generation
├── cli/
│   ├── __init__.py
│   └── main.py        # Command-line interface
└── utils/
    ├── __init__.py
    └── visualization.py  # Visualization utilities
```

## Development

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=chess_video_analyzer
```

### Code Quality

```bash
# Format code
black chess_video_analyzer

# Check types
mypy chess_video_analyzer

# Lint code
flake8 chess_video_analyzer
```

## Limitations

- The current implementation works best with clear, well-lit videos of standard chess boards
- Performance may vary depending on video quality, lighting conditions, and board/piece styles
- The piece recognition is basic and may not work well with all chess piece designs
- Real-time processing performance depends on the hardware capabilities

## Future Improvements

- Improved piece recognition using machine learning
- Support for more board and piece styles
- Better handling of different lighting conditions and camera angles
- Real-time streaming support
- Web interface for easier use
- Integration with chess engines for analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.
