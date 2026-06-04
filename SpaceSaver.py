# MISSION: Space Savers.
# STATUS: Public
# VERSION: 1.0.1
# NOTES: https://github.com/TotalPythoneering and https://www.youtube.com/@TotalPythoneering
# DATE: 2026-06-04 11:33:13
# FILE: SpaceSaver.py
# AUTHOR: Randall Nagy + Google A.I.
#
import tkinter as tk
import random
import math

class UnicodeFlyer:
    def __init__(self, root):
        self.root = root
        self.root.title("Unicode Vehicle Flyer")
        
        # Configure full screen or large window
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.configure(bg="black")
        
        # Canvas for rendering vehicles
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind left mouse click to rocket launch function
        self.canvas.bind("<Button-1>", self.launch_rocket)
        
        # Game stats tracking
        self.rockets_launched = 0
        self.objects_destroyed = 0
        self.total_targets = 15
        
        # Create scoreboard text item
        self.score_text_id = self.canvas.create_text(
            20, 20,
            anchor="nw",
            text="",
            font=("Courier", 16, "bold"),
            fill="#00FF00"
        )
        self.update_scoreboard()
        
        # List of unicode vehicle characters for ambient traffic
        self.vehicles = [
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
        
        # Separate lists for tracking items, rockets, and explosion particles
        self.active_items = []
        self.active_rockets = []
        self.particles = []
        
        # Firework color palette options
        self.firework_colors = [
            ["#FF1493", "#FF69B4", "#FFC0CB"],  # Pinks
            ["#00FFFF", "#00BFFF", "#1E90FF"],  # Cyan / Blues
            ["#00FF00", "#7FFF00", "#ADFF2F"],  # Lime Greens
            ["#FF4500", "#FF8C00", "#FFD700"],  # Orange / Golds
            ["#9400D3", "#8A2BE2", "#BA55D3"]   # Purples
        ]
        
        # Track restarting state to avoid multiple simultaneous spawns
        self.is_restarting = False
        
        # Initialize vehicle population
        self.spawn_initial_vehicles(self.total_targets)
        self.animate()

    def update_scoreboard(self):
        # Calculate accuracy safely to avoid dividing by zero
        accuracy = (self.objects_destroyed / self.rockets_launched * 100) if self.rockets_launched > 0 else 0
        
        stats_text = (
            f"Rockets Fired: {self.rockets_launched}\n"
            f"Destroyed    : {self.objects_destroyed}\n"
            f"Remaining    : {len(self.active_items) if hasattr(self, 'active_items') else self.total_targets}\n"
            f"Accuracy     : {accuracy:.1f}%"
        )
        self.canvas.itemconfig(self.score_text_id, text=stats_text)

    def spawn_initial_vehicles(self, count):
        for _ in range(count):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            char = random.choice(self.vehicles)
            self.create_vehicle(x, y, char)

    def launch_rocket(self, event):
        if self.is_restarting:
            return
            
        target_x = event.x
        target_y = event.y
        
        spawn_x = target_x
        spawn_y = self.height - 30
        
        dx = 0
        dy = -12  
        size = 32
        
        item_id = self.canvas.create_text(
            spawn_x, spawn_y, 
            text="🚀", 
            font=("Arial", size), 
            fill="white"
        )
        
        self.active_rockets.append({
            "id": item_id,
            "dx": dx,
            "dy": dy,
            "size": size,
            "target_y": target_y  
        })
        
        # Increment tracking and update ui immediately
        self.rockets_launched += 1
        self.update_scoreboard()

    def create_vehicle(self, x, y, char):
        dx = random.choice([-1, 1]) * random.randint(2, 4)
        dy = random.choice([-1, 1]) * random.randint(2, 4)
        size = random.randint(24, 48)
        
        item_id = self.canvas.create_text(
            x, y, 
            text=char, 
            font=("Arial", size), 
            fill="white"
        )
        
        self.active_items.append({
            "id": item_id,
            "dx": dx,
            "dy": dy,
            "size": size
        })

    def create_firework(self, x, y):
        color_scheme = random.choice(self.firework_colors)
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            p_dx = math.cos(angle) * speed
            p_dy = math.sin(angle) * speed
            
            color = random.choice(color_scheme)
            radius = random.randint(2, 4)
            
            p_id = self.canvas.create_oval(
                x - radius, y - radius, 
                x + radius, y + radius, 
                fill=color, 
                outline=""
            )
            
            self.particles.append({
                "id": p_id,
                "dx": p_dx,
                "dy": p_dy,
                "life": random.randint(20, 35),  
                "gravity": 0.15                  
            })

    def trigger_restart(self):
        self.canvas.delete("all")
        self.active_rockets.clear()
        self.particles.clear()
        
        # Re-create scoreboard for the new round
        self.score_text_id = self.canvas.create_text(
            20, 20,
            anchor="nw",
            text="",
            font=("Courier", 16, "bold"),
            fill="#00FF00"
        )
        self.update_scoreboard()
        
        self.spawn_initial_vehicles(self.total_targets)
        self.is_restarting = False

    def animate(self):
        # 1. Move regular vehicles and bounce off boundaries
        for item in self.active_items:
            self.canvas.move(item["id"], item["dx"], item["dy"])
            pos = self.canvas.coords(item["id"])
            if pos and len(pos) >= 2:
                x, y = pos[0], pos[1]
                if x <= 0 or x >= self.width:
                    item["dx"] = -item["dx"]
                if y <= 0 or y >= self.height:
                    item["dy"] = -item["dy"]

        # 2. Move ascending rockets and check conditions
        rockets_to_remove = []
        items_to_remove = []

        for rocket in self.active_rockets:
            self.canvas.move(rocket["id"], rocket["dx"], rocket["dy"])
            r_pos = self.canvas.coords(rocket["id"])
            
            if not r_pos or len(r_pos) < 2:
                continue
                
            rx, ry = r_pos[0], r_pos[1]
            exploded = False

            if ry <= rocket["target_y"]:
                self.create_firework(rx, ry)
                self.canvas.delete(rocket["id"])
                rockets_to_remove.append(rocket)
                continue

            if rx <= 0 or rx >= self.width or ry <= 0 or ry >= self.height:
                self.create_firework(rx, ry)
                self.canvas.delete(rocket["id"])
                rockets_to_remove.append(rocket)
                continue

            for item in self.active_items:
                i_pos = self.canvas.coords(item["id"])
                if i_pos and len(i_pos) >= 2:
                    ix, iy = i_pos[0], i_pos[1]
                    distance = math.sqrt((rx - ix)**2 + (ry - iy)**2)
                    collision_threshold = (rocket["size"] + item["size"]) / 2
                    
                    if distance < collision_threshold:
                        self.create_firework((rx + ix) / 2, (ry + iy) / 2)
                        self.canvas.delete(rocket["id"])
                        self.canvas.delete(item["id"])
                        rockets_to_remove.append(rocket)
                        items_to_remove.append(item)
                        
                        # Increment objects hit and refresh UI
                        self.objects_destroyed += 1
                        exploded = True
                        break
            
            if exploded:
                continue

        # Clean up destroyed objects from our lists
        for r in rockets_to_remove:
            if r in self.active_rockets:
                self.active_rockets.remove(r)
        for i in items_to_remove:
            if i in self.active_items:
                self.active_items.remove(i)
                # Keep real-time remaining target count correct
                self.update_scoreboard()

        # 3. Animate firework spark particles
        particles_to_remove = []
        for p in self.particles:
            p["dy"] += p["gravity"]
            self.canvas.move(p["id"], p["dx"], p["dy"])
            
            p["life"] -= 1
            if p["life"] <= 0:
                self.canvas.delete(p["id"])
                particles_to_remove.append(p)
                
        for p in particles_to_remove:
            if p in self.particles:
                self.particles.remove(p)

        # Check if all moving objects are gone
        if len(self.active_items) == 0 and not self.is_restarting:
            self.is_restarting = True
            self.root.after(1500, self.trigger_restart)

        # Loop animation every 20 milliseconds
        self.root.after(20, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = UnicodeFlyer(root)
    root.mainloop()
