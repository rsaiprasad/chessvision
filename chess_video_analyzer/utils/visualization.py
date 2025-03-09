"""
Visualization utilities for chess video analyzer.
"""

import cv2
import numpy as np
import chess
from typing import Dict, List, Optional, Tuple


class Visualizer:
    """
    Provides visualization utilities for chess video analyzer.
    """

    def __init__(self, board_size: int = 400):
        """
        Initialize the visualizer.

        Args:
            board_size: Size of the chess board visualization
        """
        self.board_size = board_size
        self.cell_size = board_size // 8
        
        # Colors
        self.white_color = (240, 240, 240)
        self.black_color = (125, 135, 150)
        self.highlight_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.move_color = (0, 0, 255)

    def draw_board(self, board: chess.Board) -> np.ndarray:
        """
        Draw a chess board visualization.

        Args:
            board: Chess board

        Returns:
            np.ndarray: Board visualization image
        """
        # Create empty board image
        board_img = np.zeros((self.board_size, self.board_size, 3), dtype=np.uint8)
        
        # Draw cells
        for row in range(8):
            for col in range(8):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Determine cell color
                if (row + col) % 2 == 0:
                    color = self.white_color
                else:
                    color = self.black_color
                    
                # Draw cell
                cv2.rectangle(board_img, (x1, y1), (x2, y2), color, -1)
                
        # Draw pieces
        for row in range(8):
            for col in range(8):
                # Convert to chess square (a8 is 0,0)
                square = chess.square(col, 7 - row)
                piece = board.piece_at(square)
                
                if piece:
                    x = col * self.cell_size
                    y = row * self.cell_size
                    self._draw_piece(board_img, piece, x, y)
                    
        return board_img

    def _draw_piece(self, img: np.ndarray, piece: chess.Piece, x: int, y: int) -> None:
        """
        Draw a chess piece on the board image.

        Args:
            img: Board image
            piece: Chess piece
            x: X coordinate
            y: Y coordinate
        """
        # This is a simple text-based representation
        # In a real implementation, this would use piece images
        
        # Determine piece symbol and color
        symbol = piece.symbol()
        if piece.color == chess.WHITE:
            text_color = (0, 0, 0)
        else:
            text_color = (50, 50, 50)
            
        # Draw piece symbol
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        thickness = 2
        
        # Center the text in the cell
        text_size = cv2.getTextSize(symbol, font, font_scale, thickness)[0]
        text_x = x + (self.cell_size - text_size[0]) // 2
        text_y = y + (self.cell_size + text_size[1]) // 2
        
        # Draw white background for better visibility
        if piece.color == chess.BLACK:
            cv2.putText(img, symbol, (text_x, text_y), font, font_scale, (255, 255, 255), thickness + 2)
            
        cv2.putText(img, symbol, (text_x, text_y), font, font_scale, text_color, thickness)

    def highlight_square(self, img: np.ndarray, square: chess.Square, color: Tuple[int, int, int] = None) -> np.ndarray:
        """
        Highlight a square on the board image.

        Args:
            img: Board image
            square: Chess square
            color: Highlight color (default: self.highlight_color)

        Returns:
            np.ndarray: Board image with highlighted square
        """
        if color is None:
            color = self.highlight_color
            
        # Get square coordinates
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        # Create a copy of the image
        result = img.copy()
        
        # Draw highlight
        cv2.rectangle(result, (x1, y1), (x2, y2), color, 3)
        
        return result

    def highlight_move(self, img: np.ndarray, move: chess.Move) -> np.ndarray:
        """
        Highlight a move on the board image.

        Args:
            img: Board image
            move: Chess move

        Returns:
            np.ndarray: Board image with highlighted move
        """
        # Create a copy of the image
        result = img.copy()
        
        # Highlight from square
        from_col = chess.square_file(move.from_square)
        from_row = 7 - chess.square_rank(move.from_square)
        
        from_x1 = from_col * self.cell_size
        from_y1 = from_row * self.cell_size
        from_x2 = from_x1 + self.cell_size
        from_y2 = from_y1 + self.cell_size
        
        cv2.rectangle(result, (from_x1, from_y1), (from_x2, from_y2), self.move_color, 3)
        
        # Highlight to square
        to_col = chess.square_file(move.to_square)
        to_row = 7 - chess.square_rank(move.to_square)
        
        to_x1 = to_col * self.cell_size
        to_y1 = to_row * self.cell_size
        to_x2 = to_x1 + self.cell_size
        to_y2 = to_y1 + self.cell_size
        
        cv2.rectangle(result, (to_x1, to_y1), (to_x2, to_y2), self.move_color, 3)
        
        # Draw arrow
        from_center_x = from_x1 + self.cell_size // 2
        from_center_y = from_y1 + self.cell_size // 2
        to_center_x = to_x1 + self.cell_size // 2
        to_center_y = to_y1 + self.cell_size // 2
        
        cv2.arrowedLine(result, (from_center_x, from_center_y), (to_center_x, to_center_y), self.move_color, 2)
        
        return result

    def draw_coordinates(self, img: np.ndarray) -> np.ndarray:
        """
        Draw board coordinates on the image.

        Args:
            img: Board image

        Returns:
            np.ndarray: Board image with coordinates
        """
        # Create a copy of the image
        result = img.copy()
        
        # Draw file coordinates (a-h)
        for col in range(8):
            file_label = chr(ord('a') + col)
            x = col * self.cell_size + self.cell_size // 2
            y = self.board_size - 5
            
            cv2.putText(result, file_label, (x - 5, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 1)
            
        # Draw rank coordinates (1-8)
        for row in range(8):
            rank_label = str(8 - row)
            x = 5
            y = row * self.cell_size + self.cell_size // 2 + 5
            
            cv2.putText(result, rank_label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 1)
            
        return result

    def create_side_by_side(self, img1: np.ndarray, img2: np.ndarray, labels: Optional[Tuple[str, str]] = None) -> np.ndarray:
        """
        Create a side-by-side visualization of two images.

        Args:
            img1: First image
            img2: Second image
            labels: Optional labels for the images

        Returns:
            np.ndarray: Side-by-side visualization
        """
        # Resize images to the same height if needed
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        target_height = max(h1, h2)
        
        if h1 != target_height:
            scale = target_height / h1
            img1 = cv2.resize(img1, (int(w1 * scale), target_height))
            
        if h2 != target_height:
            scale = target_height / h2
            img2 = cv2.resize(img2, (int(w2 * scale), target_height))
            
        # Create side-by-side image
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        result = np.zeros((target_height, w1 + w2, 3), dtype=np.uint8)
        result[:, :w1] = img1
        result[:, w1:w1+w2] = img2
        
        # Add labels if provided
        if labels:
            label1, label2 = labels
            
            cv2.putText(result, label1, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(result, label2, (w1 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        return result

    def add_text_overlay(self, img: np.ndarray, text: str, position: Tuple[int, int] = None) -> np.ndarray:
        """
        Add a text overlay to an image.

        Args:
            img: Input image
            text: Text to add
            position: Position of the text (default: bottom-left)

        Returns:
            np.ndarray: Image with text overlay
        """
        # Create a copy of the image
        result = img.copy()
        
        # Set default position if not provided
        if position is None:
            position = (10, img.shape[0] - 20)
            
        # Add text background for better visibility
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x, text_y = position
        
        cv2.rectangle(
            result,
            (text_x - 5, text_y - text_size[1] - 5),
            (text_x + text_size[0] + 5, text_y + 5),
            (0, 0, 0),
            -1
        )
        
        # Add text
        cv2.putText(result, text, position, font, font_scale, (255, 255, 255), thickness)
        
        return result
