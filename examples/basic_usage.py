"""
Basic usage example for the Chess Video Analyzer.
"""

import argparse
import cv2
import os
import sys
from pathlib import Path

import chess

from chess_video_analyzer.video.input import VideoInput
from chess_video_analyzer.video.frame import FrameExtractor
from chess_video_analyzer.board.detector import BoardDetector
from chess_video_analyzer.board.normalizer import BoardNormalizer
from chess_video_analyzer.position.extractor import PositionExtractor
from chess_video_analyzer.position.validator import PositionValidator
from chess_video_analyzer.moves.tracker import MoveTracker
from chess_video_analyzer.notation.generator import NotationGenerator
from chess_video_analyzer.utils.visualization import Visualizer


def main():
    """Main function."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Chess Video Analyzer Example")
    parser.add_argument("video_path", help="Path to the video file")
    args = parser.parse_args()
    
    # Check if the video file exists
    if not os.path.exists(args.video_path):
        print(f"Error: Video file not found: {args.video_path}")
        sys.exit(1)
        
    # Initialize components
    video_input = VideoInput(args.video_path)
    frame_extractor = FrameExtractor(target_fps=1.0)  # Process 1 frame per second
    board_detector = BoardDetector()
    board_normalizer = BoardNormalizer()
    position_extractor = PositionExtractor()
    position_validator = PositionValidator()
    move_tracker = MoveTracker()
    notation_generator = NotationGenerator()
    visualizer = Visualizer()
    
    # Open video
    if not video_input.open():
        print(f"Error: Could not open video file {args.video_path}")
        sys.exit(1)
        
    print(f"Processing video: {args.video_path}")
    print(f"Video properties: {video_input.width}x{video_input.height}, {video_input.fps} FPS")
    
    # Set frame interval based on video FPS
    frame_extractor.set_frame_interval(video_input.fps)
    
    # Process frames
    frame_count = 0
    detected_positions = []
    
    # Create a window for visualization
    cv2.namedWindow("Chess Video Analyzer Example", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Chess Video Analyzer Example", 1200, 600)
    
    print("\nPress 'q' to quit, any other key to continue to the next frame")
    
    while True:
        # Get frame
        ret, frame = video_input.get_frame()
        if not ret:
            break
            
        # Process every nth frame based on frame interval
        if frame_count % frame_extractor.frame_interval == 0:
            print(f"\nProcessing frame {frame_count} ({frame_count / video_input.fps:.2f} seconds)")
            
            # Process frame
            processed_frame = frame_extractor.process_frame(frame)
            
            # Detect board
            board_contour = board_detector.detect_board(processed_frame)
            
            if board_contour is not None:
                print("Chess board detected")
                
                # Draw board contour
                contour_img = board_detector.draw_board_contour(processed_frame, board_contour)
                
                # Extract and normalize board
                board_img = board_detector.extract_board(processed_frame, board_contour)
                
                if board_img is not None:
                    # Normalize board
                    normalized_board = board_normalizer.normalize_board(board_img)
                    
                    # Create grid
                    grid = board_normalizer.create_grid(normalized_board)
                    
                    # Extract position
                    board = position_extractor.extract_position(normalized_board, grid)
                    
                    # Validate position
                    is_valid, issues = position_validator.validate_position(board)
                    
                    if is_valid:
                        print("Valid chess position detected")
                        
                        # Track move
                        if not detected_positions:
                            move_tracker.set_initial_position(board)
                            print("Initial position set")
                        else:
                            move = move_tracker.track_move(board)
                            
                            if move:
                                notation_generator.add_move(move)
                                print(f"Detected move: {board.san(move)}")
                                
                        detected_positions.append(board)
                        
                        # Draw board visualization
                        board_vis = visualizer.draw_board(board)
                        board_vis = visualizer.draw_coordinates(board_vis)
                        
                        # Add FEN overlay
                        fen = board.fen().split(" ")[0]  # Just the piece placement part
                        board_vis = visualizer.add_text_overlay(board_vis, fen)
                        
                        # Create side-by-side visualization
                        vis_img = visualizer.create_side_by_side(
                            contour_img,
                            board_vis,
                            labels=("Detected Board", "Extracted Position")
                        )
                        
                        # Show visualization
                        cv2.imshow("Chess Video Analyzer Example", vis_img)
                        
                        # Wait for key press
                        key = cv2.waitKey(0)
                        if key == ord('q'):
                            break
                    else:
                        print("Invalid chess position detected:")
                        for issue in issues:
                            print(f"  - {issue}")
                else:
                    print("Could not extract board image")
            else:
                print("No chess board detected")
                cv2.imshow("Chess Video Analyzer Example", processed_frame)
                
                # Wait for key press
                key = cv2.waitKey(0)
                if key == ord('q'):
                    break
                    
        frame_count += 1
        
    # Close video
    video_input.close()
    
    # Close visualization window
    cv2.destroyAllWindows()
    
    # Print results
    if detected_positions:
        print(f"\nDetected {len(detected_positions)} positions")
        print(f"Tracked {len(move_tracker.get_moves())} moves")
        
        # Print moves
        moves = notation_generator.get_formatted_move_list()
        print("\nDetected moves:")
        print(moves)
        
        # Print PGN
        pgn = notation_generator.get_pgn()
        print("\nPGN:")
        print(pgn)
    else:
        print("\nNo valid chess positions detected")


if __name__ == "__main__":
    main()
