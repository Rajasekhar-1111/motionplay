# Subway Surfers - Hand Gesture Control Game

A web-based Subway Surfers game where players control the character using real-time hand gestures detected through their webcam.

## Features

✨ **Real-time Hand Gesture Recognition**
- Left Point → Move Left
- Right Point → Move Right  
- Open Palm → Jump
- Closed Fist → Slide

🎮 **Interactive Game**
- Browser-based Subway Surfers clone
- Real-time gameplay with hand gesture controls
- Score tracking and difficulty progression

📱 **Cross-Platform**
- Works on desktop and mobile browsers
- Webcam/camera access required
- No installation needed - just open the URL!

## Local Development

### Prerequisites
- Python 3.10+
- Webcam/Camera access

### Setup

1. **Clone or extract the project:**
   ```bash
   cd motionplay/src
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   Navigate to `http://localhost:5000`

## Deployment to Render

### Step 1: Prepare for Deployment

All deployment files are ready:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Render process definition
- ✅ `render.yaml` - Render configuration
- ✅ `runtime.txt` - Python version specification

### Step 2: Deploy to Render

1. **Create a GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Subway Surfers hand gesture game"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/motionplay.git
   git push -u origin main
   ```

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select the repository branch (main)

3. **Configure Render:**
   - **Name:** `subway-surfers-gesture`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --worker-class eventlet -w 1 app:app`
   - **Plan:** Start with Free tier (can upgrade later)

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - You'll receive a unique URL like: `https://subway-surfers-gesture.onrender.com`

### Step 3: Access Your Game

Once deployed, share the Render URL with users:
```
https://your-app-name.onrender.com
```

Users can:
1. Click the link
2. Grant webcam permission in their browser
3. Click "START GAME" to begin
4. Use hand gestures to play!

## Game Controls

| Gesture | Action | Command |
|---------|--------|---------|
| 👉 Point Right | Move Right | Arrow Right |
| 👈 Point Left | Move Left | Arrow Left |
| ✋ Open Palm | Jump | Arrow Up |
| ✊ Closed Fist | Slide | Arrow Down |

### Keyboard Fallback
- **Arrow Keys** - Control player (if hand detection fails)
- **Arrow Right** - Move right
- **Arrow Left** - Move left
- **Arrow Up** - Jump
- **Arrow Down** - Slide

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Browser (Client-Side)                   │
├─────────────────────────────────────────────────┤
│  • Webcam Access (getUserMedia)                 │
│  • Canvas-based Game                            │
│  • Real-time Video Processing                   │
│  • WebSocket Communication (Socket.IO)          │
└──────────────┬──────────────────────────────────┘
               │ WebSocket (Socket.IO)
               │ Frame Data ↔ Gesture Results
┌──────────────▼──────────────────────────────────┐
│       Flask Web Server (app.py)                  │
├─────────────────────────────────────────────────┤
│  • WebSocket Handler                            │
│  • Frame Processing                             │
│  • Hand Detection & Gesture Recognition         │
│  • Command Mapping                              │
└─────────────────────────────────────────────────┘
               │
               ▼ OpenCV + MediaPipe
        ┌──────────────────────┐
        │ Hand Detection Lab   │
        │ (modules/)           │
        └──────────────────────┘
```

## Technical Stack

**Frontend:**
- HTML5 Canvas - Game rendering
- JavaScript - Game logic
- Socket.IO Client - Real-time communication
- getUserMedia API - Webcam access

**Backend:**
- Flask - Web framework
- Flask-SocketIO - WebSocket support
- OpenCV - Image processing
- MediaPipe - Hand detection
- NumPy - Numerical computations

**Deployment:**
- Render - Cloud hosting
- Gunicorn - WSGI server
- Eventlet - Async worker

## Troubleshooting

### Webcam Not Detected
- Ensure browser has permission to access camera
- Check if another application is using the camera
- Try using HTTPS (some browsers require it)

### Hand Gestures Not Recognized
- Ensure good lighting conditions
- Keep hands fully visible in camera
- Maintain consistent hand positioning
- Try the HSV range adjustment in `hand_detection_segmentation.py`

### Performance Issues
- Check internet connection (WebSocket requires stable connection)
- Reduce video resolution if needed
- Close other browser tabs/applications
- Try different browser (Chrome recommended)

### Deployment Issues

**Build fails:**
- Check `requirements.txt` has correct package names
- Ensure `Procfile` points to correct app file
- Verify Python version in `runtime.txt`

**App crashes after deploy:**
- Check Render logs: Dashboard → Your App → Logs
- Verify all imports work correctly
- Test locally first before deploying

**WebSocket connection fails:**
- Ensure Render URL is accessible
- Check CORS settings in Flask app
- Verify Socket.IO version compatibility

## Performance Optimization

**For better performance:**

1. **Reduce frame size:**
   Change in `app.py` during capture
   ```python
   cap = cv2.VideoCapture(0)
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```

2. **Adjust frame rate:**
   Process every Nth frame instead of every frame
   ```python
   frame_count = 0
   if frame_count % 2 == 0:  # Process every 2nd frame
       # Process frame
   ```

3. **Optimize hand detection:**
   Reduce image resolution before processing in `hand_detection_segmentation.py`

## Future Enhancements

- 🔊 Add sound effects and background music
- 🏆 Leaderboard with high scores
- 🎨 Multiple game themes/skins
- 🌐 Multiplayer mode
- 📊 Gesture accuracy analytics
- 🎯 Difficulty levels
- ⚙️ Adjustable gesture sensitivity

## File Structure

```
motionplay/src/
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── Procfile                        # Render process definition
├── render.yaml                     # Render configuration
├── runtime.txt                     # Python version
├── .gitignore                      # Git ignore file
├── templates/
│   └── index.html                  # Game UI
├── modules/
│   ├── __init__.py
│   ├── video_capture_preprocessing.py
│   ├── hand_detection_segmentation.py
│   ├── feature_extraction.py
│   ├── gesture_classification.py
│   └── game_control_interface.py
├── main.py                         # Original desktop app
├── main_optimized.py
├── main_mediapipe.py
└── quick_hand_check.py
```

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Render logs for error messages
3. Test locally to isolate the issue
4. Check browser console for JavaScript errors

---

**Enjoy playing Subway Surfers with your hands! 🎮**

Made with ❤️ using Flask, OpenCV, and MediaPipe
