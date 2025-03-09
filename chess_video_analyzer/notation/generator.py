"""
Chess notation generation module for chess video analyzer.
"""

import chess
import chess.pgn
import datetime
from typing import Dict, List, Optional, Tuple


class NotationGenerator:
    """
    Generates chess notation (PGN/FEN) from tracked moves.
    """

    def __init__(self):
        """
        Initialize the notation generator.
        """
        self.moves = []
        self.headers = {
            "Event": "Chess Video Analysis",
            "Site": "Unknown",
            "Date": datetime.datetime.now().strftime("%Y.%m.%d"),
            "Round": "?",
            "White": "?",
            "Black": "?",
            "Result": "*"
        }

    def add_move(self, move: chess.Move) -> None:
        """
        Add a move to the game.

        Args:
            move: Chess move
        """
        self.moves.append(move)

    def set_moves(self, moves: List[chess.Move]) -> None:
        """
        Set the list of moves.

        Args:
            moves: List of chess moves
        """
        self.moves = moves.copy()

    def set_header(self, key: str, value: str) -> None:
        """
        Set a PGN header value.

        Args:
            key: Header key
            value: Header value
        """
        self.headers[key] = value

    def set_result(self, result: str) -> None:
        """
        Set the game result.

        Args:
            result: Game result (1-0, 0-1, 1/2-1/2, or *)
        """
        if result in ["1-0", "0-1", "1/2-1/2", "*"]:
            self.headers["Result"] = result

    def get_pgn(self, include_headers: bool = True) -> str:
        """
        Get the PGN representation of the game.

        Args:
            include_headers: Whether to include PGN headers

        Returns:
            str: PGN string
        """
        if not self.moves:
            return ""
            
        # Create a new game
        game = chess.pgn.Game()
        
        # Set headers
        if include_headers:
            for key, value in self.headers.items():
                game.headers[key] = value
                
        # Add moves
        node = game
        board = chess.Board()
        
        for move in self.moves:
            node = node.add_variation(move)
            board.push(move)
            
        # Set result
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                self.headers["Result"] = "0-1"
            else:
                self.headers["Result"] = "1-0"
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_fifty_moves() or board.is_repetition():
            self.headers["Result"] = "1/2-1/2"
            
        if include_headers:
            game.headers["Result"] = self.headers["Result"]
            
        # Generate PGN string
        pgn_string = str(game)
        
        return pgn_string

    def get_fen(self, move_index: Optional[int] = None) -> str:
        """
        Get the FEN representation of the position after a specific move.

        Args:
            move_index: Index of the move (None for the final position)

        Returns:
            str: FEN string
        """
        board = chess.Board()
        
        if not self.moves:
            return board.fen()
            
        if move_index is None:
            move_index = len(self.moves)
            
        move_index = min(move_index, len(self.moves))
        
        for i in range(move_index):
            board.push(self.moves[i])
            
        return board.fen()

    def get_move_list(self) -> List[str]:
        """
        Get a list of moves in SAN notation.

        Returns:
            List[str]: List of moves in SAN notation
        """
        if not self.moves:
            return []
            
        board = chess.Board()
        move_list = []
        
        for move in self.moves:
            san = board.san(move)
            move_list.append(san)
            board.push(move)
            
        return move_list

    def get_move_pairs(self) -> List[Tuple[str, Optional[str]]]:
        """
        Get a list of move pairs (white move, black move).

        Returns:
            List[Tuple[str, Optional[str]]]: List of move pairs
        """
        move_list = self.get_move_list()
        move_pairs = []
        
        for i in range(0, len(move_list), 2):
            white_move = move_list[i]
            black_move = move_list[i + 1] if i + 1 < len(move_list) else None
            move_pairs.append((white_move, black_move))
            
        return move_pairs

    def get_formatted_move_list(self) -> str:
        """
        Get a formatted move list with move numbers.

        Returns:
            str: Formatted move list
        """
        move_pairs = self.get_move_pairs()
        formatted_list = []
        
        for i, (white_move, black_move) in enumerate(move_pairs):
            move_num = i + 1
            if black_move:
                formatted_list.append(f"{move_num}. {white_move} {black_move}")
            else:
                formatted_list.append(f"{move_num}. {white_move}")
                
        return " ".join(formatted_list)

    def export_pgn(self, file_path: str) -> bool:
        """
        Export the game to a PGN file.

        Args:
            file_path: Path to the output file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, "w") as f:
                f.write(self.get_pgn())
            return True
        except Exception as e:
            print(f"Error exporting PGN: {e}")
            return False

    def export_fen(self, file_path: str) -> bool:
        """
        Export the final position to a FEN file.

        Args:
            file_path: Path to the output file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, "w") as f:
                f.write(self.get_fen())
            return True
        except Exception as e:
            print(f"Error exporting FEN: {e}")
            return False
