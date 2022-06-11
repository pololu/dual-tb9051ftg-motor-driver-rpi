# Python library for the Pololu Single TB9051FTG Motor Driver for Raspberry Pi

Version: 1.0.0<br>
Release Date: 2022-06-11<br>
[www.pololu.com](https://www.pololu.com/)

## Summary

This library runs on the [Raspberry Pi](https://www.pololu.com/product/2759)
(Model B+ or newer) and provides functions for controlling both channels of the
[Pololu Single TB9051FTG Motor Driver for Raspberry Pi](https://www.pololu.com/product/2997).
This library supports both Python 2 and Python 3.

## Getting Started

### Installation

This library depends on [pigpio](http://abyz.me.uk/rpi/pigpio/), and the
instructions below explain how to set it up.

These instructions assume you are using Raspbian, Debian, or some other
distribution that provides the `apt` command for managing packages. If you do
not have `apt`, you will need to use a different method to install the required
packages.

These instructions also assume you will use Python 2.  If you want to use
Python 3, you will need to:
* install the `python3-pigpio` package instead of `python-pigpio`
  (it is okay to install both)
* use the `python3` command instead of `python` for running Python scripts

First, to download and install pigpio and its Python module, run:

```
sudo apt install python-pigpio
```

Then, to start the `pigpiod` daemon, run:

```
sudo systemctl start pigpiod
```

Optionally, to automatically start the daemon every time your Raspberry Pi
boots, you can also run:

```
sudo systemctl enable pigpiod
```

Finally, to download and install the single_tb9051ftg_rpi library, run:

```
git clone https://github.com/Penumbrage/single-tb9051ftg-motor-driver-rpi.git
cd single-tb9051ftg-motor-driver-rpi
sudo python setup.py install
```

### Running the example program

This library comes with an example program that drives a single motor in both
directions.  To run the example, navigate to the
single-tb9051ftg-motor-driver-rpi directory and run:

```
python example.py
```

## Library reference

This library uses ultrasonic 20&nbsp;kHz PWM to drive the motors.

Motor speeds in this library are represented as numbers between **-480** and
**480** (inclusive).  A speed of 0 corresponds to braking.  Positive speeds
correspond to current flowing from M1A to M1B, while negative speeds
correspond to current flowing in the other direction.

The library can be imported into a Python program with the following line:

```
from single_tb9051ftg_rpi import motors, MAX_SPEED
```

After importing the library, you can use the functions below to enable the motors
and set motor speeds:

* `motors.enable()`: Enable the motor driver.
* `motors.motor1.enable()`: Enable motor driver 1.
* `motors.motor2.enable()`: [NOT AVAILABLE] Enable motor driver 2.
* `motors.disable()`: Disable the motor driver.
* `motors.motor1.disable()`: Disable motor driver 1.
* `motors.motor2.disable()`: [NOT AVAILABLE] Disable motor driver 2.
* `motors.setSpeeds(m1_speed)`: Set speed and direction for motor 1.
* `motors.motor1.setSpeed(speed)`: Set speed and direction for motor 1.
* `motors.motor2.setSpeed(speed)`: [NOT AVAILABLE] Set speed and direction for motor 2.
* `motors.getFaults()`: Returns `True` if there is a fault on the motor
  driver, `False` if no fault.
* `motors.motor1.getFault()`: Returns `True` if there is a fault on motor driver
  1, `False` if no fault.
* `motors.motor2.getFault()`: [NOT AVAILABLE] Returns `True` if there is a fault on motor driver
  2, `False` if no fault.

For convenience, a constant called `MAX_SPEED` (which is equal to 480) is
available on all the objects provided by this library.  You can access it
directly by just writing `MAX_SPEED` if you imported it as shown above, or it
can be accessed in the following ways:

* `motors.MAX_SPEED`
* `motors.motor1.MAX_SPEED`
* `motors.motor2.MAX_SPEED`: [NOT AVAILABLE]

If you are controlling multiple motor drivers, you might prefer to import the
library using `import single_tb9051ftg_rpi`, which requires the commands listed
above to be prefixed with `single_tb9051ftg_rpi.`.

## Version history

* 1.0.0 (2022-06-22): Original release.
