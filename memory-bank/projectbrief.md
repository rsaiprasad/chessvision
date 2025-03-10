# Chess Video Analysis Application - Project Brief

## Project Overview
This application analyzes chess games from video recordings, identifies the chess board, extracts positions, and tracks moves in real-time. It outputs the game in standard chess notation (PGN/FEN) as moves are made.

## Core Requirements
1. Process chess game videos (recorded files or streams)
2. Identify and extract the chess board from video frames
3. Recognize chess pieces and their positions
4. Track moves as they occur in the video
5. Output standard chess notation (PGN/FEN) for the game
6. Consider legal chess moves to improve move detection accuracy

## Project Structure
The project is organized into three main components:

1. **chess-vision-lib**: Core library for chess video analysis
   - Video processing and frame extraction
   - Board detection and normalization
   - Position extraction and validation
   - Move tracking and chess logic
   - PGN/FEN generation

2. **chess-vision-service**: Backend REST API service
   - Exposes library functionality through web API
   - Handles video stream processing
   - Provides endpoints for position/move data
   - Manages authentication and authorization
   - Formats responses for frontend consumption

3. **chess-vision-web**: Frontend web application
   - React/TypeScript with ShadCN UI
   - Dual-panel interface (video + chess board)
   - Integration with Lichess analysis board
   - Connection to backend service via API
   - User controls and settings

## Development Phases

### Phase 1: Core Library Development (chess-vision-lib)
- Create core video processing functionality
- Implement chess position extraction algorithms
- Develop move detection and tracking
- Build command-line utility for video input
- Display identified chess positions visually
- Output PGN/FEN as moves are detected

### Phase 2: Backend Service Implementation (chess-vision-service)
- Create REST API service using FastAPI
- Accept video stream inputs
- Process video streams in real-time
- Provide API endpoints for position/move data
- Output FEN/PGN based on specified arguments

### Phase 3: Frontend Development (chess-vision-web)
- Build React/TypeScript frontend with ShadCN UI
- Create dual-panel interface (video + chess board)
- Integrate with Lichess analysis board for position display
- Connect to backend web service via API
- Display real-time position updates

## Technical Architecture
- Core Library: Python (chess-vision-lib)
- Backend Service: Python with FastAPI (chess-vision-service)
- Frontend: React/TypeScript with ShadCN UI (chess-vision-web)
- Frontend Build Tool: RSPack
- Integration: Web API connecting frontend and backend

## Success Criteria
- Accurate chess board detection in videos
- Reliable piece position extraction
- Correct move tracking and PGN generation
- Real-time processing capability
- Seamless integration between frontend and backend
