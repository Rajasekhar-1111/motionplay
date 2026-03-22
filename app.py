"""
Flask Web Application for Hand Gesture Game
Web-based Subway Surfers with real-time hand gesture recognition
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
from io import BytesIO
import threading
import time
import json

# Import hand gesture modules
from modules.video_capture_preprocessing import VideoCapturePreprocessor
from modules.hand_detection_segmentation import HandDetectionSegmentor
from modules.feature_extraction import FeatureExtractor
from modules.gesture_classification import GestureClassifier

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Configure SocketIO for production deployment
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet',
    ping_timeout=60,
    ping_interval=25,
    engineio_logger=False,
    socketio_logger=False,
    transport=['websocket', 'polling']  # Support both websocket and polling fallback
)

# Global state
gesture_state = {
    'current_gesture': 'NEUTRAL',
    'last_command': None,
    'last_command_time': 0,
    'command_cooldown': 0.3
}

# Initialize gesture recognition modules
try:
    detector = HandDetectionSegmentor()
    extractor = FeatureExtractor()
    classifier = GestureClassifier(smoothing_enabled=True)
except Exception as e:
    print(f"Warning: Could not initialize gesture modules: {e}")
    detector = None


def process_frame(frame_data):
    """
    Process base64 frame from browser and detect gesture
    Returns gesture name and frame with annotations
    """
    try:
        # Decode base64 image
        if ',' in frame_data:
            frame_data = frame_data.split(',')[1]
        
        frame_bytes = base64.b64decode(frame_data)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        
        if frame is None:
            return None, "NEUTRAL"
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detect hand
        if detector:
            mask, contour, properties = detector.detect_hand(hsv, frame)
            
            if contour is not None and len(contour) > 20:
                # Extract features
                features = extractor.extract_features(mask, contour, properties)
                
                # Classify gesture
                if features and 'finger_count' in features:
                    gesture = classifier.classify_gesture(features)
                    
                    # Map internal gesture names to game commands
                    gesture_mapping = {
                        'INDEX_RIGHT': 'RIGHT_POINT',
                        'INDEX_LEFT': 'LEFT_POINT',
                        'OPEN_PALM': 'OPEN_PALM',
                        'CLOSED_FIST': 'CLOSED_FIST'
                    }
                    
                    # Get mapped gesture name, or use original if not in mapping
                    game_gesture = gesture_mapping.get(str(gesture), str(gesture))
                    
                    # Draw annotations
                    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                    cv2.putText(frame, f"Gesture: {game_gesture}", (10, 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Fingers: {features['finger_count']}", (10, 70),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    return frame, game_gesture
        
        return frame, "NEUTRAL"
    
    except Exception as e:
        print(f"Error processing frame: {e}")
        return None, "NEUTRAL"


def encode_frame(frame):
    """Encode OpenCV frame to base64 for transmission"""
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/jpeg;base64,{frame_base64}"
    except:
        return None


@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


@socketio.on('connect')
def handle_connect():
    """WebSocket connection established"""
    print(f"Client connected: {request.sid}")
    emit('connection_response', {'data': 'Connected to gesture recognition server'})


@socketio.on('disconnect')
def handle_disconnect():
    """WebSocket disconnected"""
    print(f"Client disconnected: {request.sid}")


@socketio.on('frame')
def handle_frame(data):
    """
    Receive video frame from browser, process for gestures
    Send back annotated frame and detected gesture
    """
    try:
        if 'image' in data:
            frame, gesture = process_frame(data['image'])
            
            # Update gesture state
            current_time = time.time()
            gesture_state['current_gesture'] = gesture
            
            # Emit back processed frame and gesture
            response = {
                'gesture': gesture,
                'timestamp': current_time
            }
            
            if frame is not None:
                response['frame'] = encode_frame(frame)
            
            emit('processed_frame', response)
    
    except Exception as e:
        print(f"Error handling frame: {e}")
        emit('error', {'message': str(e)})


@socketio.on('game_command')
def handle_game_command():
    """Get the latest gesture to command mapping"""
    gesture = gesture_state['current_gesture']
    
    # Map gesture to game command
    command_map = {
        'RIGHT_POINT': 'RIGHT',
        'LEFT_POINT': 'LEFT',
        'OPEN_PALM': 'UP',
        'CLOSED_FIST': 'DOWN'
    }
    
    command = command_map.get(gesture, None)
    emit('command', {'gesture': gesture, 'command': command})


if __name__ == '__main__':
    # For local development
    # Note: Gunicorn will run this automatically on production (render.yaml)
    socketio.run(
        app, 
        debug=True, 
        host='0.0.0.0', 
        port=5000,
        allow_unsafe_werkzeug=True
    )
