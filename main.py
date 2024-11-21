import pygame
import sys
import math  # Use the math module for trigonometric functions
from kuksa_client.grpc import VSSClient
from threading import Thread, Lock

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vehicle Dashboard")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.SysFont("Arial", 24)

# Dashboard values
brake = 0     # Percentage
steering_angle = 0  # Degrees

# Shared speed value and lock
values = {"speed": 0,"brake":0, "acceleration":0, "steering_angle":0}
speed_lock = Lock()

# Utility function to draw a needle for steering angle
def draw_needle(center, angle, radius, color=RED):
    radians = math.radians(angle)
    end_x = center[0] + radius * math.cos(radians)
    end_y = center[1] - radius * math.sin(radians)
    pygame.draw.line(screen, color, center, (end_x, end_y), 2)

# Kuksa client thread
def start_kuksa_client():
    try:
        with VSSClient('127.0.0.1', 55555) as client:
            for updates in client.subscribe_current_values(['Vehicle.Speed', 'Vehicle.Chassis.Brake.PedalPosition', 'Vehicle.Chassis.Accelerator.PedalPosition', 'Vehicle.Chassis.Axle.Row1.SteeringAngle']):  
                print(updates) 
                with speed_lock:
                    if updates.get('Vehicle.Speed') and updates['Vehicle.Speed'].value:
                        values["speed"] = updates['Vehicle.Speed'].value
                    #elif(values['speed']!=0):
                    #    values["speed"] = 0 
                    else:
                        print(f"Received updated speed: {values['speed']}", flush=True)
                    if updates.get('Vehicle.Chassis.Brake.PedalPosition') and updates['Vehicle.Chassis.Brake.PedalPosition'].value:
                        values["brake"] = updates['Vehicle.Chassis.Brake.PedalPosition'].value
                    #elif(values["brake"] != 0 ):
                    #    values["brake"] = 0 
                    else:
                        print(f"Received updated brake: {values['brake']}", flush=True)
                    if updates.get('Vehicle.Chassis.Accelerator.PedalPosition') and updates['Vehicle.Chassis.Accelerator.PedalPosition'].value:
                        values["acceleration"] = updates['Vehicle.Chassis.Accelerator.PedalPosition'].value
                   # elif(values["acceleration"] != 0):
                   #     values["acceleration"] = 0
                    else:
                        print(f"Received updated acceleration: {values['acceleration']}", flush=True)

                    # Update steering angle
                    if updates.get('Vehicle.Chassis.Axle.Row1.SteeringAngle') and updates['Vehicle.Chassis.Axle.Row1.SteeringAngle'].value:
                        values["steering_angle"] = updates['Vehicle.Chassis.Axle.Row1.SteeringAngle'].value
                    #elif(values["steering_angle"] != 0):
                    #    values["steering_angle"] = 0
                    else:
                        print(f"Received updated steering_angle: {values['steering_angle']}", flush=True)

                    #values["acceleration"] = updates['Vehicle.Chassis.Accelerator.PedalPosition'] and updates['Vehicle.Chassis.Accelerator.PedalPosition'].value if updates['Vehicle.Chassis.Accelerator.PedalPosition'] != None else 0
                    #print(f"Received updated acceleration: {values['acceleration']}", flush=True)
                    #values["steering_angle"] = updates['Vehicle.Chassis.Axle.Row1.SteeringAngle'] and updates['Vehicle.Chassis.Axle.Row1.SteeringAngle'].value if updates['Vehicle.Chassis.Axle.Row1.SteeringAngle'] != None else 0
                    #print(f"Received updated steering_angle: {values['steering_angle']}", flush=True)
    except Exception as e:
        print(f"Kuksa client error: {e}", flush=True)

# Start Kuksa client thread
kuksa_thread = Thread(target=start_kuksa_client, daemon=True)
kuksa_thread.start()

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read speed safely
    with speed_lock:
        current_speed = values["speed"]
        brake = values["brake"]
        steering_angle = values["steering_angle"]

    # Draw throttle bar
    pygame.draw.rect(screen, GRAY, (50, 50, 200, 30))  # Background
    pygame.draw.rect(screen, GREEN, (50, 50, 2 * min(current_speed, 100), 30))  # Foreground
    throttle_text = font.render(f"Throttle: {current_speed}%", True, WHITE)
    screen.blit(throttle_text, (50, 90))

    # Draw brake bar
    pygame.draw.rect(screen, GRAY, (50, 150, 200, 30))  # Background
    pygame.draw.rect(screen, RED, (50, 150, 2 * brake, 30))  # Foreground
    brake_text = font.render(f"Brake: {brake}%", True, WHITE)
    screen.blit(brake_text, (50, 190))

    # Draw steering angle
    pygame.draw.circle(screen, GRAY, (400, 200), 100)  # Steering wheel
    draw_needle((400, 200), -steering_angle, 90)  # Needle
    steering_text = font.render(f"Steering: {steering_angle}°", True, WHITE)
    screen.blit(steering_text, (350, 310))

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Clean up and exit
pygame.quit()
sys.exit()
