"""
Chess position extraction module for chess video analyzer.
"""

import cv2
import numpy as np
import chess
from typing import Dict, List, Optional, Tuple


class PositionExtractor:
    """
    Extracts chess positions from board images.
    """

    def __init__(self):
        """
        Initialize the position extractor.
        """
        # Piece detection thresholds
        self.piece_threshold = 0.7
        
        # Initialize piece templates (would be loaded from files in a real implementation)
        self.piece_templates = {}
        
        # Initialize the board
        self.board = chess.Board()

    def extract_position(self, board_img: np.ndarray, grid: List[List[np.ndarray]]) -> chess.Board:
        """
        Extract the chess position from a board image.

        Args:
            board_img: Normalized board image
            grid: Grid of cell images

        Returns:
            chess.Board: Chess board with the detected position
        """
        # Create a new board
        board = chess.Board()
        board.clear()  # Clear all pieces
        
        # Process each cell in the grid
        for row in range(8):
            for col in range(8):
                cell_img = grid[row][col]
                piece = self.detect_piece(cell_img)
                
                if piece:
                    # Convert row, col to chess square (a8 is 0,0)
                    square = chess.square(col, 7 - row)
                    board.set_piece_at(square, chess.Piece.from_symbol(piece))
                    
        return board

    def detect_piece(self, cell_img: np.ndarray) -> Optional[str]:
        """
        Detect a chess piece in a cell image.

        Args:
            cell_img: Cell image

        Returns:
            Optional[str]: Piece symbol (K, Q, R, B, N, P, k, q, r, b, n, p) or None if empty
        """
        # This is a placeholder implementation
        # In a real implementation, this would use template matching or ML-based detection
        
        # Convert to grayscale if needed
        if len(cell_img.shape) == 3:
            gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = cell_img.copy()
            
        # Calculate the average pixel value
        avg_value = np.mean(gray)
        
        # Calculate the standard deviation
        std_dev = np.std(gray)
        
        # If the cell has high standard deviation, it likely contains a piece
        if std_dev > 40:
            # Determine if it's a white or black piece based on average value
            if avg_value > 128:
                return 'P'  # Placeholder: white pawn
            else:
                return 'p'  # Placeholder: black pawn
                
        return None  # Empty cell

    def get_fen(self, board: chess.Board) -> str:
        """
        Get the FEN representation of the board.

        Args:
            board: Chess board

        Returns:
            str: FEN string
        """
        return board.fen()

    def validate_position(self, board: chess.Board) -> bool:
        """
        Validate the extracted position.

        Args:
            board: Chess board

        Returns:
            bool: True if valid, False otherwise
        """
        # Check if the position is valid
        # This is a simplified validation
        
        # Count pieces
        piece_counts = {
            'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0,
            'k': 0, 'q': 0, 'r': 0, 'b': 0, 'n': 0, 'p': 0
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_counts[piece.symbol()] += 1
                
        # Basic validation rules
        if piece_counts['K'] != 1 or piece_counts['k'] != 1:
            return False  # Must have exactly one king of each color
            
        if piece_counts['K'] == 0 or piece_counts['k'] == 0:
            return False  # Both kings must be present
            
        if piece_counts['P'] > 8 or piece_counts['p'] > 8:
            return False  # Maximum 8 pawns per side
            
        # More validation could be added here
        
        return True

    def improve_position(self, board: chess.Board) -> chess.Board:
        """
        Improve the extracted position using chess rules.

        Args:
            board: Chess board

        Returns:
            chess.Board: Improved chess board
        """
        # This is a placeholder for position improvement logic
        # In a real implementation, this would use chess rules to correct errors
        
        # For now, just return the original board
        return board

    def draw_position(self, board_img: np.ndarray, board: chess.Board) -> np.ndarray:
        """
        Draw the detected position on the board image.

        Args:
            board_img: Board image
            board: Chess board

        Returns:
            np.ndarray: Board image with position overlay
        """
        result = board_img.copy()
        height, width = result.shape[:2]
        cell_size = height // 8
        
        # Draw pieces
        for row in range(8):
            for col in range(8):
                # Convert row, col to chess square (a8 is 0,0)
                square = chess.square(col, 7 - row)
                piece = board.piece_at(square)
                
                if piece:
                    # Calculate cell position
                    x = col * cell_size
                    y = row * cell_size
                    
                    # Draw piece symbol
                    cv2.putText(
                        result,
                        piece.symbol(),
                        (x + cell_size // 3, y + cell_size // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )
                    
        return result

    def compare_positions(self, prev_board: chess.Board, curr_board: chess.Board) -> Optional[chess.Move]:
        """
        Compare two positions to detect a move.

        Args:
            prev_board: Previous board position
            curr_board: Current board position

        Returns:
            Optional[chess.Move]: Detected move or None if no move detected
        """
        # Find differences between the boards
        changes = []
        
        for square in chess.SQUARES:
            prev_piece = prev_board.piece_at(square)
            curr_piece = curr_board.piece_at(square)
            
            if prev_piece != curr_piece:
                changes.append((square, prev_piece, curr_piece))
                
        # Analyze changes to determine the move
        if len(changes) == 2:
            # Simple move: one piece disappears, another appears
            from_square = None
            to_square = None
            
            for square, prev_piece, curr_piece in changes:
                if prev_piece and not curr_piece:
                    from_square = square
                elif not prev_piece and curr_piece:
                    to_square = square
                    
            if from_square is not None and to_square is not None:
                return chess.Move(from_square, to_square)
                
        # More complex moves (castling, en passant, promotion) would need more logic
        
        return None
