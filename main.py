import pygame
import sys
import math  # Use the math module for trigonometric functions
# from kuksa_client.grpc import VSSClient

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
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Font
font = pygame.font.SysFont("Arial", 24)

# Dashboard values
throttle = 50  # Percentage
brake = 20     # Percentage
steering_angle = 30  # Degrees

# Utility function to draw a needle for steering angle
def draw_needle(center, angle, radius, color=RED):
    # Convert angle to radians and calculate the end point
    radians = math.radians(angle)
    end_x = center[0] + radius * math.cos(radians)
    end_y = center[1] - radius * math.sin(radians)
    pygame.draw.line(screen, color, center, (end_x, end_y), 2)

# Main loop
clock = pygame.time.Clock()
running = True
# with VSSClient('127.0.0.1', 55555) as client:
while running:

        

        # for updates in client.subscribe_current_values([
        #         'Vehicle.Speed',
        #     ]):
        #         speed = updates['Vehicle.Speed'].value
        #         print(f"Received updated speed: {speed}")
            
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw throttle bar
        pygame.draw.rect(screen, GRAY, (50, 50, 200, 30))  # Background
        pygame.draw.rect(screen, GREEN, (50, 50, 2 * throttle, 30))  # Foreground
        throttle_text = font.render(f"Throttle: {throttle}%", True, WHITE)
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

pygame.quit()
sys.exit()
