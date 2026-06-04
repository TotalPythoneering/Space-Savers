# MISSION: Space Savers.
# STATUS: Public
# VERSION: 1.0.0
# NOTES: https://github.com/TotalPythoneering and https://www.youtube.com/@TotalPythoneering
# DATE: 2026-06-04 11:47:55
# FILE: ScreenSaver.py
# AUTHOR: Randall Nagy + Google A.I.
#
import tkinter as tk
import random
import math

# Define a list of Unicode vehicle characters (cars, trucks, planes, trains)
VEHICLE_CHARS = [
    '🌟', # GLOWING STAR
    '🌌', # MILKY WAY
    '🚗', # AUTOMOBILE
    '🚕', # TAXI
    '🛩', # SMALL AIRPLANE
    '🌠', # SHOOTING STAR
    '🛰', # SATELLITE
    '👽', # EXTRATERRESTRIAL ALIEN
    '☀', # BLACK SUN WITH RAYS
    '👾', # ALIEN MONSTER
    '🚚', # DELIVERY TRUCK
    '🛳', # PASSENGER SHIP
    '🌀', # CYCLONE
    '🚌', # BUS
    '🪐', # RINGED PLANET
    '🚲', # BICYCLE
    '🚙', # RECREATIONAL VEHICLE
    '🌙', # CRESCENT MOON
    '🌑', # NEW MOON SYMBOL
    '🚄', # HIGH-SPEED TRAIN
    '🛸', # FLYING SAUCER
    '☄', # COMET
    '🚁', # HELICOPTER
    '🌕', # FULL MOON SYMBOL
    '🔭', # TELESCOPE
]

class FlyingVehicles:
    def __init__(self, root):
        self.root = root
        self.root.title("Flying Vehicles 🚗✈️")
        self.root.geometry("800x600")
        
        # Black background for a night-sky or void look
        self.canvas = tk.Canvas(root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.vehicles = []
        self.num_vehicles = 15
        self.speed_range = (2, 6)
        self.font_size = 40
        
        # Spawn the vehicles after the window is fully drawn
        self.canvas.bind("<Configure>", self.spawn_vehicles)
        
        # Start the animation loop
        self.animate()

    def spawn_vehicles(self, event=None):
        # Prevent re-spawning if already initialized
        if self.vehicles:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        for _ in range(self.num_vehicles):
            char = random.choice(VEHICLE_CHARS)
            
            # Start at a random location
            x = random.randint(50, canvas_width - 50)
            y = random.randint(50, canvas_height - 50)
            
            # Random direction (angle in radians)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*self.speed_range)
            
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            
            # Create the text object on the canvas
            text_id = self.canvas.create_text(
                x, y, 
                text=char, 
                font=('Arial', self.font_size), 
                fill='white'
            )
            
            self.vehicles.append({
                'id': text_id,
                'dx': dx,
                'dy': dy
            })

    def animate(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Approximate size of bounding box for the character
        padding = self.font_size // 2 

        for v in self.vehicles:
            # Move the object
            self.canvas.move(v['id'], v['dx'], v['dy'])
            
            # Check current position
            pos = self.canvas.coords(v['id'])
            if not pos:
                continue
                
            x, y = pos[0], pos[1]
            
            # Bounce off the walls
            if x <= padding and v['dx'] < 0:
                v['dx'] = -v['dx']
            elif x >= (canvas_width - padding) and v['dx'] > 0:
                v['dx'] = -v['dx']
                
            if y <= padding and v['dy'] < 0:
                v['dy'] = -v['dy']
            elif y >= (canvas_height - padding) and v['dy'] > 0:
                v['dy'] = -v['dy']

        # Call animate() again in 20 milliseconds (approx. 50 FPS)
        self.root.after(20, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlyingVehicles(root)
    root.mainloop()
