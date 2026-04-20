
> **Role:** Senior Frontend Engineer.
> **Context:** The current game v0.2.0-alpha has major layout and UI interaction issues.
> 
> **Specific Instructions:**
> 1. **Responsive Background:** Update `draw_background` to calculate a scale factor that covers the entire canvas (Object-fit: Cover logic). Center the image horizontally and vertically.
> 2. **Coordinate Refactor:** Replace all hard-coded pixel values for `waiter_y`, `tray_y`, and `glass_y` with relative values based on `self.canvas.height` (e.g., Waiter should be at `height * 0.85`).
> 3. **UI Fix:** Ensure the `#game-over` div has a `z-index: 999` and that all parent containers do not have `pointer-events: none` when the game ends. Verify the Restart button listener.
> 4. **Asset Fail-safe:** In `AssetManager`, if `onerror` triggers, set a flag `use_placeholders = True` so the game can proceed with colored rectangles instead of getting stuck on the loading bar.
> 5. **Physics Update:** Add a damping factor to the $glass\_angle$ to prevent jittery movement when the device is near 0 degrees.
> 
> **Deliverable:** Modified PyScript and CSS blocks that integrate seamlessly with the existing structure.

