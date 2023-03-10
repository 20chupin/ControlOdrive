"""Calibration without load"""

from motor import *

# Initialisation
motor = OdriveEncoderHall(enable_watchdog=False)
motor.erase_configuration()
motor.configuration()
motor.save_configuration()
motor.calibration(mechanical_load=False)
motor.stop()
