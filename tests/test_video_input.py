"""
Tests for the VideoInput class.
"""

import os
import pytest
import tempfile
import numpy as np
import cv2
from pathlib import Path

from chess_video_analyzer.video.input import VideoInput


@pytest.fixture
def sample_video_path():
    """Create a temporary sample video file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        temp_path = f.name
        
    # Create a simple test video
    width, height = 640, 480
    fps = 30
    duration = 1  # seconds
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))
    
    # Create frames with frame numbers
    for i in range(int(fps * duration)):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Add frame number text
        cv2.putText(
            frame,
            f"Frame {i}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )
        out.write(frame)
        
    out.release()
    
    yield temp_path
    
    # Clean up
    os.unlink(temp_path)


def test_video_input_open(sample_video_path):
    """Test opening a video file."""
    video_input = VideoInput(sample_video_path)
    assert video_input.open() is True
    assert video_input.cap is not None
    assert video_input.width == 640
    assert video_input.height == 480
    assert video_input.fps == 30
    assert video_input.frame_count == 30
    video_input.close()


def test_video_input_get_frame(sample_video_path):
    """Test getting frames from a video."""
    video_input = VideoInput(sample_video_path)
    video_input.open()
    
    # Get first frame
    ret, frame = video_input.get_frame()
    assert ret is True
    assert frame is not None
    assert frame.shape == (480, 640, 3)
    
    # Get all frames
    frame_count = 0
    while True:
        ret, frame = video_input.get_frame()
        if not ret:
            break
        frame_count += 1
        
    assert frame_count == 29  # We already read one frame
    
    video_input.close()


def test_video_input_get_frames(sample_video_path):
    """Test the frame generator."""
    video_input = VideoInput(sample_video_path)
    
    frames = list(video_input.get_frames())
    assert len(frames) == 30
    assert all(frame.shape == (480, 640, 3) for frame in frames)


def test_video_input_invalid_file():
    """Test handling of invalid video files."""
    video_input = VideoInput("nonexistent_file.mp4")
    assert video_input.open() is False


def test_video_input_is_valid_video_file(sample_video_path):
    """Test video file validation."""
    assert VideoInput.is_valid_video_file(sample_video_path) is True
    assert VideoInput.is_valid_video_file("nonexistent_file.mp4") is False
    
    # Create a non-video file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"This is not a video file")
        temp_path = f.name
        
    assert VideoInput.is_valid_video_file(temp_path) is False
    
    os.unlink(temp_path)


def test_video_input_get_video_info(sample_video_path):
    """Test getting video information."""
    video_input = VideoInput(sample_video_path)
    video_input.open()
    
    info = video_input.get_video_info()
    assert info["source"] == sample_video_path
    assert info["width"] == 640
    assert info["height"] == 480
    assert info["fps"] == 30
    assert info["frame_count"] == 30
    
    video_input.close()
