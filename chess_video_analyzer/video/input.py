"""
Video input handling module for chess video analyzer.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Iterator, Optional, Tuple


class VideoInput:
    """
    Handles video input from files or streams.
    """

    def __init__(self, source: str):
        """
        Initialize the video input handler.

        Args:
            source: Path to video file or stream URL
        """
        self.source = source
        self.cap = None
        self.width = 0
        self.height = 0
        self.fps = 0
        self.frame_count = 0

    def open(self) -> bool:
        """
        Open the video source.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.source)
            if not self.cap.isOpened():
                print(f"Error: Could not open video source {self.source}")
                return False

            # Get video properties
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

            return True
        except Exception as e:
            print(f"Error opening video source: {e}")
            return False

    def close(self) -> None:
        """
        Close the video source.
        """
        if self.cap is not None:
            self.cap.release()

    def get_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Get the next frame from the video.

        Returns:
            Tuple[bool, Optional[np.ndarray]]: Success flag and frame (if successful)
        """
        if self.cap is None or not self.cap.isOpened():
            return False, None

        ret, frame = self.cap.read()
        if not ret:
            return False, None

        return True, frame

    def get_frames(self) -> Iterator[np.ndarray]:
        """
        Generator that yields frames from the video.

        Yields:
            np.ndarray: Video frame
        """
        if not self.open():
            return

        try:
            while True:
                ret, frame = self.get_frame()
                if not ret:
                    break
                yield frame
        finally:
            self.close()

    def get_video_info(self) -> dict:
        """
        Get information about the video.

        Returns:
            dict: Video information
        """
        return {
            "source": self.source,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "frame_count": self.frame_count,
        }

    @staticmethod
    def is_valid_video_file(file_path: str) -> bool:
        """
        Check if the given file is a valid video file.

        Args:
            file_path: Path to the file

        Returns:
            bool: True if valid, False otherwise
        """
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            return False

        # Check file extension
        valid_extensions = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
        if path.suffix.lower() not in valid_extensions:
            return False

        # Try opening the file
        cap = cv2.VideoCapture(str(path))
        is_valid = cap.isOpened()
        cap.release()

        return is_valid
