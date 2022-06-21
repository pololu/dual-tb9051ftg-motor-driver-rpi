import pigpio

_pi = pigpio.pi()
if not _pi.connected:
    raise IOError("Can't connect to pigpio")

# Motor speeds for this library are specified as numbers between -MAX_SPEED and
# MAX_SPEED, inclusive.
# This has a value of 480 for historical reasons/to maintain compatibility with
# older libraries for other Pololu boards (which used WiringPi to set up the
# hardware PWM directly).
_max_speed = 480
MAX_SPEED = _max_speed

# TODO: These pins need to be updated based on the pins to be used by the Raspberry Pi Zero 2 W
# NOTE: These are default pins if the pins are not indicated upon instantiation
_pin_M1DIAG = 5
# _pin_M2DIAG = 6
_pin_M1PWM1 = 12
_pin_M1PWM2 = 13
# _pin_M2PWM = 13
_pin_M1EN = 22
_pin_M1ENB = 23
# _pin_M2EN = 23
# _pin_M1DIR = 24
# _pin_M2DIR = 25

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm1_pin = _pin_M1PWM1, pwm2_pin = _pin_M1PWM2, en_pin = _pin_M1EN, enb_pin = _pin_M1ENB, diag_pin = _pin_M1DIAG):
        self.pwm1_pin = pwm1_pin
        self.pwm2_pin = pwm2_pin
        self.en_pin = en_pin
        self.enb_pin = enb_pin
        self.diag_pin = diag_pin

        _pi.set_pull_up_down(diag_pin, pigpio.PUD_UP) # make sure DIAG is pulled up
        
        # enabling the driver requires the en and enb pins to be pulled to their respective values
        _pi.write(en_pin, 1)    # enable driver by default
        _pi.write(enb_pin, 0)   # enable driver by default

    def setSpeed(self, speed):
        # ensure the speed written is within the [-480, 480] default range
        if speed > MAX_SPEED:
            speed = MAX_SPEED
        elif speed < -MAX_SPEED:
            speed = -MAX_SPEED

        # check the direction of the motor using the sign (pos value = forward, neg value = backward)
        if speed < 0:
            # backward
            speed = -speed
            pwm1_value = 0
            pwm2_value = speed
            _pi.write(self.pwm1_pin, pwm1_value)
            _pi.hardware_PWM(self.pwm2_pin, 20000, int(pwm2_value * 6250 / 3))
        else:
            # forward
            pwm1_value = speed
            pwm2_value = 0
            _pi.hardware_PWM(self.pwm1_pin, 20000, int(pwm1_value * 6250 / 3))
            _pi.write(self.pwm2_pin, pwm2_value)

        # _pi.write(self.dir_pin, dir_value)
        # _pi.hardware_PWM(self.pwm_pin, 20000, int(speed * 6250 / 3))
          # 20 kHz PWM, duty cycle in range 0-1000000 as expected by pigpio

    def enable(self):
        _pi.write(self.en_pin, 1)
        _pi.write(self.enb_pin, 0)

    def disable(self):
        _pi.write(self.en_pin, 0)
        _pi.write(self.enb_pin, 1)

    def getFault(self):
        return not _pi.read(self.diag_pin)

class Motors(object):
    # NOTE: normally this class would control both motors, but since this motor driver only has one motor,
    # we will only have functions for one motor

    MAX_SPEED = _max_speed

    def __init__(self, motor1):
        # NOTE: both motors need to be objects of the Motor() class
        self.motor1 = motor1
        # self.motor2 = motor2
        # self.motor1 = Motor(_pin_M1PWM, _pin_M1DIR, _pin_M1EN, _pin_M1DIAG)
        # self.motor2 = Motor(_pin_M2PWM, _pin_M2DIR, _pin_M2EN, _pin_M2DIAG)

    def setSpeeds(self, m1_speed):      # removed m2_speed veriable in function def
        self.motor1.setSpeed(m1_speed)
        # self.motor2.setSpeed(m2_speed)

    def enable(self):
        self.motor1.enable()
        # self.motor2.enable()

    def disable(self):
        self.motor1.disable()
        # self.motor2.disable()

    def getFaults(self):
        return self.motor1.getFault() # or self.motor2.getFault()

    def forceStop(self):
        # reinitialize the pigpio interface in case we interrupted another command
        # (so this method works reliably when called from an exception handler)
        global _pi
        _pi.stop()
        _pi = pigpio.pi()
        self.setSpeeds(0)       # m2_speed has been removed from the setSpeeds function call

# motors = Mo52tors()
