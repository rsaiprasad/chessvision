"""
Chess position validation module for chess video analyzer.
"""

import chess
from typing import Dict, List, Optional, Tuple


class PositionValidator:
    """
    Validates chess positions using chess rules.
    """

    def __init__(self):
        """
        Initialize the position validator.
        """
        pass

    def validate_position(self, board: chess.Board) -> Tuple[bool, List[str]]:
        """
        Validate a chess position using chess rules.

        Args:
            board: Chess board

        Returns:
            Tuple[bool, List[str]]: Validation result and list of issues
        """
        issues = []
        
        # Check kings
        if not self._validate_kings(board, issues):
            return False, issues
            
        # Check piece counts
        if not self._validate_piece_counts(board, issues):
            return False, issues
            
        # Check pawn placement
        if not self._validate_pawn_placement(board, issues):
            return False, issues
            
        # Check if the position is legal
        if not self._validate_check_state(board, issues):
            return False, issues
            
        return len(issues) == 0, issues

    def _validate_kings(self, board: chess.Board, issues: List[str]) -> bool:
        """
        Validate that there is exactly one king of each color.

        Args:
            board: Chess board
            issues: List to append issues to

        Returns:
            bool: True if valid, False otherwise
        """
        white_king_count = 0
        black_king_count = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.KING:
                if piece.color == chess.WHITE:
                    white_king_count += 1
                else:
                    black_king_count += 1
                    
        if white_king_count != 1:
            issues.append(f"Invalid white king count: {white_king_count}")
            return False
            
        if black_king_count != 1:
            issues.append(f"Invalid black king count: {black_king_count}")
            return False
            
        return True

    def _validate_piece_counts(self, board: chess.Board, issues: List[str]) -> bool:
        """
        Validate that piece counts are within legal limits.

        Args:
            board: Chess board
            issues: List to append issues to

        Returns:
            bool: True if valid, False otherwise
        """
        # Count pieces by type and color
        piece_counts = {
            chess.WHITE: {
                chess.PAWN: 0,
                chess.KNIGHT: 0,
                chess.BISHOP: 0,
                chess.ROOK: 0,
                chess.QUEEN: 0,
                chess.KING: 0
            },
            chess.BLACK: {
                chess.PAWN: 0,
                chess.KNIGHT: 0,
                chess.BISHOP: 0,
                chess.ROOK: 0,
                chess.QUEEN: 0,
                chess.KING: 0
            }
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_counts[piece.color][piece.piece_type] += 1
                
        # Check piece counts
        valid = True
        
        # Pawns: 0-8 per side
        for color in [chess.WHITE, chess.BLACK]:
            color_name = "white" if color == chess.WHITE else "black"
            
            if piece_counts[color][chess.PAWN] > 8:
                issues.append(f"Too many {color_name} pawns: {piece_counts[color][chess.PAWN]}")
                valid = False
                
            # Knights: 0-10 per side (8 pawns could be promoted)
            if piece_counts[color][chess.KNIGHT] > 10:
                issues.append(f"Too many {color_name} knights: {piece_counts[color][chess.KNIGHT]}")
                valid = False
                
            # Bishops: 0-10 per side
            if piece_counts[color][chess.BISHOP] > 10:
                issues.append(f"Too many {color_name} bishops: {piece_counts[color][chess.BISHOP]}")
                valid = False
                
            # Rooks: 0-10 per side
            if piece_counts[color][chess.ROOK] > 10:
                issues.append(f"Too many {color_name} rooks: {piece_counts[color][chess.ROOK]}")
                valid = False
                
            # Queens: 0-9 per side
            if piece_counts[color][chess.QUEEN] > 9:
                issues.append(f"Too many {color_name} queens: {piece_counts[color][chess.QUEEN]}")
                valid = False
                
            # Total pieces: max 16 per side
            total_pieces = sum(piece_counts[color].values())
            if total_pieces > 16:
                issues.append(f"Too many {color_name} pieces: {total_pieces}")
                valid = False
                
        return valid

    def _validate_pawn_placement(self, board: chess.Board, issues: List[str]) -> bool:
        """
        Validate that pawns are not on the first or last rank.

        Args:
            board: Chess board
            issues: List to append issues to

        Returns:
            bool: True if valid, False otherwise
        """
        valid = True
        
        # Check for pawns on first rank
        for file_idx in range(8):
            square = chess.square(file_idx, 0)  # a1, b1, ..., h1
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                issues.append(f"Pawn on first rank at {chess.square_name(square)}")
                valid = False
                
        # Check for pawns on last rank
        for file_idx in range(8):
            square = chess.square(file_idx, 7)  # a8, b8, ..., h8
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                issues.append(f"Pawn on last rank at {chess.square_name(square)}")
                valid = False
                
        return valid

    def _validate_check_state(self, board: chess.Board, issues: List[str]) -> bool:
        """
        Validate that the position is legal regarding check state.

        Args:
            board: Chess board
            issues: List to append issues to

        Returns:
            bool: True if valid, False otherwise
        """
        # Check if the side not to move is in check
        side_to_move = board.turn
        board.turn = not side_to_move
        
        if board.is_check():
            issues.append(f"The side not to move is in check")
            board.turn = side_to_move
            return False
            
        board.turn = side_to_move
        return True

    def suggest_corrections(self, board: chess.Board) -> chess.Board:
        """
        Suggest corrections for an invalid position.

        Args:
            board: Chess board

        Returns:
            chess.Board: Corrected chess board
        """
        # This is a placeholder for position correction logic
        # In a real implementation, this would use chess rules to suggest corrections
        
        # For now, just return the original board
        return board.copy()

    def is_reasonable_position(self, board: chess.Board) -> bool:
        """
        Check if the position is reasonable for a real game.

        Args:
            board: Chess board

        Returns:
            bool: True if reasonable, False otherwise
        """
        # This is a simplified check for a reasonable position
        
        # Count pieces
        piece_counts = {
            chess.WHITE: {
                chess.PAWN: 0,
                chess.KNIGHT: 0,
                chess.BISHOP: 0,
                chess.ROOK: 0,
                chess.QUEEN: 0,
                chess.KING: 0
            },
            chess.BLACK: {
                chess.PAWN: 0,
                chess.KNIGHT: 0,
                chess.BISHOP: 0,
                chess.ROOK: 0,
                chess.QUEEN: 0,
                chess.KING: 0
            }
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_counts[piece.color][piece.piece_type] += 1
                
        # Check if the position is reasonable
        
        # Both sides should have kings
        if piece_counts[chess.WHITE][chess.KING] != 1 or piece_counts[chess.BLACK][chess.KING] != 1:
            return False
            
        # Material difference should not be too extreme
        white_material = (
            piece_counts[chess.WHITE][chess.PAWN] * 1 +
            piece_counts[chess.WHITE][chess.KNIGHT] * 3 +
            piece_counts[chess.WHITE][chess.BISHOP] * 3 +
            piece_counts[chess.WHITE][chess.ROOK] * 5 +
            piece_counts[chess.WHITE][chess.QUEEN] * 9
        )
        
        black_material = (
            piece_counts[chess.BLACK][chess.PAWN] * 1 +
            piece_counts[chess.BLACK][chess.KNIGHT] * 3 +
            piece_counts[chess.BLACK][chess.BISHOP] * 3 +
            piece_counts[chess.BLACK][chess.ROOK] * 5 +
            piece_counts[chess.BLACK][chess.QUEEN] * 9
        )
        
        material_diff = abs(white_material - black_material)
        
        # If material difference is too large, it's probably an error
        if material_diff > 15:
            return False
            
        return True
