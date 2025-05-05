# SystemDesignProject

Project Overview

This project involved programming a LEGO EV3 robot to autonomously follow a white line on a track and handle various challenges, including:

- Navigating breaks in the line
- Adjusting to changes in ambient light
- Handling sharp turns
- Detecting and responding to walls
- Performing a ball-throwing task

The robot uses multiple sensors (light, color, and ultrasonic) and motors, coordinated through multi-threaded Python code, to perceive its environment and react in real-time.
How It Works

Line Following:
  - The robot uses two light sensors (left and right) and a color sensor (middle) to detect the white line. It continuously compares the reflected light intensity from each side to determine if it needs to steer left, right, or continue straight. This is handled in a dedicated motor control thread.

Obstacle and Wall Detection:
  - An ultrasonic sensor monitors the distance to obstacles ahead. When a wall is detected within a certain range, the robot stops, performs a turn, and signals with a beep.

Ball Throwing:
  - Upon reaching a specific location (detected by the ultrasonic sensor), the robot activates a motorized arm to throw a ball, then continues its routine.

Threaded Sensor Reading:
  - Each sensor runs in its own thread, allowing the robot to react quickly to environmental changes without missing sensor updates.
