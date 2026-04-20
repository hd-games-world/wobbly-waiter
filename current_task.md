**Directive for Orchestrator (Trae):** Activate the **UI & Sensor Specialist** agent to build the foundation of version v0.3.0.

**Tasks:**

1. **Structural Separation:** Refactor the current project into three clean files: `index.html` (Shell), `style.css` (Visuals), and `main.py` (Logic).
    
2. **Responsive Canvas:** Implement a JavaScript observer that updates CSS variables `--vw` and `--vh` to match the real-time window size. The `#game-canvas` must always fill 100% of the screen.
    
3. **The Data Bridge:** Initialize a global `window.gameState` object containing: `tilt`, `score`, `isGameOver`, and `difficulty`.
    
4. **Sensor Integration:** Use the **Generic Sensor API** to capture phone tilt and map it to `window.gameState.tilt`.
    

**Reference:** Follow the `.traerules` file for scaling and VRAM constraints. No physics logic yet, just the environment.
