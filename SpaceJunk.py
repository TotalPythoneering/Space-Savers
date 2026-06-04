# MISSION: Space Savers.
# STATUS: Public
# VERSION: 1.0.0
# NOTES: https://github.com/TotalPythoneering and https://www.youtube.com/@TotalPythoneering
# DATE: 2026-06-04 11:35:57
# FILE: SpaceJunk.py
# AUTHOR: Randall Nagy + Google A.I.
#
import tkinter as tk
import random
import math

# Configuration
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600
FONT_SIZE = 24
SPEED_MIN = 2
SPEED_MAX = 5
BASE_COLLISION_RADIUS = 25  # Maximum collision distance
PADDING = 25               # Margin to keep items away from window borders

# Explosion Particle Configuration
PARTICLES_PER_EXPLOSION = 12
PARTICLE_LIFETIME = 20      # Number of frames the explosion lasts
PARTICLE_SPEED = 4

VEHICLE_CHARS = [
    '🌟', '🌌', '🚗', '🚕', '🛩', '🌠', '🛰', '👽', '☀', '👾', 
    '🚚', '🛳', '🌀', '🚌', '🪐', '🚲', '🚙', '🌙', '🌑', '🚄', 
    '🛸', '☄', '🚁', '🌕', '🔭'
]

EXPLOSION_COLORS = [
    "#FF3333", "#FF6633", "#FF9933", "#FFCC33", "#FFFF33", # Reds/Yellows
    "#33FF33", "#33FF99", "#33FFFF", "#3399FF", "#3333FF", # Greens/Blues
    "#9933FF", "#FF33FF", "#FF3399"                       # Purples/Pinks
]

class BouncingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Simulation with Particle Explosions")
        
        self.width = INITIAL_WIDTH
        self.height = INITIAL_HEIGHT
        self.current_collision_radius = BASE_COLLISION_RADIUS
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#0b0f19", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.items = []
        self.particles = []  # List to track active explosion particles
        self.reset_pending = False
        
        self.setup_simulation()
        self.animate()

    def on_resize(self, event):
        """Track window dimensional changes."""
        self.width = event.width
        self.height = event.height

    def setup_simulation(self):
        """Spawns characters safely, dynamically scaling spacing parameters."""
        self.canvas.delete("all")
        self.items = []
        self.particles = [] # Clear leftover particles on reset
        
        max_x = max(PADDING + 10, self.width - PADDING)
        max_y = max(PADDING + 10, self.height - PADDING)
        
        screen_area = self.width * self.height
        if screen_area < 150000:
            self.current_collision_radius = max(5, int(math.sqrt(screen_area) / 15))
        else:
            self.current_collision_radius = BASE_COLLISION_RADIUS

        for char in VEHICLE_CHARS:
            x = random.randint(PADDING, max_x)
            y = random.randint(PADDING, max_y)
            
            dx = random.choice([-1, 1]) * random.uniform(SPEED_MIN, SPEED_MAX)
            dy = random.choice([-1, 1]) * random.uniform(SPEED_MIN, SPEED_MAX)
            
            canvas_id = self.canvas.create_text(
                x, y, 
                text=char, 
                font=("Segoe UI Symbol", FONT_SIZE), 
                fill="white"
            )
            
            self.items.append({
                "id": canvas_id,
                "dx": dx,
                "dy": dy
            })
            
        self.reset_pending = False

    def create_explosion(self, x, y):
        """Spawns expanding particle rings in a single random color."""
        color = random.choice(EXPLOSION_COLORS)
        
        for _ in range(PARTICLES_PER_EXPLOSION):
            # Distribute particle angles evenly around a circle
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, PARTICLE_SPEED)
            p_dx = math.cos(angle) * speed
            p_dy = math.sin(angle) * speed
            
            # Draw a tiny particle circle
            radius = random.randint(2, 4)
            p_id = self.canvas.create_oval(
                x - radius, y - radius, 
                x + radius, y + radius, 
                fill=color, outline=""
            )
            
            self.particles.append({
                "id": p_id,
                "dx": p_dx,
                "dy": p_dy,
                "life": PARTICLE_LIFETIME
            })

    def animate(self):
        """Continuous core loop processing movement, bounds, particles, and deaths."""
        # 1. Update and Animate Active Explosion Particles
        next_particles = []
        for p in self.particles:
            self.canvas.move(p["id"], p["dx"], p["dy"])
            p["life"] -= 1
            
            if p["life"] <= 0:
                self.canvas.delete(p["id"])
            else:
                next_particles.append(p)
        self.particles = next_particles

        # Skip character physics if a board reset is waiting out its delay
        if self.reset_pending:
            self.root.after(16, self.animate)
            return

        to_delete = set()
        collision_locations = []  # Keep track of where to spawn explosions
        
        # 2. Coordinate updates & strict bounding box clamping
        for item in self.items:
            self.canvas.move(item["id"], item["dx"], item["dy"])
            x, y = self.canvas.coords(item["id"])
            
            if x <= PADDING:
                item["dx"] = abs(item["dx"])
                self.canvas.coords(item["id"], PADDING + 1, y)
            elif x >= self.width - PADDING:
                item["dx"] = -abs(item["dx"])
                self.canvas.coords(item["id"], self.width - PADDING - 1, y)
                
            x, y = self.canvas.coords(item["id"])
            
            if y <= PADDING:
                item["dy"] = abs(item["dy"])
                self.canvas.coords(item["id"], x, PADDING + 1)
            elif y >= self.height - PADDING:
                item["dy"] = -abs(item["dy"])
                self.canvas.coords(item["id"], x, self.height - PADDING - 1)

        # 3. Distance checks
        num_items = len(self.items)
        for i in range(num_items):
            for j in range(i + 1, num_items):
                item1 = self.items[i]
                item2 = self.items[j]
                
                x1, y1 = self.canvas.coords(item1["id"])
                x2, y2 = self.canvas.coords(item2["id"])
                
                distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                if distance < self.current_collision_radius:
                    if item1["id"] not in to_delete and item2["id"] not in to_delete:
                        to_delete.add(item1["id"])
                        to_delete.add(item2["id"])
                        # Calculate midpoint of collision for explosion center
                        mid_x = (x1 + x2) / 2
                        mid_y = (y1 + y2) / 2
                        collision_locations.append((mid_x, mid_y))

        # 4. Clean elements and trigger visual effects
        if to_delete:
            for canvas_id in to_delete:
                self.canvas.delete(canvas_id)
            self.items = [item for item in self.items if item["id"] not in to_delete]
            
            # Fire off explosions at collision points
            for loc_x, loc_y in collision_locations:
                self.create_explosion(loc_x, loc_y)

        # 5. Schedule Reset without breaking loop sequence
        if len(self.items) <= 1:
            self.reset_pending = True
            # Extended delay slightly to 800ms so players see the last explosion finish
            self.root.after(800, self.setup_simulation)
        
        self.root.after(16, self.animate)

if __name__ == "__main__":
    window = tk.Tk()
    app = BouncingApp(window)
    window.mainloop()
