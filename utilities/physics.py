import random
import time
import math

#CONSTANTS
GRAVITY = 9.81

def main():
    import time
    import math

def Trajectory(angle, start_velocity, air_time):
    v0_x = math.cos(angle)
    v0_y = math.sin(angle)
    sy = (v0_y * air_time) + (0.5 * GRAVITY * air_time**2)
    sx = v0_x * air_time


if __name__ == '__main__':
    main()
