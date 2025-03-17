# Window Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
DARK_RED = (139, 0, 0)
SILVER = (192, 192, 192)
ROAD_COLOR = (128, 128, 128)
GRASS_COLOR = (34, 139, 34)
SIDEWALK_COLOR = (192, 192, 192)

# Vehicle Counts
MAX_VEHICLES = 8
INITIAL_CARS = 3
INITIAL_TRUCKS = 2
INITIAL_BIKES = 3

# Road Configuration
ROAD_WIDTH = 60
INTERSECTION_SIZE = 100
LANE_MARKER_WIDTH = 4
LANE_MARKER_LENGTH = 30
LANE_MARKER_GAP = 20

# Traffic Light Configuration
TRAFFIC_LIGHT_RADIUS = 8  # Radius of each light circle
LIGHT_RADIUS = 8  # For backwards compatibility
DETECTION_RADIUS = 50  # Distance at which ambulance triggers green light
NORMAL_RED_TIME = 5000  # Duration of red light in milliseconds
NORMAL_GREEN_TIME = 5000  # Duration of green light in milliseconds
NORMAL_YELLOW_TIME = 2000  # Duration of yellow light in milliseconds
TRAFFIC_LIGHT_TIMING = 150  # Frames between light changes

# Vehicle Configuration
AMBULANCE_WIDTH = 70
AMBULANCE_HEIGHT = 45
AMBULANCE_SPEED = 0.4

CAR_WIDTH = 50
CAR_HEIGHT = 30
CAR_SPEED = 0.25

TRUCK_WIDTH = 70
TRUCK_HEIGHT = 40
TRUCK_SPEED = 0.2

BIKE_WIDTH = 30
BIKE_HEIGHT = 20
BIKE_SPEED = 0.3

# Message Configuration
FONT_SIZE = 42
MESSAGE_DURATION = 3000
UI_FONT_SIZE = 36

# Route Configuration
MAIN_HORIZONTAL_Y = 400
MAIN_VERTICAL_X1 = 200
MAIN_VERTICAL_X2 = 400
MAIN_VERTICAL_X3 = 600

# Hospital Configuration
HOSPITAL_X = WINDOW_WIDTH - 120  # Original position near the right edge
HOSPITAL_Y = MAIN_HORIZONTAL_Y - 60  # Original position near the main road
HOSPITAL_WIDTH = 100
HOSPITAL_HEIGHT = 120

# Ambulance route - Multiple possible routes to hospital
ROUTE_POINTS = [
    # Route 1: Direct route from left to hospital
    [(0, MAIN_HORIZONTAL_Y),
     (HOSPITAL_X, MAIN_HORIZONTAL_Y)],
    
    # Route 2: Route from left via upper road
    [(0, MAIN_HORIZONTAL_Y - 200),
     (MAIN_VERTICAL_X2, MAIN_HORIZONTAL_Y - 200),
     (MAIN_VERTICAL_X2, MAIN_HORIZONTAL_Y),
     (HOSPITAL_X, MAIN_HORIZONTAL_Y)],
    
    # Route 3: Route from bottom via vertical road
    [(MAIN_VERTICAL_X3, WINDOW_HEIGHT),
     (MAIN_VERTICAL_X3, MAIN_HORIZONTAL_Y),
     (HOSPITAL_X, MAIN_HORIZONTAL_Y)]
]

# Vehicle routes - Updated for better traffic flow
CAR_ROUTES = [
    # Horizontal routes
    [(0, MAIN_HORIZONTAL_Y), (WINDOW_WIDTH, MAIN_HORIZONTAL_Y)],
    [(WINDOW_WIDTH, MAIN_HORIZONTAL_Y), (0, MAIN_HORIZONTAL_Y)],
    [(0, MAIN_HORIZONTAL_Y - 200), (WINDOW_WIDTH, MAIN_HORIZONTAL_Y - 200)],
    [(WINDOW_WIDTH, MAIN_HORIZONTAL_Y - 200), (0, MAIN_HORIZONTAL_Y - 200)],
    
    # Vertical routes
    [(MAIN_VERTICAL_X1, 0), (MAIN_VERTICAL_X1, WINDOW_HEIGHT)],
    [(MAIN_VERTICAL_X1, WINDOW_HEIGHT), (MAIN_VERTICAL_X1, 0)],
    [(MAIN_VERTICAL_X2, 0), (MAIN_VERTICAL_X2, WINDOW_HEIGHT)],
    [(MAIN_VERTICAL_X2, WINDOW_HEIGHT), (MAIN_VERTICAL_X2, 0)],
    [(MAIN_VERTICAL_X3, 0), (MAIN_VERTICAL_X3, WINDOW_HEIGHT)],
    [(MAIN_VERTICAL_X3, WINDOW_HEIGHT), (MAIN_VERTICAL_X3, 0)]
]

TRUCK_ROUTES = CAR_ROUTES  # Trucks follow the same routes as cars
BIKE_ROUTES = CAR_ROUTES   # Bikes follow the same routes as cars

# Traffic Light Configuration - Updated for new routes
TRAFFIC_LIGHTS = [
    (MAIN_VERTICAL_X1, MAIN_HORIZONTAL_Y - ROAD_WIDTH//2),
    (MAIN_VERTICAL_X2, MAIN_HORIZONTAL_Y - ROAD_WIDTH//2),
    (MAIN_VERTICAL_X3, MAIN_HORIZONTAL_Y - ROAD_WIDTH//2),
    (MAIN_VERTICAL_X1, MAIN_HORIZONTAL_Y - 200 - ROAD_WIDTH//2),
    (MAIN_VERTICAL_X2, MAIN_HORIZONTAL_Y - 200 - ROAD_WIDTH//2),
    (MAIN_VERTICAL_X3, MAIN_HORIZONTAL_Y - 200 - ROAD_WIDTH//2)
]

# Vehicle rotation settings
ROTATE_VEHICLES = True
VERTICAL_ROTATION = 90

# Base speed and vehicle speeds (as multipliers)
BASE_SPEED = 1  # Reduced base speed
AMBULANCE_SPEED = 0.4  # Slower ambulance
CAR_SPEED = 0.25  # Slower cars
TRUCK_SPEED = 0.2  # Slower trucks
BIKE_SPEED = 0.3  # Slower bikes 