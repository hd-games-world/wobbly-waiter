import asyncio
import js
import math
import random
from pyodide.ffi import create_proxy

VERSION = "v0.3.0"
DEBUG_MODE = False
FIXED_DT_CAP = 0.05

class AssetManager:
    def __init__(self):
        self.images = {
            'waiter': None,
            'tray': None,
            'glass': None,
            'background': None
        }
        self.loaded = False
        self.load_count = 0
        self.total_assets = 4
        self.load_images()

    def load_images(self):
        try:
            assets = [
                ('background', 'assets/background.jpg'),
                ('waiter', 'assets/waiter.png'),
                ('tray', 'assets/tray.png'),
                ('glass', 'assets/glass.png')
            ]
            for name, src in assets:
                img = js.Image.new()
                img.src = src
                img.onload = create_proxy(self._on_image_loaded)
                img.onerror = create_proxy(self._on_image_error)
                self.images[name] = img
        except Exception as e:
            print(f"Error loading images: {e}")

    def _on_image_loaded(self, event):
        self.load_count += 1
        progress = int((self.load_count / self.total_assets) * 40) + 60
        try:
            js.document.getElementById('loading-progress').style.width = f"{progress}%"
        except:
            pass

        if self.load_count >= self.total_assets:
            self.loaded = True
            try:
                js.window.onAssetsLoaded()
            except:
                pass

    def _on_image_error(self, event):
        self.load_count += 1
        if self.load_count >= self.total_assets:
            self.loaded = True
            try:
                js.window.onAssetsLoaded()
            except:
                pass

    def is_ready(self):
        return self.loaded

    def get_image(self, name):
        return self.images.get(name)


class InputManager:
    def __init__(self):
        self.filtered_tilt = 0
        self.alpha = 0.2
        self.dead_zone = 3
        self.last_tilt = 0
        self.lerp_target = 0
        self.lerp_current = 0
        self.shiver_offset = 0

    def update(self, raw_tilt, is_mobile):
        if is_mobile:
            self.filtered_tilt = self.alpha * raw_tilt + (1 - self.alpha) * self.filtered_tilt
            self.shiver_offset = (random.random() - 0.5) * 1.0
            if abs(self.filtered_tilt + self.shiver_offset) < self.dead_zone:
                return 0
            return self.filtered_tilt + self.shiver_offset
        else:
            self.lerp_target = raw_tilt
            self.lerp_current = self.lerp_current + (self.lerp_target - self.lerp_current) * 0.1
            self.shiver_offset = (random.random() - 0.5) * 0.5
            return self.lerp_current + self.shiver_offset

    def reset(self):
        self.filtered_tilt = 0
        self.lerp_current = 0
        self.lerp_target = 0
        self.shiver_offset = 0


class PhysicsEngine:
    def __init__(self, difficulty='medium'):
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 'easy':
            self.gravity = 300
            self.restoring_k = 0.15
            self.damping = 0.92
        elif difficulty == 'hard':
            self.gravity = 600
            self.restoring_k = 0.02
            self.damping = 0.98
        else:
            self.gravity = 400
            self.restoring_k = 0.05
            self.damping = 0.95

    def update(self, dt, tilt_angle, glass_x, glass_vx, tray_half_width):
        tray_angle_rad = math.radians(tilt_angle)
        gx = self.gravity * math.sin(tray_angle_rad)
        glass_vx += gx * dt
        glass_vx *= self.damping
        new_glass_x = glass_x + glass_vx * dt
        return new_glass_x, glass_vx


class Game:
    def __init__(self, asset_manager):
        self.canvas = js.document.getElementById("game-canvas")
        self.ctx = self.canvas.getContext("2d")
        self.resize_canvas()
        self.asset_manager = asset_manager
        self.input_manager = InputManager()
        self.physics_engine = PhysicsEngine()

        self.waiter_x = self.width / 2
        self.waiter_y = self.height * 0.85
        self.waiter_width = 200
        self.waiter_height = 200

        self.tray_x = self.waiter_x
        self.tray_y = self.waiter_y - 60
        self.tray_width = 200
        self.tray_height = 25
        self.tray_angle = 0

        self.glass_x = self.tray_x
        self.glass_y = self.tray_y - 35
        self.glass_width = 50
        self.glass_height = 70
        self.glass_vx = 0
        self.glass_angle = 0
        self.glass_ang_vel = 0

        self.score = 0
        self.game_over = False
        self.last_time = 0
        self.score_start_time = 1
        self.gameplay_started = False
        self.debug_mode = DEBUG_MODE

    def resize_canvas(self):
        self.width = js.window.innerWidth
        self.height = js.window.innerHeight
        # Scaling logic as per .traerules (Relative positioning)
        # For now, just filling the window as per instructions
        self.canvas.width = self.width
        self.canvas.height = self.height

    def set_difficulty(self, difficulty):
        self.physics_engine.set_difficulty(difficulty)

    def reset(self):
        self.tray_x = self.width / 2
        self.tray_y = self.height * 0.85 - 60
        self.tray_angle = 0
        self.glass_x = self.tray_x
        self.glass_y = self.tray_y - 35
        self.glass_vx = 0
        self.glass_angle = 0
        self.score = 0
        self.game_over = False
        self.score_start_time = 0
        self.gameplay_started = False
        self.input_manager.reset()

    def update(self, dt):
        if self.game_over:
            return

        dt = min(dt, FIXED_DT_CAP)
        gs = js.window.gameState
        raw_tilt = gs.tilt
        is_mobile = "Mobi" in js.navigator.userAgent

        tilt = self.input_manager.update(raw_tilt, is_mobile)

        if not self.gameplay_started:
            if abs(tilt) > 3:
                self.gameplay_started = True
                self.score_start_time = js.performance.now()

        if not self.gameplay_started:
            self.tray_angle = math.radians(tilt)
            return

        tray_half_width = self.tray_width / 2
        self.glass_x, self.glass_vx = self.physics_engine.update(
            dt, tilt, self.glass_x, self.glass_vx, tray_half_width
        )

        self.glass_angle = (math.radians(tilt) * 0.5) + (self.glass_vx * 0.15)

        tray_left = self.tray_x - tray_half_width
        tray_right = self.tray_x + tray_half_width

        if self.glass_x < tray_left:
            self.glass_x = tray_left
            self.glass_vx *= -0.2
        elif self.glass_x > tray_right:
            self.glass_x = tray_right
            self.glass_vx *= -0.2

        self.glass_y = self.tray_y - 35
        self.tray_angle = math.radians(tilt)

        if abs(self.glass_x - self.tray_x) > tray_half_width - 15:
            self.game_over = True
            js.window.gameState.isGameOver = True
            self.show_game_over()

        if abs(tilt) > 80:
            self.game_over = True
            js.window.gameState.isGameOver = True
            self.show_game_over()

        if self.gameplay_started:
            current_time = js.performance.now()
            time_since_start = current_time - self.score_start_time if self.score_start_time > 0 else 0
            if time_since_start > 2000 and abs(self.glass_x - self.width/2) < 20:
                self.score += 1
                js.window.gameState.score = self.score

    def draw(self):
        self.draw_background()
        self.ctx.save()
        self.ctx.shadowColor = "white"
        self.ctx.shadowBlur = 8
        self.draw_waiter()
        self.draw_tray()
        self.draw_glass()
        self.ctx.restore()
        if self.debug_mode:
            self.draw_debug()
        self.draw_ui()

    def draw_background(self):
        img = self.asset_manager.get_image('background')
        if img and img.complete:
            self.ctx.drawImage(img, 0, 0, self.width, self.height)
        else:
            self.ctx.fillStyle = "#1a1a2e"
            self.ctx.fillRect(0, 0, self.width, self.height)

    def draw_waiter(self):
        img = self.asset_manager.get_image('waiter')
        if img and img.complete:
            self.ctx.drawImage(img, self.waiter_x - self.waiter_width/2, self.waiter_y - self.waiter_height/2, self.waiter_width, self.waiter_height)

    def draw_tray(self):
        img = self.asset_manager.get_image('tray')
        if img and img.complete:
            self.ctx.save()
            self.ctx.translate(self.tray_x, self.tray_y)
            self.ctx.rotate(self.tray_angle)
            self.ctx.drawImage(img, -self.tray_width/2, -self.tray_height/2, self.tray_width, self.tray_height)
            self.ctx.restore()

    def draw_glass(self):
        img = self.asset_manager.get_image('glass')
        if img and img.complete:
            self.ctx.save()
            self.ctx.translate(self.glass_x, self.glass_y + self.glass_height/2)
            self.ctx.rotate(self.glass_angle)
            self.ctx.drawImage(img, -self.glass_width/2, -self.glass_height, self.glass_width, self.glass_height)
            self.ctx.restore()

    def draw_debug(self):
        self.ctx.strokeStyle = "red"
        self.ctx.lineWidth = 2
        tray_half = self.tray_width / 2
        self.ctx.save()
        self.ctx.translate(self.tray_x, self.tray_y)
        self.ctx.rotate(self.tray_angle)
        self.ctx.strokeRect(-tray_half, -self.tray_height/2, self.tray_width, self.tray_height)
        self.ctx.restore()

    def draw_ui(self):
        self.ctx.font = "bold 48px Arial"
        self.ctx.textAlign = "left"
        self.ctx.strokeStyle = "black"
        self.ctx.lineWidth = 4
        self.ctx.strokeText(f"Score: {self.score}", 30, 60)
        self.ctx.fillStyle = "white"
        self.ctx.fillText(f"Score: {self.score}", 30, 60)

        self.ctx.font = "bold 32px Arial"
        self.ctx.strokeText(f"Tilt: {js.window.gameState.tilt:.1f}°", 30, 100)
        self.ctx.fillStyle = "#a0a0a0"
        self.ctx.fillText(f"Tilt: {js.window.gameState.tilt:.1f}°", 30, 100)

    def show_game_over(self):
        js.document.getElementById("game-over").style.display = "flex"
        js.document.getElementById("score").textContent = f"Score: {self.score}"


asset_manager = AssetManager()
game = None

async def main():
    global game
    game = Game(asset_manager)
    
    # Expose reset to JS
    def py_game_reset():
        if game:
            game.reset()
            game.set_difficulty(js.window.gameState.difficulty)
    
    js.window.pyGameReset = create_proxy(py_game_reset)

    while True:
        if asset_manager.is_ready() and js.window.gameState.gameStarted:
            if game.game_over and not js.window.gameState.isGameOver:
                 # If Python thinks game is over but JS reset it
                 game.reset()
            
            # Simple game loop
            game.update(0.016) # ~60fps
            game.draw()
        
        await asyncio.sleep(0.016)

asyncio.ensure_future(main())
