Optimizing tool selection...

Read [](file:///home/hassan/001.Development/10.games/001/wobbly-waiter/index.html#1-1), lines 1 to 500

# Complete Code Tutorial for Beginners: Wobbly Waiter Game

This is a full walkthrough of every JavaScript and Python line in your game. I'll explain it section by section.

---

## Part 1: HTML Setup & Libraries

```html
<!DOCTYPE html>
<html lang="en">
```
This tells the browser "this is an HTML5 document" and the language is English.

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
```
- **charset**: Tells the browser to use UTF-8 text encoding (supports all languages)
- **viewport**: Makes the game responsive on mobile phones and prevents users from zooming (which would break the game)

```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
```
This downloads **Pyodide**, which is a Python runtime that runs *inside the browser*. Normally Python runs on a server, but Pyodide lets us run Python directly in the browser.

```html
<link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css">
<script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>
```
These load **PyScript**, which makes it easy to write Python code in an HTML file.

---

## Part 2: CSS Styling (Brief Overview)

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
```
Resets all HTML elements to have no default spacing.

```css
html, body { width: 100%; height: 100%; overflow: hidden; background: #1a1a2e; }
```
Makes the page fill the entire screen with a dark background color (#1a1a2e = dark blue).

```css
#game-canvas { display: block; width: 100%; height: 100%; touch-action: none; }
```
The canvas (where the game draws) fills the screen and ignores default touch gestures.

The rest of the CSS styles various screens (start screen, game over, calibration).

---

## Part 3: Game State (JavaScript)

```javascript
window.pyodideReady = false;
```
A flag variable that tracks whether Python has loaded. Initially `false`, later set to `true` when ready.

```javascript
window.gameState = {
    tiltAngle: 0,              // Current phone tilt (degrees)
    isMobile: false,           // Is this a mobile phone?
    gameStarted: false,        // Has the player clicked "Start"?
    score: 0,                  // Player's current score
    initialBeta: null,         // Phone's tilt angle at calibration start
    initialGamma: null,        // Phone's side tilt at calibration start
    calibrating: true          // Are we in calibration mode?
};
```

This is a **state object** - a single place storing all game information. Think of it as the "brain" of the game.

---

## Part 4: Loading Python (JavaScript)

```javascript
async function initPyodide() {
    window.pyodide = await loadPyodide();
```

- **async**: This function waits for something to finish before continuing
- **await**: "Wait for Python to load before moving on"
- **loadPyodide()**: Loads the Python runtime from the CDN

```javascript
    window.pyodideReady = true;
```
Once Python loads, set the flag to `true`.

```javascript
    document.getElementById('start-btn').disabled = false;
    document.getElementById('start-btn').textContent = "Start Game";
}
initPyodide();
```
Enable the "Start Game" button and change its text. Call the function immediately.

---

## Part 5: Device Orientation (Phone Tilt Sensor)

```javascript
function requestSensorAccess() {
    if (typeof DeviceOrientationEvent !== 'undefined' && 
        typeof DeviceOrientationEvent.requestPermission === 'function') {
```

This checks if the browser supports device orientation sensors (for phone tilt).

```javascript
        DeviceOrientationEvent.requestPermission()
            .then(response => {
                if (response === 'granted') {
                    window.addEventListener('deviceorientation', handleOrientation);
                }
            })
```

Ask the user's permission to read the phone's orientation sensor. If granted, listen for `deviceorientation` events.

```javascript
    } else {
        window.addEventListener('deviceorientation', handleOrientation);
    }
}
```

On non-Apple devices, just start listening without asking permission.

---

## Part 6: Processing Phone Tilt

```javascript
function handleOrientation(event) {
    let gamma = event.gamma || 0;  // Side-to-side tilt (-90 to 90 degrees)
    let beta = event.beta || 0;    // Forward-backward tilt (-180 to 180 degrees)
```

Every time the phone moves, the browser fires a `deviceorientation` event with:
- **gamma**: Tilting left/right
- **beta**: Tilting forward/backward

```javascript
    if (window.gameState.initialGamma === null) {
        window.gameState.initialGamma = gamma;
        window.gameState.initialBeta = beta;
```

On the first reading, save the phone's starting position. This is the **calibration phase** - we're establishing a baseline.

```javascript
        setTimeout(() => {
            window.gameState.calibrating = false;
        }, 1000);
        return;
    }
```

Wait 1000 milliseconds (1 second), then finish calibration. Return early so we don't process this data yet.

```javascript
    if (window.gameState.calibrating) return;
```

While calibrating, ignore all tilt data.

```javascript
    let relativeGamma = gamma - window.gameState.initialGamma;
    let relativeBeta = beta - window.gameState.initialBeta;
```

Calculate the **difference** between the current tilt and the starting tilt. This gives us the actual tilt amount (not absolute angle).

```javascript
    if (window.innerWidth > window.innerHeight) {
        window.gameState.tiltAngle = relativeGamma;
    } else {
        window.gameState.tiltAngle = relativeBeta;
    }
```

If the phone is in landscape mode, use `gamma` (side tilt). If portrait mode, use `beta` (forward tilt).

---

## Part 7: Button Click Events (JavaScript)

```javascript
document.getElementById('start-btn').addEventListener('click', () => {
    document.getElementById('start-screen').style.display = 'none';
```

When the "Start" button is clicked, hide the start screen.

```javascript
    if (window.gameState.isMobile) {
        document.getElementById('calibration-screen').style.display = 'flex';
        
        setTimeout(() => {
            window.gameState.isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            window.gameState.tiltAngle = 0;
            window.gameState.initialGamma = null;
            window.gameState.initialBeta = null;
            window.gameState.calibrating = true;
            if (window.gameState.isMobile) requestSensorAccess();
```

Show a calibration screen (asking the player to hold the phone steady). Reset tilt values and request sensor permission if it's a mobile device.

```javascript
            setTimeout(() => {
                document.getElementById('calibration-screen').style.display = 'none';
                window.gameState.calibrating = false;
                window.gameState.gameStarted = true;
            }, 1500);
        }, 100);
    } else {
        window.gameState.gameStarted = true;
    }
});
```

After 1500ms (1.5 seconds), hide the calibration screen and start the game. On desktop, skip calibration and start immediately.

```javascript
document.getElementById('restart-btn').addEventListener('click', () => {
    document.getElementById('game-over').style.display = 'none';
    document.getElementById('calibration-screen').style.display = 'flex';
    
    window.gameState.tiltAngle = 0;
    window.gameState.score = 0;
    window.gameState.initialBeta = null;
    window.gameState.initialGamma = null;
    window.gameState.calibrating = true;
    
    setTimeout(() => {
        document.getElementById('calibration-screen').style.display = 'none';
        window.gameState.calibrating = false;
        window.gameState.gameStarted = true;
        
        if (window.pyGameReset) {
            window.pyGameReset();
        }
    }, 1500);
});
```

The restart button does the same thing: reset the game, calibrate again, and call the Python function `pyGameReset()` to reset the game state.

---

## Part 8: Desktop Input (Mouse & Touch)

```javascript
document.addEventListener('mousemove', (e) => {
    if (window.gameState.gameStarted) {
        let centerX = window.innerWidth / 2;
        let offset = e.clientX - centerX;
        let normalized = offset / centerX;
        window.gameState.tiltAngle = normalized * 45;
    }
});
```

On desktop with a mouse:
- Get the mouse's X position
- Calculate distance from center of screen
- Normalize to a value between -1 and 1
- Convert to a tilt angle (-45° to +45°)

```javascript
document.addEventListener('touchmove', (e) => {
    if (window.gameState.gameStarted && e.touches.length > 0) {
        e.preventDefault();
        let touch = e.touches[0];
        let centerX = window.innerWidth / 2;
        let offset = touch.clientX - centerX;
        let normalized = offset / centerX;
        window.gameState.tiltAngle = normalized * 45;
    }
}, { passive: false });
```

On mobile touch screens (non-sensor phones):
- Prevent the default touch behavior (scrolling)
- Do the same calculation with the touch position

---

## Part 9: Python Game Logic

```python
import asyncio
import js
import math
import random
from pyodide.ffi import create_proxy
```

**Imports**:
- **asyncio**: For handling asynchronous operations
- **js**: Bridge to access JavaScript from Python
- **math**: Mathematical functions
- **random**: Generate random numbers
- **create_proxy**: Make Python functions callable from JavaScript

---

## The Game Class (Python)

```python
class Game:
    def __init__(self):
```

A **class** is a template for objects. This Game class holds all the game logic.

```python
        self.canvas = js.document.getElementById("game-canvas")
        self.ctx = self.canvas.getContext("2d")
```

Get the canvas element from HTML and get its **2D context** (the drawing tool).

```python
        self.width = js.window.innerWidth
        self.height = js.window.innerHeight
        self.canvas.width = self.width
        self.canvas.height = self.height
```

Set the canvas size to match the window size.

```python
        self.tray_x = self.width / 2
        self.tray_y = self.height * 0.6
        self.tray_angle = 0
```

**Tray** (wooden plate) properties:
- Position: Center horizontally, 60% down the screen
- Angle: 0 (flat)

```python
        self.glass_x = self.tray_x
        self.glass_y = self.tray_y - 60
        self.glass_vx = 0
        self.glass_vy = 0
        self.glass_angle = 0
        self.glass_ang_vel = 0
```

**Glass** properties:
- Position: On top of the tray, 60 pixels up
- **vx** = horizontal velocity (how fast moving left/right)
- **vy** = vertical velocity (not used in this game)
- **ang_vel** = angular velocity (how fast rotating)

```python
        self.score = 0
        self.game_over = False
        self.last_time = 0
        
        self.tray_images = {}
        self.glass_images = {}
        self.waiter_images = {}
```

Initialize score, game-over flag, and empty dictionaries for images.

---

## Reset Function (Python)

```python
    def reset(self):
        self.tray_x = self.width / 2
        self.tray_y = self.height * 0.6
        # ... (resets all values back to start)
        self.score = 0
        self.game_over = False
```

When the player clicks "Restart", this resets all game values.

---

## Update Function (Python) - The Physics Engine

This is the most important function - it updates game physics every frame.

```python
    def update(self, dt):
        if self.game_over:
            return
```

If the game is over, don't update anything.

```python
        tilt = 0
        try:
            tilt = js.window.gameState.tiltAngle
        except:
            return
```

Read the tilt angle from JavaScript's game state. If it fails, stop updating.

```python
        if not self.gameplay_started:
            if abs(tilt) > 3:
                self.gameplay_started = True
                current_time = js.window.performance.now()
                self.score_start_time = current_time
```

**Gameplay doesn't start until the player tilts!** This prevents accidental scoring while waiting.

```python
        tilt = max(-90, min(90, tilt))
```

**Clamp** the tilt value between -90° and +90° (prevent extreme values).

```python
        self.tray_angle = math.radians(tilt)
```

Convert the tilt from degrees to radians (math uses radians).

```python
        gravity = 400
        gx = gravity * math.sin(self.tray_angle)
```

Calculate the **gravitational force** pulling the glass sideways:
- `math.sin()` converts angle to force direction
- Multiply by 400 to make it strong enough

```python
        friction = 0.98
        self.glass_vx += gx * dt
        self.glass_vx *= friction
```

**Friction**: Each frame, multiply velocity by 0.98 (slows it down a bit).  
Then add gravity force and apply friction.

```python
        self.glass_x += self.glass_vx * dt
```

Update the glass's position based on its velocity.

```python
        tray_half_width = 90
        tray_left = self.tray_x - tray_half_width
        tray_right = self.tray_x + tray_half_width
        
        if self.glass_x < tray_left:
            self.glass_x = tray_left
            self.glass_vx *= -0.2
        elif self.glass_x > tray_right:
            self.glass_x = tray_right
            self.glass_vx *= -0.2
```

**Collision detection**: If the glass slides off the tray:
- Stop it at the edge
- Reverse its velocity (bounce) with 0.2 damping (loses energy)

```python
        self.glass_y = self.tray_y - 30
```

Keep the glass on top of the tray (always 30 pixels above it).

```python
        torque = self.glass_vx * 0.005
        self.glass_ang_vel += torque * dt
        self.glass_ang_vel *= 0.98
        self.glass_angle += self.glass_ang_vel
```

**Rotational physics**: 
- The moving glass creates rotational force (**torque**)
- Increase angular velocity by torque
- Apply friction to rotation
- Update the rotation angle

```python
        if abs(self.glass_x - self.tray_x) > tray_half_width - 10:
            self.game_over = True
            self.show_game_over()
        
        if abs(tilt) > 80:
            self.game_over = True
            self.show_game_over()
```

**Game over conditions**:
1. Glass slides off the tray
2. Player tilts the phone too extreme (past 80°)

```python
        if self.gameplay_started:
            current_time = js.window.performance.now()
            time_since_start = current_time - self.score_start_time
            
            if time_since_start > 2000 and abs(self.glass_x - self.width/2) < 20:
                self.score += 1
                try:
                    js.window.gameState.score = self.score
                except:
                    pass
```

**Scoring**: If 2 seconds have passed AND the glass is centered (within 20 pixels), add 1 point!

---

## Draw Function (Python) - Rendering

```python
    def draw(self):
        self.ctx.fillStyle = "#1a1a2e"
        self.ctx.fillRect(0, 0, self.width, self.height)
```

Clear the canvas by drawing a dark blue rectangle over everything.

```python
        self.ctx.save()
        self.ctx.translate(self.tray_x, self.tray_y)
        self.ctx.rotate(self.tray_angle)
        self.draw_tray_sprite(0, 0)
        self.ctx.restore()
```

Draw the tray:
- **save()**: Remember current drawing state
- **translate()**: Move the drawing "pen" to the tray's position
- **rotate()**: Rotate the pen by the tray angle
- **draw_tray_sprite()**: Actually draw the tray
- **restore()**: Return pen to original state

```python
        self.ctx.save()
        self.ctx.translate(self.glass_x, self.glass_y)
        self.ctx.rotate(self.glass_angle)
        self.draw_glass_sprite(0, 0)
        self.ctx.restore()
```

Same for the glass.

```python
        self.draw_waiter_sprite(self.width/2, self.height * 0.85)
        self.draw_ui()
```

Draw the waiter character and UI (score display).

---

## Drawing Shapes (Python)

```python
    def draw_tray_sprite(self, x, y):
        w, h = 220, 25
        self.ctx.fillStyle = "#8b5a2b"
        self.ctx.beginPath()
        self.ctx.ellipse(x, y, w/2, h/2, 0, 0, math.pi * 2)
        self.ctx.fill()
```

Draw an ellipse (oval) for the tray:
- Width 220, height 25
- Brown color (#8b5a2b)
- **ellipse()**: (x, y, radiusX, radiusY, rotation, startAngle, endAngle)

```python
    def draw_glass_sprite(self, x, y):
        w, h = 45, 70
        self.ctx.fillStyle = "rgba(200, 220, 255, 0.3)"
        self.ctx.beginPath()
        self.ctx.moveTo(x - w/2 + 5, y - h/2)
        self.ctx.lineTo(x - w/2, y + h/2)
        self.ctx.lineTo(x + w/2, y + h/2)
        self.ctx.lineTo(x + w/2 - 5, y - h/2)
        self.ctx.closePath()
        self.ctx.fill()
```

Draw a glass (trapezoid shape):
- Semi-transparent blue
- **beginPath()**: Start a new shape
- **moveTo()**: Move pen to starting point
- **lineTo()**: Draw a line to this point
- **closePath()**: Close the shape

---

## UI Text (Python)

```python
    def draw_ui(self):
        self.ctx.fillStyle = "white"
        self.ctx.font = "24px Arial"
        self.ctx.textAlign = "left"
        self.ctx.fillText(f"Score: {self.score}", 20, 40)
```

Draw the score text:
- White color, 24px font
- Display at position (20, 40)
- The `f"..."` notation inserts variables into the string

```python
        tilt = 0
        try:
            gs = js.window.gameState if js.window else None
            if gs:
                tilt = gs.tiltAngle
        except:
            pass
        self.ctx.fillStyle = "#a0a0a0"
        self.ctx.font = "16px Arial"
        self.ctx.fillText(f"Tilt: {tilt:.1f}°", 20, 70)
```

Display the current tilt angle (for debugging). The `.1f` means "show 1 decimal place".

---

## Game Over (Python)

```python
    def show_game_over(self):
        try:
            js.document.getElementById("game-over").style.display = "flex"
            js.document.getElementById("score").textContent = f"Score: {self.score}"
        except:
            pass
```

Show the game-over screen from JavaScript and update the score display.

---

## Game Loop (Python)

```python
game = Game()
game.initialized = False

def game_loop(timestamp):
    try:
        if not hasattr(game, 'last_time'):
            game.last_time = timestamp
        
        dt = (timestamp - game.last_time) / 1000
        game.last_time = timestamp
        dt = min(dt, 0.05)
```

**Delta Time (dt)**: How many seconds have passed since the last frame.
- Calculate the difference between current time and last time
- Divide by 1000 to convert milliseconds to seconds
- Cap it at 0.05 (prevents bugs if the frame is extremely slow)

```python
        if not game.initialized:
            try:
                if js.window.gameState.gameStarted:
                    game.initialized = True
            except:
                pass
```

Wait until the player clicks "Start" before initializing.

```python
        if game.initialized:
            try:
                game.update(dt)
            except:
                pass
        
        try:
            game.draw()
        except:
            pass
```

Update the game physics, then draw the new frame. Both are wrapped in try/except (error handling).

---

## Summary

**JavaScript** handles:
- Loading Pyodide
- Reading phone sensors
- Button clicks  
- Converting touch/mouse input to tilt angles

**Python** handles:
- Physics calculations (gravity, friction, rotation)
- Collision detection
- Drawing graphics
- Game state (score, game over)
- The main game loop

They communicate through `window.gameState` - a shared object that both languages read and write to.
