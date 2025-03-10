"""
Chess board normalization module for chess vision library.
"""

import cv2
import numpy as np
from typing import List, Optional, Tuple


class BoardNormalizer:
    """
    Normalizes chess board images for position extraction.
    """

    def __init__(self, target_size: int = 800):
        """
        Initialize the board normalizer.

        Args:
            target_size: Target size for the normalized board (square)
        """
        self.target_size = target_size

    def normalize_board(self, board_img: np.ndarray) -> np.ndarray:
        """
        Normalize the board image for consistent processing.

        Args:
            board_img: Input board image

        Returns:
            np.ndarray: Normalized board image
        """
        if board_img is None:
            raise ValueError("Board image cannot be None")
            
        # Resize to target size
        normalized = cv2.resize(board_img, (self.target_size, self.target_size))
        
        return normalized

    def enhance_board(self, board_img: np.ndarray) -> np.ndarray:
        """
        Enhance the board image for better position extraction.

        Args:
            board_img: Input board image

        Returns:
            np.ndarray: Enhanced board image
        """
        # Convert to grayscale if needed
        if len(board_img.shape) == 3:
            gray = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = board_img.copy()
            
        # Apply histogram equalization
        equalized = cv2.equalizeHist(gray)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh

    def create_grid(self, board_img: np.ndarray) -> List[List[np.ndarray]]:
        """
        Create a grid of cell images from the board.

        Args:
            board_img: Normalized board image

        Returns:
            List[List[np.ndarray]]: Grid of cell images
        """
        height, width = board_img.shape[:2]
        cell_size = height // 8  # Assuming square board
        
        grid = []
        for row in range(8):
            grid_row = []
            for col in range(8):
                # Extract cell image
                y = row * cell_size
                x = col * cell_size
                cell = board_img[y:y+cell_size, x:x+cell_size]
                grid_row.append(cell)
            grid.append(grid_row)
            
        return grid

    def get_cell_color(self, row: int, col: int) -> str:
        """
        Get the color of a cell based on its position.

        Args:
            row: Row index (0-7)
            col: Column index (0-7)

        Returns:
            str: 'white' or 'black'
        """
        return 'white' if (row + col) % 2 == 0 else 'black'

    def adjust_brightness_contrast(
        self, img: np.ndarray, brightness: float = 0, contrast: float = 1
    ) -> np.ndarray:
        """
        Adjust brightness and contrast of an image.

        Args:
            img: Input image
            brightness: Brightness adjustment (-1 to 1)
            contrast: Contrast adjustment (0 to 3)

        Returns:
            np.ndarray: Adjusted image
        """
        # Convert brightness from -1:1 to 0:100
        beta = int(brightness * 100)
        
        # Convert contrast from 0:3 to 0:300
        alpha = contrast * 100
        
        # Apply brightness and contrast adjustment
        adjusted = cv2.convertScaleAbs(img, alpha=alpha/100, beta=beta)
        
        return adjusted

    def detect_board_orientation(self, board_img: np.ndarray) -> float:
        """
        Detect the orientation of the board.

        Args:
            board_img: Input board image

        Returns:
            float: Rotation angle in degrees
        """
        # Convert to grayscale if needed
        if len(board_img.shape) == 3:
            gray = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = board_img.copy()
            
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        if lines is None:
            return 0.0
            
        # Calculate the dominant angle
        angles = []
        for line in lines:
            rho, theta = line[0]
            # Convert theta to degrees and normalize to -90 to 90
            angle = np.degrees(theta) % 180
            if angle > 90:
                angle -= 180
            angles.append(angle)
            
        # Find the most common angle
        angles = np.array(angles)
        hist, bins = np.histogram(angles, bins=180)
        dominant_angle = bins[np.argmax(hist)]
        
        return dominant_angle

    def rotate_board(self, board_img: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate the board image by the given angle.

        Args:
            board_img: Input board image
            angle: Rotation angle in degrees

        Returns:
            np.ndarray: Rotated board image
        """
        height, width = board_img.shape[:2]
        center = (width // 2, height // 2)
        
        # Get rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Apply rotation
        rotated = cv2.warpAffine(board_img, M, (width, height), flags=cv2.INTER_LINEAR)
        
        return rotated
