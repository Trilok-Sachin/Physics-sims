import pygame
import random
import math

# Constants
screen_width = 1400
screen_height = 800
background_color = (0, 0, 0)  # Black background
G = 50  # Gravitational constant
time_step = 0.01
body_radius_multiplier = 0.5
trail_length = 10

num_small_bodies = 150
num_large_bodies = 5

# Initialize Pygame
pygame.init()

# Create a Pygame screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("N-Body Simulation")  # Change the title to "N-Body Simulation"

# Define celestial bodies
bodies = []

# Function to map mass to a color using a normal distribution
def mass_to_color(mass, mass_max):

    # Scale mass to the range [0, 1]
    scaled_mass = (mass - mass_min) / (mass_max - mass_min)
    print(mass, mass_min)
    if scaled_mass>1:
        scaled_mass=0.95
    # Calculate the hue value (0 to 360 degrees)
    hue = int(scaled_mass * 360)
    # Convert hue to RGB
    rgb_color = pygame.Color(0)
    rgb_color.hsva = (hue, 50, 100, 100)  # Set saturation and value to 100, alpha to 100
    return rgb_color

# Initialize celestial bodies

masses = [random.uniform(1, 4) for _ in range(num_small_bodies)]
# masses = [0.5, 0.75, 0.2, 0.1]
large_masses = [random.uniform(100, 500) for _ in range(num_large_bodies)]
masses.extend(large_masses)

num_bodies = len(masses)
mass_min = min(masses)
mass_max = max(masses)

for i in range(num_bodies):
    mass = masses[i]
    initial_position = [random.uniform(0, screen_width), random.uniform(0, screen_height)]
    initial_velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
    
    # Calculate color based on mass (you can customize this color scale)
    # color = (int(255 * (mass / 10)), int(255 * (1 - (mass / 10))), 0)
    color = mass_to_color(mass, mass_max)
    
    body = {
        "mass": mass,
        "x": initial_position[0],
        "y": initial_position[1],
        "vx": initial_velocity[0],
        "vy": initial_velocity[1],
        "color": color,
        "trail": [],
    }
    bodies.append(body)

# Function to calculate the distance between two bodies
def distance(body1, body2):
    dx = body2["x"] - body1["x"]
    dy = body2["y"] - body1["y"]
    return math.sqrt(dx ** 2 + dy ** 2)



# Function to check for and handle collisions
def handle_collisions():
    for i, body in enumerate(bodies):
        for j, other_body in enumerate(bodies):
            if i != j:
                dx = other_body["x"] - body["x"]
                dy = other_body["y"] - body["y"]
                dist = distance(body, other_body)

                # Calculate the collision radius as the radius of the more massive object
                collision_radius = body_radius_multiplier*(max(math.sqrt(body["mass"]), math.sqrt(other_body["mass"])))

                if dist < collision_radius:
                    # Calculate the velocity reduction based on mass
                    reduction_factor = other_body["mass"] / (body["mass"] + other_body["mass"])
                    body["vx"] += reduction_factor * (other_body["vx"] - body["vx"])
                    body["vy"] += reduction_factor * (other_body["vy"] - body["vy"])

                    # Check if smaller object falls within 0.7 times the collision radius
                    if dist < 0.7 * collision_radius:
                        # Absorb the smaller object into the larger one
                        if body["mass"] >= other_body["mass"]:
                            # Increase the mass of the larger body
                            body["mass"] += other_body["mass"]
                            # if body["mass"]>mass_max:
                                # mass_max = 1.5*body["mass"]
                            # Change color based on new mass (you can customize this color scale)
                            # body["color"] = (int(255 * (body["mass"] / 10)), int(255 * (1 - (body["mass"] / 10))), 0)
                            body["color"] = mass_to_color(body["mass"], mass_max)
                            # Calculate new radius based on new mass
                            body["radius"] = int(math.sqrt(body["mass"]) * body_radius_multiplier)
                            # Remove the smaller body from the list
                            bodies.pop(j)
                        else:
                            other_body["mass"] += body["mass"]
                            # if other_body["mass"]>mass_max:
                                # mass_max = 1.5*other_body["mass"]
                            # other_body["color"] = (int(255 * (other_body["mass"] / 10)), int(255 * (1 - (other_body["mass"] / 10))), 0)
                            other_body["color"] = mass_to_color(other_body["mass"], mass_max)
                            other_body["radius"] = int(math.sqrt(other_body["mass"]) * body_radius_multiplier)
                            bodies.pop(i)

        # Bounce off the screen edges
        if body["x"] < 0 or body["x"] > screen_width:
            body["vx"] *= -1
        if body["y"] < 0 or body["y"] > screen_height:
            body["vy"] *= -1

# Function to display the number of bodies at the top right corner
def display_num_bodies(num):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Number of Bodies: {num}", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topright = (screen_width - 10, 10)
    screen.blit(text, text_rect)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update positions and velocities
    for i, body in enumerate(bodies):
        for j, other_body in enumerate(bodies):
            if i != j:
                dx = other_body["x"] - body["x"]
                dy = other_body["y"] - body["y"]
                dist = distance(body, other_body)

                force = (G * body["mass"] * other_body["mass"]) / (dist ** 2)
                angle = math.atan2(dy, dx)
                body["vx"] += (force / body["mass"]) * math.cos(angle) * time_step
                body["vy"] += (force / body["mass"]) * math.sin(angle) * time_step

        # Update positions
        body["x"] += body["vx"] * time_step
        body["y"] += body["vy"] * time_step

        # Store trail points
        body["trail"].append((int(body["x"]), int(body["y"])))

        # Limit the length of the trail
        if len(body["trail"]) > trail_length:
            body["trail"].pop(0)
    
    # Handle collisions
    handle_collisions()

    # Draw the bodies and trails
    screen.fill(background_color)
    for body in bodies:
        
        body_radius = int(math.sqrt(body["mass"]) * body_radius_multiplier)

        # Draw the trail
        for i in range(len(body["trail"]) - 1):
            pygame.draw.line(screen, body["color"], body["trail"][i], body["trail"][i + 1], 2)

        # Draw the body
        pygame.draw.circle(screen, body["color"], (int(body["x"]), int(body["y"])), body_radius)

    display_num_bodies(len(bodies))
    pygame.display.flip()

    # Control the frame rate
    pygame.time.delay(1)

# Quit Pygame
pygame.quit()
