import wpilib
import wpilib.drive
import math
from wpimath.controller import SimpleMotorFeedforwardMeters

# important constants calculated previously
class Constants():
    def __init__(self):
        self.kS = 0
        self.kV = 2.38
        self.kA = 0.52
        self.THEORETICAL_TOP_SPEED = 5.2 #m/s
        self.TOP_SPEED = 5.04 #m/s
        self.WHEELBASE = 0.619125 #meters

const = Constants()

# whole system for auto and teleop
class DriveTrain():
    def __init__(self):
        # define variables
        self.leftMotor = wpilib.VictorSP(0)
        self.rightMotor = wpilib.VictorSP(1)

        self.robotDrive = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)

        self.feedForward = SimpleMotorFeedforwardMeters(const.kS, const.kV, const.kA)

        self.timer = wpilib.Timer()

        self.rightMotor.setInverted(False)
        self.leftMotor.setInverted(True)
        
        self.robotDrive.setSafetyEnabled(False)
        self.robotDrive.setMaxOutput(0.7)
    
    def driveMotors(self, leftVelocity: float, rightVelocity: float, time):
        # drive motors for a given time and speed

        self.timer.restart()

        while self.timer.get() <= time:
            self.leftMotor.setVoltage(self.feedForward.calculate(leftVelocity))
            self.rightMotor.setVoltage(self.feedForward.calculate(rightVelocity))

        # motor safety
        self.leftMotor.stopMotor
        self.rightMotor.stopMotor
    
    def driveForward(self, distance: float, speed=const.TOP_SPEED):
        # drive off distance and speed

        self.driveTime = distance / speed
        self.leftSpeed = speed
        self.rightSpeed = speed
        self.timer.reset()

        self.driveMotors(self.leftSpeed, self.rightSpeed, self.driveTime)

    def turnOnSelf(self, angle, speed=const.TOP_SPEED):
        # drive off angle and speed

        self.distance = 4.9 * math.pi * const.WHEELBASE * (angle / 360)
        self.driveTime = self.distance / speed

        # make it turn instead of go straight
        self.leftSpeed = speed
        self.rightSpeed = -1 * speed

        self.driveMotors(self.leftSpeed, self.rightSpeed, self.driveTime)