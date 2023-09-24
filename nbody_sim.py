import pygame
import random
import math

# Constants
screen_width = 1400
screen_height = 800
background_color = (0, 0, 0)  # Black background
G = 1  # Gravitational constant
time_step = 0.02  # Decreased time step for smoother animation
body_radius_multiplier = 0.2  # Multiplier for body size based on mass
trail_length = 100  # Number of previous positions to display as trails

# Initialize Pygame
pygame.init()

# Create a Pygame screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("N-Body Simulation")

# Define celestial bodies
bodies = []

# Initialize celestial bodies
num_bodies = 250
for _ in range(num_bodies):
    mass = random.uniform(1, 10)
    initial_position = [random.uniform(0, screen_width), random.uniform(0, screen_height)]
    initial_velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
    body = {
        "mass": mass,
        "x": initial_position[0],
        "y": initial_position[1],
        "vx": initial_velocity[0],
        "vy": initial_velocity[1],
        "color": (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
        "trail": [],
    }
    bodies.append(body)

# Create a font for displaying text
font = pygame.font.Font(None, 24)

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
                distance = math.sqrt(dx ** 2 + dy ** 2)
                force = (G * body["mass"] * other_body["mass"]) / (distance ** 2)
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

        # Bounce off the screen edges
        if body["x"] < 0 or body["x"] > screen_width:
            body["vx"] *= -1
        if body["y"] < 0 or body["y"] > screen_height:
            body["vy"] *= -1

    # Draw the bodies, trails, and mass
    screen.fill(background_color)
    for body in bodies:
        body_radius = int(math.sqrt(body["mass"]) * body_radius_multiplier)

        # Draw the trail
        for i in range(len(body["trail"]) - 1):
            pygame.draw.line(screen, body["color"], body["trail"][i], body["trail"][i + 1], 2)

        # Draw the body
        pygame.draw.circle(screen, body["color"], (int(body["x"]), int(body["y"])), body_radius)

        # Display the mass
        # mass_text = font.render(f"Mass: {body['mass']:.2f}", True, (255, 255, 255))
        # screen.blit(mass_text, (int(body["x"]) - 20, int(body["y"]) + body_radius + 5))

    pygame.display.flip()

    # Control the frame rate
    pygame.time.delay(2)  # Decreased delay for smoother animation

# Quit Pygame
pygame.quit()
