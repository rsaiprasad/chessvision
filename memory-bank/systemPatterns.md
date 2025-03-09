# Chess Video Analysis Application - System Patterns

## System Architecture

```mermaid
flowchart TD
    subgraph Backend [Python Backend]
        VideoInput[Video Input Handler] --> FrameExtractor[Frame Extractor]
        FrameExtractor --> BoardDetector[Chess Board Detector]
        BoardDetector --> PositionExtractor[Position Extractor]
        PositionExtractor --> MoveTracker[Move Tracker]
        MoveTracker --> NotationGenerator[PGN/FEN Generator]
        
        ChessLogic[Chess Logic Engine] -.-> MoveTracker
        ChessLogic -.-> PositionExtractor
    end
    
    subgraph WebService [Python Web Service]
        API[REST API] --> VideoProcessor[Video Processor]
        VideoProcessor --> Backend
        Backend --> ResponseFormatter[Response Formatter]
        ResponseFormatter --> API
    end
    
    subgraph Frontend [React Frontend]
        VideoDisplay[Video Display] --> WebService
        WebService --> BoardDisplay[Chess Board Display]
        UserControls[User Controls] --> WebService
    end
    
    VideoFile[Video File] --> Backend
    VideoStream[Video Stream] --> WebService
    User[User] --> Frontend
```

## Component Relationships

### Backend Components

1. **Video Input Handler**
   - Accepts video files or streams
   - Validates input format and quality
   - Prepares video for processing

2. **Frame Extractor**
   - Extracts individual frames from video
   - Handles different frame rates
   - Optimizes frame selection for processing

3. **Chess Board Detector**
   - Identifies chess board in frame
   - Handles different board angles and lighting
   - Normalizes board perspective

4. **Position Extractor**
   - Identifies chess pieces on the board
   - Maps pieces to board coordinates
   - Generates position representation (FEN)

5. **Move Tracker**
   - Compares consecutive positions
   - Identifies moves made
   - Validates moves against chess rules

6. **PGN/FEN Generator**
   - Converts detected moves to standard notation
   - Maintains game history
   - Formats output according to specifications

7. **Chess Logic Engine**
   - Provides rules of chess
   - Validates legal moves
   - Improves move detection accuracy

### Web Service Components

1. **REST API**
   - Handles HTTP requests and responses
   - Manages authentication and authorization
   - Provides endpoints for video processing

2. **Video Processor**
   - Handles streaming video input
   - Manages processing state
   - Coordinates with backend components

3. **Response Formatter**
   - Structures API responses
   - Formats chess data for frontend consumption
   - Handles error responses

### Frontend Components

1. **Video Display**
   - Shows original video feed
   - Provides playback controls
   - Highlights detected board and moves

2. **Chess Board Display**
   - Renders current position using Lichess board
   - Updates in real-time with detected moves
   - Provides interactive analysis features

3. **User Controls**
   - Video upload/stream selection
   - Processing options and settings
   - Analysis tools and preferences

## Data Flow Patterns

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Backend
    participant ChessLogic
    
    User->>Frontend: Upload video/Start stream
    Frontend->>API: Send video data
    API->>Backend: Process video
    
    loop For each frame
        Backend->>Backend: Extract frame
        Backend->>Backend: Detect board
        Backend->>Backend: Extract position
        Backend->>ChessLogic: Validate position
        ChessLogic-->>Backend: Position validation
        
        alt Position changed
            Backend->>ChessLogic: Determine move
            ChessLogic-->>Backend: Legal move options
            Backend->>Backend: Generate PGN/FEN
            Backend-->>API: Position update
            API-->>Frontend: Position data
            Frontend-->>User: Update display
        end
    end
```

## Key Technical Decisions

1. **Separate Frontend and Backend Packages**
   - Enables independent development and deployment
   - Allows for different technology stacks
   - Facilitates clear API boundaries

2. **Python for Backend Processing**
   - Strong libraries for computer vision (OpenCV)
   - Excellent machine learning support
   - Rich ecosystem for chess programming

3. **React/TypeScript for Frontend**
   - Type safety for complex chess data structures
   - Component-based UI for chess visualization
   - Strong ecosystem for interactive applications

4. **REST API for Communication**
   - Stateless communication between frontend and backend
   - Standard HTTP methods for resource operations
   - JSON for data exchange

5. **Lichess Board Integration**
   - Leverage existing, well-tested chess visualization
   - Access to analysis tools
   - Familiar interface for chess players

6. **Chess Logic for Move Validation**
   - Improve accuracy by considering legal moves
   - Reduce false positives in piece detection
   - Handle edge cases in chess rules

## Design Patterns

1. **Pipeline Pattern**
   - Sequential processing of video frames
   - Clear separation of concerns between stages
   - Easy to extend or modify individual components

2. **Observer Pattern**
   - Position changes notify subscribers
   - Frontend components react to backend updates
   - Decoupled communication between components

3. **Strategy Pattern**
   - Pluggable algorithms for board detection
   - Configurable piece recognition strategies
   - Adaptable to different board styles and pieces

4. **Factory Pattern**
   - Create appropriate processors based on video type
   - Generate correct notation based on game context
   - Instantiate proper analysis tools based on user preferences

5. **Repository Pattern**
   - Abstract data storage and retrieval
   - Separate business logic from data access
   - Enable different storage backends (file, database)
