"""
Chess board detection module for chess video analyzer.
"""

import cv2
import numpy as np
from typing import List, Optional, Tuple


class BoardDetector:
    """
    Detects chess boards in video frames.
    """

    def __init__(self, min_board_size: float = 0.2, max_board_size: float = 0.9):
        """
        Initialize the board detector.

        Args:
            min_board_size: Minimum board size as a fraction of frame size
            max_board_size: Maximum board size as a fraction of frame size
        """
        self.min_board_size = min_board_size
        self.max_board_size = max_board_size
        self.last_board_contour = None  # Cache the last detected board contour

    def detect_board(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Detect a chess board in the given frame.

        Args:
            frame: Input frame

        Returns:
            Optional[np.ndarray]: Contour of the detected board or None if not found
        """
        # Convert to grayscale if needed
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame.copy()

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        min_area = height * width * self.min_board_size * self.min_board_size
        max_area = height * width * self.max_board_size * self.max_board_size
        
        # Find the chess board contour
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < min_area or area > max_area:
                continue
                
            # Approximate the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # Chess boards are approximately square (4 corners)
            if len(approx) == 4:
                self.last_board_contour = approx
                return approx
        
        # If no board found, return the last detected board if available
        return self.last_board_contour

    def extract_board(self, frame: np.ndarray, contour: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract and normalize the chess board from the frame.

        Args:
            frame: Input frame
            contour: Contour of the detected board

        Returns:
            Optional[np.ndarray]: Normalized chess board image or None if extraction fails
        """
        if contour is None or len(contour) != 4:
            return None
            
        # Order points in the contour (top-left, top-right, bottom-right, bottom-left)
        rect = self.order_points(contour.reshape(4, 2))
        
        # Get width and height of the board
        width_a = np.sqrt(((rect[1][0] - rect[0][0]) ** 2) + ((rect[1][1] - rect[0][1]) ** 2))
        width_b = np.sqrt(((rect[2][0] - rect[3][0]) ** 2) + ((rect[2][1] - rect[3][1]) ** 2))
        max_width = max(int(width_a), int(width_b))
        
        height_a = np.sqrt(((rect[3][0] - rect[0][0]) ** 2) + ((rect[3][1] - rect[0][1]) ** 2))
        height_b = np.sqrt(((rect[2][0] - rect[1][0]) ** 2) + ((rect[2][1] - rect[1][1]) ** 2))
        max_height = max(int(height_a), int(height_b))
        
        # Ensure the board is square
        max_size = max(max_width, max_height)
        
        # Define destination points for perspective transform
        dst = np.array([
            [0, 0],
            [max_size - 1, 0],
            [max_size - 1, max_size - 1],
            [0, max_size - 1]
        ], dtype="float32")
        
        # Calculate perspective transform matrix
        M = cv2.getPerspectiveTransform(rect, dst)
        
        # Apply perspective transform
        warped = cv2.warpPerspective(frame, M, (max_size, max_size))
        
        return warped

    @staticmethod
    def order_points(pts: np.ndarray) -> np.ndarray:
        """
        Order points in clockwise order starting from top-left.

        Args:
            pts: Input points (4x2 array)

        Returns:
            np.ndarray: Ordered points
        """
        # Initialize ordered points
        rect = np.zeros((4, 2), dtype="float32")
        
        # Top-left point has the smallest sum
        # Bottom-right point has the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Top-right point has the smallest difference
        # Bottom-left point has the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect

    def draw_board_contour(self, frame: np.ndarray, contour: np.ndarray) -> np.ndarray:
        """
        Draw the detected board contour on the frame.

        Args:
            frame: Input frame
            contour: Contour of the detected board

        Returns:
            np.ndarray: Frame with board contour drawn
        """
        if contour is None:
            return frame
            
        result = frame.copy()
        cv2.drawContours(result, [contour], 0, (0, 255, 0), 2)
        
        # Draw the corners
        for point in contour:
            x, y = point.ravel()
            cv2.circle(result, (int(x), int(y)), 5, (0, 0, 255), -1)
            
        return result

    def detect_grid(self, board_img: np.ndarray) -> List[List[Tuple[int, int, int, int]]]:
        """
        Detect the chess grid (8x8) from the normalized board image.

        Args:
            board_img: Normalized chess board image

        Returns:
            List[List[Tuple[int, int, int, int]]]: Grid cells as (x, y, w, h)
        """
        height, width = board_img.shape[:2]
        cell_size = min(height, width) // 8
        
        # Create grid cells
        grid = []
        for row in range(8):
            grid_row = []
            for col in range(8):
                x = col * cell_size
                y = row * cell_size
                grid_row.append((x, y, cell_size, cell_size))
            grid.append(grid_row)
            
        return grid

    def draw_grid(self, board_img: np.ndarray, grid: List[List[Tuple[int, int, int, int]]]) -> np.ndarray:
        """
        Draw the chess grid on the board image.

        Args:
            board_img: Normalized chess board image
            grid: Grid cells as (x, y, w, h)

        Returns:
            np.ndarray: Board image with grid drawn
        """
        result = board_img.copy()
        
        # Draw grid lines
        for row in range(8):
            for col in range(8):
                x, y, w, h = grid[row][col]
                cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 1)
                
        return result
