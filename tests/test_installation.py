"""
Test script to verify that the installation works correctly.
"""

import sys
import importlib


def test_import_modules():
    """Test importing all required modules."""
    modules = [
        "cv2",  # OpenCV
        "numpy",
        "chess",
        "chess_video_analyzer",
        "chess_video_analyzer.video.input",
        "chess_video_analyzer.video.frame",
        "chess_video_analyzer.board.detector",
        "chess_video_analyzer.board.normalizer",
        "chess_video_analyzer.position.extractor",
        "chess_video_analyzer.position.validator",
        "chess_video_analyzer.moves.tracker",
        "chess_video_analyzer.notation.generator",
        "chess_video_analyzer.utils.visualization",
        "chess_video_analyzer.cli.main"
    ]
    
    failed_imports = []
    
    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"✓ Successfully imported {module_name}")
        except ImportError as e:
            print(f"✗ Failed to import {module_name}: {e}")
            failed_imports.append(module_name)
            
    if failed_imports:
        print("\nThe following modules could not be imported:")
        for module in failed_imports:
            print(f"  - {module}")
        print("\nPlease check your installation and dependencies.")
        return False
    else:
        print("\nAll modules imported successfully!")
        return True


def test_opencv_version():
    """Test OpenCV version."""
    import cv2
    version = cv2.__version__
    print(f"OpenCV version: {version}")
    
    # Parse version string
    major, minor, patch = map(int, version.split('.')[:3])
    
    if major < 4:
        print("Warning: OpenCV version 4.x or higher is recommended.")
        return False
    else:
        print("OpenCV version is compatible.")
        return True


def test_python_chess_version():
    """Test python-chess version."""
    import chess
    version = chess.__version__
    print(f"python-chess version: {version}")
    
    # Parse version string
    major, minor, patch = map(int, version.split('.')[:3])
    
    if major < 1:
        print("Warning: python-chess version 1.x or higher is recommended.")
        return False
    else:
        print("python-chess version is compatible.")
        return True


def test_numpy_version():
    """Test NumPy version."""
    import numpy
    version = numpy.__version__
    print(f"NumPy version: {version}")
    
    # Parse version string
    major, minor, patch = map(int, version.split('.')[:3])
    
    if major < 1 or (major == 1 and minor < 20):
        print("Warning: NumPy version 1.20.0 or higher is recommended.")
        return False
    else:
        print("NumPy version is compatible.")
        return True


def main():
    """Run all tests."""
    print("Testing Chess Video Analyzer installation...\n")
    
    # Test importing modules
    print("Testing module imports:")
    modules_ok = test_import_modules()
    
    print("\nTesting dependency versions:")
    opencv_ok = test_opencv_version()
    chess_ok = test_python_chess_version()
    numpy_ok = test_numpy_version()
    
    # Print summary
    print("\nInstallation Test Summary:")
    print(f"Module imports: {'✓' if modules_ok else '✗'}")
    print(f"OpenCV version: {'✓' if opencv_ok else '✗'}")
    print(f"python-chess version: {'✓' if chess_ok else '✗'}")
    print(f"NumPy version: {'✓' if numpy_ok else '✗'}")
    
    if modules_ok and opencv_ok and chess_ok and numpy_ok:
        print("\nAll tests passed! The installation appears to be working correctly.")
        return 0
    else:
        print("\nSome tests failed. Please check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
