"""
Chess move tracking module for chess video analyzer.
"""

import chess
from typing import Dict, List, Optional, Tuple


class MoveTracker:
    """
    Tracks chess moves between consecutive positions.
    """

    def __init__(self):
        """
        Initialize the move tracker.
        """
        self.previous_board = None
        self.current_board = None
        self.moves = []

    def set_initial_position(self, board: chess.Board) -> None:
        """
        Set the initial position for move tracking.

        Args:
            board: Chess board
        """
        self.previous_board = board.copy()
        self.current_board = board.copy()
        self.moves = []

    def track_move(self, new_board: chess.Board) -> Optional[chess.Move]:
        """
        Track a move between the current position and a new position.

        Args:
            new_board: New chess board position

        Returns:
            Optional[chess.Move]: Detected move or None if no move detected
        """
        if self.current_board is None:
            self.current_board = new_board.copy()
            return None
            
        # Update board references
        self.previous_board = self.current_board.copy()
        self.current_board = new_board.copy()
        
        # Detect the move
        move = self._detect_move()
        
        if move:
            self.moves.append(move)
            
        return move

    def _detect_move(self) -> Optional[chess.Move]:
        """
        Detect a move between the previous and current positions.

        Returns:
            Optional[chess.Move]: Detected move or None if no move detected
        """
        # Find differences between the boards
        changes = []
        
        for square in chess.SQUARES:
            prev_piece = self.previous_board.piece_at(square)
            curr_piece = self.current_board.piece_at(square)
            
            if prev_piece != curr_piece:
                changes.append((square, prev_piece, curr_piece))
                
        # Analyze changes to determine the move
        if len(changes) == 0:
            return None  # No changes
            
        if len(changes) == 2:
            # Simple move: one piece disappears, another appears
            from_square = None
            to_square = None
            moving_piece = None
            
            for square, prev_piece, curr_piece in changes:
                if prev_piece and not curr_piece:
                    from_square = square
                    moving_piece = prev_piece
                elif not prev_piece and curr_piece:
                    to_square = square
                    
            if from_square is not None and to_square is not None and moving_piece is not None:
                # Check if this is a promotion
                if moving_piece.piece_type == chess.PAWN:
                    to_rank = chess.square_rank(to_square)
                    if (moving_piece.color == chess.WHITE and to_rank == 7) or \
                       (moving_piece.color == chess.BLACK and to_rank == 0):
                        # This is a promotion
                        promoted_piece = self.current_board.piece_at(to_square)
                        if promoted_piece:
                            promotion_piece_type = promoted_piece.piece_type
                            return chess.Move(from_square, to_square, promotion=promotion_piece_type)
                
                return chess.Move(from_square, to_square)
                
        # Handle castling
        if len(changes) == 4:
            # Potential castling: king and rook move
            king_from = None
            king_to = None
            rook_from = None
            rook_to = None
            
            for square, prev_piece, curr_piece in changes:
                if prev_piece and prev_piece.piece_type == chess.KING and not curr_piece:
                    king_from = square
                elif not prev_piece and curr_piece and curr_piece.piece_type == chess.KING:
                    king_to = square
                elif prev_piece and prev_piece.piece_type == chess.ROOK and not curr_piece:
                    rook_from = square
                elif not prev_piece and curr_piece and curr_piece.piece_type == chess.ROOK:
                    rook_to = square
                    
            if king_from and king_to and rook_from and rook_to:
                # Check if this is a castling move
                king_file_diff = abs(chess.square_file(king_from) - chess.square_file(king_to))
                
                if king_file_diff == 2:
                    # This is likely castling
                    return chess.Move(king_from, king_to)
                    
        # Handle en passant
        if len(changes) == 3:
            # Potential en passant: pawn moves diagonally and another pawn disappears
            pawn_from = None
            pawn_to = None
            captured_square = None
            
            for square, prev_piece, curr_piece in changes:
                if prev_piece and prev_piece.piece_type == chess.PAWN and not curr_piece:
                    pawn_from = square
                elif not prev_piece and curr_piece and curr_piece.piece_type == chess.PAWN:
                    pawn_to = square
                elif prev_piece and prev_piece.piece_type == chess.PAWN and not curr_piece:
                    captured_square = square
                    
            if pawn_from and pawn_to and captured_square:
                # Check if this is an en passant capture
                from_file = chess.square_file(pawn_from)
                to_file = chess.square_file(pawn_to)
                
                if abs(from_file - to_file) == 1:
                    return chess.Move(pawn_from, pawn_to)
                    
        # If we can't determine the move, try legal moves
        return self._find_legal_move()

    def _find_legal_move(self) -> Optional[chess.Move]:
        """
        Find a legal move that transforms the previous position into the current position.

        Returns:
            Optional[chess.Move]: Legal move or None if no matching move found
        """
        # Get all legal moves from the previous position
        legal_moves = list(self.previous_board.legal_moves)
        
        # Try each legal move
        for move in legal_moves:
            test_board = self.previous_board.copy()
            test_board.push(move)
            
            # Check if the resulting position matches the current position
            if self._compare_boards(test_board, self.current_board):
                return move
                
        return None

    def _compare_boards(self, board1: chess.Board, board2: chess.Board) -> bool:
        """
        Compare two chess boards to see if they represent the same position.

        Args:
            board1: First chess board
            board2: Second chess board

        Returns:
            bool: True if the boards represent the same position, False otherwise
        """
        # Compare piece placement
        for square in chess.SQUARES:
            piece1 = board1.piece_at(square)
            piece2 = board2.piece_at(square)
            
            if piece1 != piece2:
                return False
                
        return True

    def get_moves(self) -> List[chess.Move]:
        """
        Get the list of tracked moves.

        Returns:
            List[chess.Move]: List of moves
        """
        return self.moves.copy()

    def get_pgn(self) -> str:
        """
        Get the PGN representation of the tracked moves.

        Returns:
            str: PGN string
        """
        if not self.moves:
            return ""
            
        # Create a new board for PGN generation
        board = chess.Board()
        pgn_moves = []
        
        for i, move in enumerate(self.moves):
            # Add move number for white's moves
            if i % 2 == 0:
                move_num = i // 2 + 1
                pgn_moves.append(f"{move_num}.")
                
            # Add the move in SAN notation
            pgn_moves.append(board.san(move))
            
            # Apply the move to the board
            board.push(move)
            
        return " ".join(pgn_moves)

    def get_fen(self) -> str:
        """
        Get the FEN representation of the current position.

        Returns:
            str: FEN string
        """
        if self.current_board:
            return self.current_board.fen()
        return chess.Board().fen()
