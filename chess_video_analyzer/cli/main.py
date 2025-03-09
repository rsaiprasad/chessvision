"""
Command-line interface for chess video analyzer.
"""

import argparse
import cv2
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Chess Video Analyzer")
    
    parser.add_argument(
        "video_path",
        type=str,
        help="Path to the video file"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output",
        help="Output directory for results"
    )
    
    parser.add_argument(
        "--pgn",
        action="store_true",
        help="Generate PGN output"
    )
    
    parser.add_argument(
        "--fen",
        action="store_true",
        help="Generate FEN output"
    )
    
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        help="Show visualization during processing"
    )
    
    parser.add_argument(
        "--save-frames",
        action="store_true",
        help="Save processed frames"
    )
    
    parser.add_argument(
        "--fps",
        type=float,
        default=1.0,
        help="Target frames per second for processing"
    )
    
    parser.add_argument(
        "--start",
        type=float,
        default=0.0,
        help="Start time in seconds"
    )
    
    parser.add_argument(
        "--end",
        type=float,
        default=None,
        help="End time in seconds"
    )
    
    return parser.parse_args()


def process_video(args):
    """Process the video file."""
    # Create output directory if it doesn't exist
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    video_input = VideoInput(args.video_path)
    frame_extractor = FrameExtractor(target_fps=args.fps)
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
        return False
        
    # Set frame interval based on video FPS
    frame_extractor.set_frame_interval(video_input.fps)
    
    # Calculate start and end frames
    start_frame = int(args.start * video_input.fps)
    end_frame = int(args.end * video_input.fps) if args.end is not None else None
    
    # Skip to start frame
    frame_count = 0
    while frame_count < start_frame:
        ret, _ = video_input.get_frame()
        if not ret:
            print(f"Error: Could not skip to start frame {start_frame}")
            return False
        frame_count += 1
        
    # Process frames
    processed_frames = 0
    detected_positions = []
    
    print(f"Processing video: {args.video_path}")
    print(f"Video properties: {video_input.width}x{video_input.height}, {video_input.fps} FPS")
    print(f"Target processing FPS: {args.fps}")
    
    while True:
        # Get frame
        ret, frame = video_input.get_frame()
        if not ret or (end_frame is not None and frame_count >= end_frame):
            break
            
        # Process every nth frame based on frame interval
        if frame_count % frame_extractor.frame_interval == 0:
            print(f"Processing frame {frame_count} ({frame_count / video_input.fps:.2f} seconds)")
            
            # Process frame
            processed_frame = frame_extractor.process_frame(frame)
            
            # Detect board
            board_contour = board_detector.detect_board(processed_frame)
            
            if board_contour is not None:
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
                        # Track move
                        if not detected_positions:
                            move_tracker.set_initial_position(board)
                        else:
                            move = move_tracker.track_move(board)
                            
                            if move:
                                notation_generator.add_move(move)
                                print(f"Detected move: {board.san(move)}")
                                
                        detected_positions.append(board)
                        
                        # Save frame if requested
                        if args.save_frames:
                            frame_path = output_dir / f"frame_{frame_count:06d}.jpg"
                            
                            # Create visualization
                            board_vis = visualizer.draw_board(board)
                            board_vis = visualizer.draw_coordinates(board_vis)
                            
                            # Add FEN overlay
                            fen = board.fen().split(" ")[0]  # Just the piece placement part
                            board_vis = visualizer.add_text_overlay(board_vis, fen)
                            
                            # Create side-by-side visualization
                            vis_img = visualizer.create_side_by_side(
                                processed_frame,
                                board_vis,
                                labels=("Video Frame", "Detected Position")
                            )
                            
                            cv2.imwrite(str(frame_path), vis_img)
                            
                        # Show visualization if requested
                        if args.visualize:
                            # Draw board contour
                            contour_img = board_detector.draw_board_contour(processed_frame, board_contour)
                            
                            # Draw board visualization
                            board_vis = visualizer.draw_board(board)
                            board_vis = visualizer.draw_coordinates(board_vis)
                            
                            # Create side-by-side visualization
                            vis_img = visualizer.create_side_by_side(
                                contour_img,
                                board_vis,
                                labels=("Detected Board", "Extracted Position")
                            )
                            
                            # Add FEN overlay
                            fen = board.fen().split(" ")[0]  # Just the piece placement part
                            vis_img = visualizer.add_text_overlay(vis_img, fen)
                            
                            # Show visualization
                            cv2.imshow("Chess Video Analyzer", vis_img)
                            
                            # Wait for key press (1ms)
                            key = cv2.waitKey(1)
                            if key == 27:  # ESC key
                                break
                    else:
                        print(f"Invalid position detected in frame {frame_count}:")
                        for issue in issues:
                            print(f"  - {issue}")
            
            processed_frames += 1
            
        frame_count += 1
        
    # Close video
    video_input.close()
    
    # Close visualization window
    if args.visualize:
        cv2.destroyAllWindows()
        
    # Generate output
    if detected_positions:
        print(f"\nProcessed {processed_frames} frames")
        print(f"Detected {len(detected_positions)} positions")
        print(f"Tracked {len(move_tracker.get_moves())} moves")
        
        # Generate PGN
        if args.pgn:
            pgn_path = output_dir / "game.pgn"
            pgn = notation_generator.get_pgn()
            
            with open(pgn_path, "w") as f:
                f.write(pgn)
                
            print(f"PGN output saved to {pgn_path}")
            
        # Generate FEN
        if args.fen:
            fen_path = output_dir / "position.fen"
            fen = notation_generator.get_fen()
            
            with open(fen_path, "w") as f:
                f.write(fen)
                
            print(f"FEN output saved to {fen_path}")
            
        # Print moves
        moves = notation_generator.get_formatted_move_list()
        print("\nDetected moves:")
        print(moves)
        
        return True
    else:
        print("No valid chess positions detected")
        return False


def main():
    """Main entry point."""
    args = parse_args()
    
    try:
        success = process_video(args)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
