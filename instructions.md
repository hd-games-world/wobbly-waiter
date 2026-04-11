# Agent Task: Mobile-First Slapstick Physics Game (Python/PyScript)

## Project Overview
Build a "Wobbly Waiter" game where the player tilts their phone to balance a glass on a tray. 
Goal: Simple task + Difficult controls = Mechanical Comedy.

## Technical Stack
- Language: Python 3.11+
- Runtime: PyScript (Pyodide)
- Physics: Pymunk
- Graphics: HTML5 Canvas API (Drawing Sprites over Physics bodies)
- Inputs: DeviceOrientation API (Tilt) + Mouse/Touch for fallback.

## Core Logic Requirements
1. **Tilt Handling**: 
    - Implement a JavaScript-to-Python bridge to capture `deviceorientation` events.
    - Important: Add a "Request Sensor Access" button for iOS/Android compatibility.
2. **Physics Engine (Pymunk)**:
    - Gravity: Strong enough to make the glass slide.
    - Tray: A kinematic/dynamic body that tilts based on the phone's 'beta' or 'gamma' angle.
    - Glass: A dynamic body with high friction on the bottom but low stability.
3. **Visuals (Sprite Support)**:
    - The code must be ready to load 3 images: `waiter.png`, `tray.png`, `glass.png`.
    - Create a placeholder function to draw these images centered on their physical coordinates.
4. **Mobile First UI**:
    - Canvas should occupy 100% of the viewport.
    - Game over state: If glass Y coordinate > Screen Height or Tilt angle > 45 degrees.

## File Structure (Single File Preferred)
- `index.html`: Contains HTML shell, CSS for the "Start" button, and the `<py-script>` block.
- `assets/`: (Directory for images you will provide later).

## Specific Instruction for the Agent
"Please write a robust index.html using PyScript. Use `micropip` to install `pymunk`. Ensure the physics loop runs at 60fps and maps the phone's tilt to the tray's rotation angle. Provide a clean fallback for desktop testing using mouse X position to simulate tilt."
