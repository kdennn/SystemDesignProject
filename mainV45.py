#!/usr/bin/env python3
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, Motor
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from threading import Thread, Event
from ev3dev2.sound import Sound

# Initialize motors and light sensors
two_tires = MoveTank(OUTPUT_A, OUTPUT_B)
ballarm = Motor(OUTPUT_C)
leftSen = LightSensor(INPUT_1)
rightSen = LightSensor(INPUT_2)
midSen = ColorSensor(INPUT_3)
UsonicSen = UltrasonicSensor(INPUT_4)

threshholdbase = 15

# Light intesity Variables
leftSen_Inten = 0
rightSen_Inten = 0
middleSen_Inten = 0
Usonic_Inten = 100  # for milestone this was in comment

# Histroy tracker of middle sensor
middleSenLIST = []

# action bools
turned_around = False
ballpickup = False
balldropoff = False
blockdrop = False
stop_motor_thread = True

# run_bitch = True


# black = 0 - 30
# mid = 30 - 70
# white = 70 - 100

# Read Sonsors
def read_ultrasonic_sensor():
    global Usonic_Inten
    while True:
        Usonic_Inten = UsonicSen.distance_centimeters
        time.sleep(0.01)


def read_left_sensor():
    global leftSen_Inten
    while True:
        leftSen_Inten = leftSen.reflected_light_intensity
        time.sleep(0.01)  # sleepy time


def read_right_sensor():
    global rightSen_Inten
    while True:
        rightSen_Inten = rightSen.reflected_light_intensity
        time.sleep(0.01)  # sleepy time


def light_difference(left, right):
    differenz = left - right
    if differenz > threshholdbase or differenz < -threshholdbase:
        if left > right:
            return 1
        else:
            return -1
    else:
        return 0


resume_motor_event = Event()


def moter_sensor_thread():
    global leftSen_Inten
    global rightSen_Inten
    global resume_motor_event
    global stop_motor_thread

    sound = Sound()

    speed = 35
    turnspeed = 40

    sound.beep()

    while True:
        # resume_motor_event.wait()
        
        direction = light_difference(leftSen_Inten, rightSen_Inten)
        # motor control logic based on the direction
        if direction == 1:
            two_tires.on(SpeedPercent(turnspeed), SpeedPercent(-15))
        elif direction == -1:
            two_tires.on(SpeedPercent(-15), SpeedPercent(turnspeed))
        else:
            two_tires.on(SpeedPercent(speed), SpeedPercent(speed))
        time.sleep(0.01)  # sleepy time


def walldistance():
    global Usonic_Inten
    global turned_around
    global ballpickup
    global balldropoff
    global resume_motor_event

    sound = Sound()

    # Turn around function
    while not turned_around and not ballpickup and not balldropoff:
        if Usonic_Inten < 8:
            resume_motor_event.clear()
            time.sleep(0.5)
            backturn()
            time.sleep(3)
            sound.beep()
            turned_around = True
            resume_motor_event.set()
        else:
            # If the condition is not satisfied, pause the motor control thread
            # Optionally, you can add logic to handle the case when the condition is not satisfied
            # ...
            # Resume the motor control thread when needed
            resume_motor_event.set()

    while turned_around and not ballpickup and not balldropoff:
        if Usonic_Inten < 8:
            # detection of the SCHRANKE! now you see, you wait go beep
            resume_motor_event.clear()
            time.sleep(0.5)
            sound.tone(200, 300)
            ballpickup = True
            resume_motor_event.set()
        else:
            resume_motor_event.set()

    while turned_around and ballpickup and not balldropoff:
        # detection of Box to drop your big balls in booty
        if Usonic_Inten < 8:
            resume_motor_event.clear()
            ballthrow()
            balldropoff = True
            sound.beep()
            sound.beep()
            time.sleep(5)
            resume_motor_event.set()
        else:
            resume_motor_event.set()


# Start Wall distance thing
# wall_detection_event = Event()

# Threads begin
left_sensor_thread = Thread(target=read_left_sensor)
right_sensor_thread = Thread(target=read_right_sensor)
Ultrasonic_sensor_thread = Thread(target=read_ultrasonic_sensor)
motor_control_thread = Thread(target=moter_sensor_thread)

walldetection_thread = Thread(target=walldistance)

# Start Threads
left_sensor_thread.start()
right_sensor_thread.start()
Ultrasonic_sensor_thread.start()
motor_control_thread.start()

walldetection_thread.start()


# function to turn around
def backturn():
    two_tires.on_for_rotations(SpeedPercent(20), SpeedPercent(-20), rotations=1.30)


def ballthrow():
    two_tires.on_for_rotations(SpeedPercent(20), SpeedPercent(-20), rotations=0.75)
    two_tires.on_for_rotations(SpeedPercent(-5), SpeedPercent(-5), rotations=0.25)



# Turn when it detects the wall
# walldetection()



# stop_motor_control_event = Event()
# def stop_motor_control_thread():
#     stop_motor_control_event.set()

# ball_action_thread = Thread(target=ballaction)




# Start Threads
# left_sensor_thread.start()
# right_sensor_thread.start()
# Ultrasonic_sensor_thread.start()
# motor_control_thread.start()
# ball_action_thread.start()


# stop stuff




# To stop the threads when needed?
# left_sensor_thread.join()
# right_sensor_thread.join()
# motor_control_thread.join()
