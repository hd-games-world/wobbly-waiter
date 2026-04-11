# Wobbly Waiter

A mobile-first physics game where you balance a glass on a tray by tilting your phone. Built with Python (PyScript) and HTML5 Canvas.

## How to Play

1. **Mobile**: Hold your phone in a comfortable playing position, tap "Start Game", and wait for calibration. Then tilt left/right to balance the glass.
2. **Desktop**: Move your mouse left/right from the center of the screen to simulate tilting. The further from center, the more tilt.

## Goal

Keep the glass balanced on the tray for as long as possible without:
- Letting it fall off the tray
- Tilting more than 80 degrees

Score increases when the glass stays near the center of the tray.

## Running the Game

### Option 1: Local Server (Recommended)
```bash
cd test.03
python -m http.server 8080
```
Then open `http://localhost:8080` in your browser.

### Option 2: Any Web Server
Serve the directory with any web server and open the index.html file.

## Technical Details

- **Runtime**: PyScript (Pyodide) - runs Python in the browser
- **Language**: Python 3.11+
- **Graphics**: HTML5 Canvas API
- **Inputs**: 
  - Mobile: DeviceOrientation API (gyroscope)
  - Desktop: Mouse position relative to screen center
- **Physics**: Custom lightweight physics (no external physics library due to Pyodide limitations)

## File Structure

```
test.03/
├── index.html      # Main game file
├── instructions.md # Original task specification
└── README.md       # This file
```

## Features

- Calibration system captures your initial phone position
- Responsive canvas (100% viewport)
- Score only counts after you start playing (tilt > 3°)
- 2-second grace period before scoring begins
- Game over detection (fall off tray or extreme tilt)
- Restart functionality
- Works on both mobile and desktop

## Browser Compatibility

- **Mobile**: Chrome, Firefox, Safari (iOS/Android)
- **Desktop**: Chrome, Firefox, Edge, Safari

Note: On iOS, you may need to grant motion sensor permissions when prompted.
