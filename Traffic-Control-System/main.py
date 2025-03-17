# Import necessary libraries
import pygame  # For game development and graphics
import sys  # For system operations
import random  # For generating random values
from traffic_system import TrafficLight, Ambulance, Car, Truck, Bike  # Import vehicle classes
from config import *  # Import all configuration variables

class Simulation:
    def __init__(self):
        # Initialize Pygame and create the game window
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Smart Traffic Control System")
        self.clock = pygame.time.Clock()  # For controlling frame rate
        self.font = pygame.font.Font(None, FONT_SIZE)  # Font for messages
        self.reset_simulation()  # Initialize simulation state

    def reset_simulation(self):
        # Create traffic lights at specified positions
        self.traffic_lights = [TrafficLight(x, y) for x, y in TRAFFIC_LIGHTS]
        
        # Initialize ambulance with random route
        chosen_route = random.choice(ROUTE_POINTS)
        self.ambulance = Ambulance(chosen_route)
        self.ambulance.started = False
        self.ambulance.reached_hospital = False
        self.show_message("Press SPACE to start the ambulance!")
        
        # Initialize vehicle lists with specified counts
        self.vehicles = []
        
        # Add initial cars
        for _ in range(INITIAL_CARS):
            route = random.choice(CAR_ROUTES)
            self.vehicles.append(Car(route))
        
        # Add initial trucks
        for _ in range(INITIAL_TRUCKS):
            route = random.choice(TRUCK_ROUTES)
            self.vehicles.append(Truck(route))
        
        # Add initial bikes
        for _ in range(INITIAL_BIKES):
            route = random.choice(BIKE_ROUTES)
            self.vehicles.append(Bike(route))

        # Initialize timing and message variables
        self.start_time = None
        self.message = ""
        self.message_time = 0

    def draw_roads(self):
        # Fill background with grass
        self.screen.fill(GRASS_COLOR)
        
        # Draw vertical roads with lane markers
        for x in [MAIN_VERTICAL_X1, MAIN_VERTICAL_X2, MAIN_VERTICAL_X3]:
            # Draw road
            pygame.draw.rect(self.screen, ROAD_COLOR, 
                           (x - ROAD_WIDTH//2, 0, ROAD_WIDTH, WINDOW_HEIGHT))
            # Draw lane markers
            for y in range(0, WINDOW_HEIGHT, LANE_MARKER_LENGTH + LANE_MARKER_GAP):
                pygame.draw.rect(self.screen, YELLOW, 
                               (x - LANE_MARKER_WIDTH//2, y, 
                                LANE_MARKER_WIDTH, LANE_MARKER_LENGTH))
        
        # Draw horizontal roads with lane markers
        for y in [MAIN_HORIZONTAL_Y, MAIN_HORIZONTAL_Y - 200]:
            # Draw road
            pygame.draw.rect(self.screen, ROAD_COLOR, 
                           (0, y - ROAD_WIDTH//2, WINDOW_WIDTH, ROAD_WIDTH))
            # Draw lane markers
            for x in range(0, WINDOW_WIDTH, LANE_MARKER_LENGTH + LANE_MARKER_GAP):
                pygame.draw.rect(self.screen, YELLOW, 
                               (x, y - LANE_MARKER_WIDTH//2,
                                LANE_MARKER_LENGTH, LANE_MARKER_WIDTH))
        
        # Draw hospital building and details
        pygame.draw.rect(self.screen, WHITE, 
                        (HOSPITAL_X - HOSPITAL_WIDTH//2, HOSPITAL_Y,
                         HOSPITAL_WIDTH, HOSPITAL_HEIGHT))
        
        # Draw hospital cross
        cross_color = RED
        cross_width = 60
        cross_height = 60
        cross_x = HOSPITAL_X - cross_width//2
        cross_y = HOSPITAL_Y + 20
        
        # Add hospital text
        font = pygame.font.Font(None, UI_FONT_SIZE)
        text = font.render("HOSPITAL", True, BLACK)
        text_rect = text.get_rect(center=(HOSPITAL_X, HOSPITAL_Y + 10))
        self.screen.blit(text, text_rect)
        
        # Draw hospital cross (vertical part)
        pygame.draw.rect(self.screen, cross_color,
                        (cross_x + cross_width//3, cross_y,
                         cross_width//3, cross_height))
        # Draw hospital cross (horizontal part)
        pygame.draw.rect(self.screen, cross_color,
                        (cross_x, cross_y + cross_height//3,
                         cross_width, cross_height//3))

        # Draw sidewalks along roads
        sidewalk_width = 10
        # Vertical road sidewalks
        for x in [MAIN_VERTICAL_X1, MAIN_VERTICAL_X2, MAIN_VERTICAL_X3]:
            pygame.draw.rect(self.screen, SIDEWALK_COLOR,
                           (x - ROAD_WIDTH//2 - sidewalk_width, 0,
                            sidewalk_width, WINDOW_HEIGHT))
            pygame.draw.rect(self.screen, SIDEWALK_COLOR,
                           (x + ROAD_WIDTH//2, 0,
                            sidewalk_width, WINDOW_HEIGHT))
        
        # Horizontal road sidewalks
        for y in [MAIN_HORIZONTAL_Y, MAIN_HORIZONTAL_Y - 200]:
            pygame.draw.rect(self.screen, SIDEWALK_COLOR,
                           (0, y - ROAD_WIDTH//2 - sidewalk_width,
                            WINDOW_WIDTH, sidewalk_width))
            pygame.draw.rect(self.screen, SIDEWALK_COLOR,
                           (0, y + ROAD_WIDTH//2,
                            WINDOW_WIDTH, sidewalk_width))

    def show_message(self, text):
        # Update message text and timing
        self.message = text
        self.message_time = pygame.time.get_ticks()

    def draw_message(self):
        # Draw message if it's within display duration
        if self.message and pygame.time.get_ticks() - self.message_time < MESSAGE_DURATION:
            # Create text surface with white text on black background
            text_surface = self.font.render(self.message, True, WHITE, BLACK)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, 50))
            # Add black background with padding
            bg_rect = text_rect.copy()
            bg_rect.inflate_ip(20, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            self.screen.blit(text_surface, text_rect)
        else:
            self.message = ""  # Clear message when duration expires

    def run(self):
        # Initialize game loop variables
        clock = pygame.time.Clock()
        running = True
        message_shown = False  # Track if hospital arrival message shown
        
        # Main game loop
        while running:
            # Handle events (keyboard, mouse, quit)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.reset_simulation()
                        message_shown = False
                    elif event.key == pygame.K_SPACE and not self.ambulance.started:
                        # Start ambulance when space is pressed
                        self.ambulance.started = True
                        self.show_message("Ambulance is starting!")
                        self.start_time = pygame.time.get_ticks()
                        message_shown = False
            
            # Draw background and roads
            self.draw_roads()
            
            # Update and draw traffic lights
            for light in self.traffic_lights:
                light.update((self.ambulance.position.x, self.ambulance.position.y))
                light.draw(self.screen)
            
            # Update and draw vehicles with collision avoidance
            for vehicle in self.vehicles:
                if vehicle.waiting:
                    vehicle.reduce_wait_time()
                vehicle.update(self.traffic_lights, self.vehicles)
                vehicle.draw(self.screen)
            
            # Update and draw ambulance
            self.ambulance.update(self.traffic_lights)
            self.ambulance.draw(self.screen)
            
            # Check if ambulance reached hospital
            if self.ambulance.started and not self.ambulance.reached_hospital and self.ambulance.completed:
                if not message_shown:
                    self.ambulance.reached_hospital = True
                    self.show_message("Ambulance Successfully Reached Hospital!")
                    message_shown = True

            # Draw any active messages
            self.draw_message()
            
            # Update display and maintain frame rate
            pygame.display.flip()
            clock.tick(FPS)
        
        # Clean up when simulation ends
        pygame.quit()

# Start simulation when run directly
if __name__ == "__main__":
    simulation = Simulation()
    simulation.run() 