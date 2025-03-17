import pygame
import numpy as np
import time
import random
import os
import math
from config import *
from pygame.math import Vector2

class Vehicle:
    """Base class for all vehicles in the simulation"""
    def __init__(self, route, speed_multiplier=1.0):
        # Initialize basic vehicle properties
        self.route = route  # List of points defining the vehicle's path
        self.current_point = 0  # Index of current target point in route
        self.position = Vector2(route[0])  # Current position as 2D vector
        self.target = Vector2(route[1])  # Next target position as 2D vector
        self.direction = (self.target - self.position).normalize()  # Normalized direction vector
        self.speed = BASE_SPEED * speed_multiplier  # Vehicle speed with type multiplier
        self.angle = self.calculate_angle()  # Current rotation angle
        self.completed = False  # Flag for route completion
        self.waiting = False  # Flag for waiting state (at traffic lights or collisions)
        self.wait_time = 0  # Counter for waiting duration
        self.collision_radius = 40  # Radius for collision detection with other vehicles
        
    def calculate_angle(self):
        """Calculate the rotation angle based on movement direction"""
        # Convert direction vector to degrees for sprite rotation
        # atan2 gives angle in radians, convert to degrees
        # Negative y because pygame's y-axis is inverted
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        return angle

    def check_collision(self, other_vehicles):
        """Check for potential collisions with other vehicles"""
        for vehicle in other_vehicles:
            if vehicle != self:  # Don't check collision with self
                # Calculate distance between vehicles
                distance = (vehicle.position - self.position).length()
                if distance < self.collision_radius:  # If vehicles are too close
                    # Calculate dot product to determine relative direction
                    dot_product = self.direction.dot(vehicle.direction)
                    if dot_product > 0.5:  # Vehicles moving in similar direction
                        return True  # Slow down to avoid collision
                    else:  # Vehicles moving in different directions
                        self.try_change_direction()  # Try to change direction at intersection
                        return True
        return False

    def try_change_direction(self):
        """Attempt to change direction when at an intersection"""
        x, y = self.position.x, self.position.y
        
        # Check if vehicle is on a vertical road
        for road_x in [MAIN_VERTICAL_X1, MAIN_VERTICAL_X2, MAIN_VERTICAL_X3]:
            if abs(x - road_x) < ROAD_WIDTH:  # If on vertical road
                if abs(self.direction.x) > abs(self.direction.y):  # If moving horizontally
                    self.direction.y = random.choice([-1, 1])  # Change to vertical movement
                    self.direction.x = 0
                    self.angle = self.calculate_angle()
                    return

        # Check if vehicle is on a horizontal road
        for road_y in [MAIN_HORIZONTAL_Y, MAIN_HORIZONTAL_Y - 200]:
            if abs(y - road_y) < ROAD_WIDTH:  # If on horizontal road
                if abs(self.direction.y) > abs(self.direction.x):  # If moving vertically
                    self.direction.x = random.choice([-1, 1])  # Change to horizontal movement
                    self.direction.y = 0
                    self.angle = self.calculate_angle()
                    return

    def update(self, traffic_lights, other_vehicles=[]):
        """Update vehicle position and handle interactions"""
        # Skip update if vehicle has completed route or is waiting
        if self.completed or self.waiting:
            return

        # Check for collisions with other vehicles
        if self.check_collision(other_vehicles):
            self.waiting = True
            self.wait_time = random.randint(30, 60)  # Random wait duration
            return

        # Check proximity to traffic lights
        for light in traffic_lights:
            distance_to_light = (Vector2(light.x, light.y) - self.position).length()
            if distance_to_light < TRAFFIC_LIGHT_RADIUS * 2:  # If near traffic light
                if not light.is_green():  # Stop at red/yellow lights
                    self.waiting = True
                    self.wait_time = random.randint(30, 60)
                    return

        # Move vehicle towards target
        movement = self.direction * self.speed
        self.position += movement

        # Check if reached current target point
        if (self.target - self.position).length() < 5:  # Within 5 pixels of target
            self.current_point += 1
            if self.current_point >= len(self.route):
                self.completed = True  # Route completed
            else:
                # Update to next target point
                self.position = Vector2(self.route[self.current_point - 1])
                self.target = Vector2(self.route[self.current_point])
                self.direction = (self.target - self.position).normalize()
                self.angle = self.calculate_angle()

    def reduce_wait_time(self):
        """Reduce waiting time and resume movement when done"""
        if self.waiting:
            self.wait_time -= 1
            if self.wait_time <= 0:
                self.waiting = False  # Resume movement

    def draw(self, screen):
        """Draw vehicle sprite on the screen"""
        if hasattr(self, 'image'):  # If vehicle has an image sprite
            # Rotate image based on movement direction
            rotated_image = pygame.transform.rotate(self.image, -self.angle)
            rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
            screen.blit(rotated_image, rect)

class Ambulance(Vehicle):
    """Special vehicle class for ambulance with priority movement"""
    def __init__(self, route):
        # Initialize ambulance with special properties
        super().__init__(route, AMBULANCE_SPEED)
        self.started = False  # Flag for ambulance start
        self.reached_hospital = False  # Flag for hospital arrival
        self.image = pygame.image.load("assets/ambulance.png")  # Load ambulance sprite
        self.image = pygame.transform.scale(self.image, (80, 40))  # Scale sprite
        
    def update(self, traffic_lights):
        """Update ambulance position (ignores traffic lights)"""
        # Skip update if not started or already at hospital
        if not self.started or self.reached_hospital:
            return
            
        # Move ambulance (ignores traffic lights)
        movement = self.direction * self.speed
        self.position += movement

        # Check if reached current target
        if (self.target - self.position).length() < 5:
            self.current_point += 1
            if self.current_point >= len(self.route):
                self.reached_hospital = True  # Arrived at hospital
            else:
                # Update to next target point
                self.position = Vector2(self.route[self.current_point - 1])
                self.target = Vector2(self.route[self.current_point])
                self.direction = (self.target - self.position).normalize()
                self.angle = self.calculate_angle()

class Car(Vehicle):
    """Regular car vehicle class"""
    def __init__(self, route):
        super().__init__(route, CAR_SPEED)
        self.image = pygame.image.load("assets/car.png")  # Load car sprite
        self.image = pygame.transform.scale(self.image, (60, 30))  # Scale sprite

class Truck(Vehicle):
    """Larger truck vehicle class"""
    def __init__(self, route):
        super().__init__(route, TRUCK_SPEED)
        self.image = pygame.image.load("assets/truck.png")  # Load truck sprite
        self.image = pygame.transform.scale(self.image, (80, 40))  # Scale sprite

class Bike(Vehicle):
    """Smaller bike vehicle class"""
    def __init__(self, route):
        super().__init__(route, BIKE_SPEED)
        self.image = pygame.image.load("assets/bike.png")  # Load bike sprite
        self.image = pygame.transform.scale(self.image, (40, 20))  # Scale sprite

class TrafficLight:
    """Traffic light class with normal operation and ambulance override"""
    def __init__(self, x, y):
        self.x = x  # X position
        self.y = y  # Y position
        self.state = "red"  # Initial state
        self.last_change = pygame.time.get_ticks()  # Time of last state change
        self.forced_green = False  # Flag for ambulance-forced green state
    
    def is_green(self):
        """Check if light is currently green"""
        return self.state == "green"
    
    def update(self, ambulance_pos):
        """Update traffic light state based on timing and ambulance position"""
        current_time = pygame.time.get_ticks()
        # Calculate distance to ambulance
        distance = np.sqrt((self.x - ambulance_pos[0])**2 + (self.y - ambulance_pos[1])**2)
        
        # Force green if ambulance is nearby
        if distance < DETECTION_RADIUS and not self.forced_green:
            self.state = "green"
            self.forced_green = True
            self.last_change = current_time
        
        # Normal traffic light cycle
        elif not self.forced_green:
            time_in_state = current_time - self.last_change
            
            # State transitions based on timing
            if self.state == "red" and time_in_state >= NORMAL_RED_TIME:
                self.state = "green"
                self.last_change = current_time
            elif self.state == "green" and time_in_state >= NORMAL_GREEN_TIME:
                self.state = "yellow"
                self.last_change = current_time
            elif self.state == "yellow" and time_in_state >= NORMAL_YELLOW_TIME:
                self.state = "red"
                self.last_change = current_time
        
        # Reset to normal operation when ambulance is gone
        elif self.forced_green and distance > DETECTION_RADIUS:
            self.forced_green = False
            self.state = "red"
            self.last_change = current_time

    def draw(self, screen):
        """Draw traffic light with housing and colored lights"""
        # Draw traffic light housing (black rectangle)
        pygame.draw.rect(screen, BLACK, (self.x - 15, self.y - 35, 30, 70))
        
        # Define colors and positions for lights
        colors = {"red": RED, "yellow": YELLOW, "green": GREEN}
        positions = {"red": -25, "yellow": 0, "green": 25}
        
        # Draw each light (active or inactive)
        for light, y_offset in positions.items():
            # Use full color for active light, dim for inactive
            color = colors[light] if self.state == light else (40, 40, 40)
            pygame.draw.circle(screen, color, (self.x, self.y + y_offset), TRAFFIC_LIGHT_RADIUS) 