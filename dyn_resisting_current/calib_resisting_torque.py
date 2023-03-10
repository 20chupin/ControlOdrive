""" Example on how to use the Motor.py code in torque control"""
import numpy as np
import matplotlib.pyplot as plt

from motor import *

# Initialisation
motor = OdriveEncoderHall()
motor.zero_position_calibration()

# Set the control mode
motor.torque_control()

# Variables to plot
t = []
instructions = []
vel_estimate = []
torque_measured = []
positions = []

t0 = time.time()
t1 = time.time()
t_next = 0

l = 0.17
m = 2
g = 9.81
ins = l * m * g
instruction = ins

# motor.set_training_mode("Eccentric")

for i in range(10):
    vel = motor.get_estimated_velocity()
    instruction = ins
    motor.torque_control(instruction)
    while vel == 0.0:
        vel = motor.get_estimated_velocity()
        t1 = time.time()
        if t1 - t0 > t_next:
            t.append(t1 - t0)
            instructions.append(instruction)
            vel_estimate.append(vel)
            torque_measured.append(motor.get_torque_measured())
            positions.append(motor.get_angle())

            t_next += 0.05

    print(torque_measured[-1])
    instruction = 0.0
    motor.torque_control(instruction)

    while vel != 0.0:
        vel = motor.get_estimated_velocity()
        t1 = time.time()
        if t1 - t0 > t_next:
            t.append(t1 - t0)
            instructions.append(instruction)
            vel_estimate.append(vel)
            torque_measured.append(motor.get_torque_measured())
            positions.append(motor.get_angle())

            t_next += 0.05

motor.stop()

vel_estimate = np.asarray(vel_estimate)
positions = np.asarray(positions)

plt.title("Velocity in torque control")
plt.plot(t, vel_estimate, label="Estimated velocity")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()

plt.figure()
plt.title("Torque")
plt.plot(t, instructions, label="Instruction")
plt.plot(t, torque_measured, label="Measured torque")
plt.plot(t, - l * m * g * np.sin(positions / 180 * np.pi), label="'Actual' torque")
plt.xlabel("Time (s)")
plt.ylabel("Torque (Nm)")
plt.legend()

plt.show()