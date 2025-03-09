"""
Frame extraction and processing module for chess video analyzer.
"""

import cv2
import numpy as np
from typing import List, Optional, Tuple


class FrameExtractor:
    """
    Extracts and processes frames from video for chess board detection.
    """

    def __init__(self, target_fps: Optional[float] = None, resize_dim: Optional[Tuple[int, int]] = None):
        """
        Initialize the frame extractor.

        Args:
            target_fps: Target frames per second to extract (None for all frames)
            resize_dim: Dimensions to resize frames to (width, height) or None for original size
        """
        self.target_fps = target_fps
        self.resize_dim = resize_dim
        self.frame_interval = 1  # Default to processing every frame

    def set_frame_interval(self, video_fps: float) -> None:
        """
        Set the frame interval based on the video FPS and target FPS.

        Args:
            video_fps: FPS of the input video
        """
        if self.target_fps is not None and self.target_fps > 0 and video_fps > 0:
            self.frame_interval = max(1, int(video_fps / self.target_fps))
        else:
            self.frame_interval = 1

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a single frame (resize, enhance, etc.).

        Args:
            frame: Input frame

        Returns:
            np.ndarray: Processed frame
        """
        if frame is None:
            raise ValueError("Frame cannot be None")

        # Resize if needed
        if self.resize_dim is not None:
            frame = cv2.resize(frame, self.resize_dim)

        return frame

    def extract_frames(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """
        Extract and process frames at the specified interval.

        Args:
            frames: List of input frames

        Returns:
            List[np.ndarray]: Processed frames
        """
        processed_frames = []
        
        for i, frame in enumerate(frames):
            if i % self.frame_interval == 0:
                processed_frame = self.process_frame(frame)
                processed_frames.append(processed_frame)
                
        return processed_frames

    @staticmethod
    def enhance_frame(frame: np.ndarray) -> np.ndarray:
        """
        Enhance a frame for better board detection.

        Args:
            frame: Input frame

        Returns:
            np.ndarray: Enhanced frame
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh

    @staticmethod
    def extract_key_frames(frames: List[np.ndarray], max_frames: int = 10) -> List[np.ndarray]:
        """
        Extract key frames from a list of frames.

        Args:
            frames: List of input frames
            max_frames: Maximum number of frames to extract

        Returns:
            List[np.ndarray]: Key frames
        """
        if not frames:
            return []
            
        if len(frames) <= max_frames:
            return frames
            
        # Simple approach: take evenly spaced frames
        indices = np.linspace(0, len(frames) - 1, max_frames, dtype=int)
        return [frames[i] for i in indices]
