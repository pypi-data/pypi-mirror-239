﻿# coding: utf-8

from time import sleep
from .actuator import Actuator
from .._global import OptionalModule

try:
  import serial
except (ModuleNotFoundError, ImportError):
  serial = OptionalModule("pyserial")


class Biaxe(Actuator):
  """This class creates an axis and opens the corresponding serial port."""

  def __init__(self,
               port: str = '/dev/ttyUSB0',
               baudrate: int = 38400,
               timeout: float = 1) -> None:
    """Sets the instance attributes.

    Args:
      port (:obj:`str`, optional): Path to the corresponding serial port, e.g
        `'/dev/ttyS4'`.
      baudrate (:obj:`int`, optional): Set the corresponding baud rate.
      timeout (:obj:`float`, optional): Serial timeout.
    """

    Actuator.__init__(self)
    self.port = port
    self.baudrate = baudrate
    self.timeout = timeout

  def open(self) -> None:
    self.ser = serial.Serial(self.port, self.baudrate,
                             serial.EIGHTBITS, serial.PARITY_EVEN,
                             serial.STOPBITS_ONE, self.timeout)
    self.clear_errors()
    self.speed = None

  def stop(self) -> None:
    self.set_speed(0)

  def close(self) -> None:
    """Close the designated port."""

    self.stop()
    sleep(.01)
    self.ser.close()

  def clear_errors(self) -> None:
    """Reset errors."""

    self.ser.write(b"CLRFAULT\r\n")
    self.ser.write(b"OPMODE 0\r\n EN\r\n")

  def set_speed(self, speed: float) -> None:
    """Re-define the speed of the motor.
    ::

      1 = 0.002 mm/s

    """

    s = int(speed / .002)  # Convert to mm/s
    if s != self.speed:  # If it changed since last time (to avoid spamming)
      self.ser.write(b"J " + str(s).encode('ASCII') + b"\r\n")
      self.speed = s
