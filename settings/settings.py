
class Values:

    PRINT_FPS = True

    CAMERA = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 360

    SHOOT_PIN = 21

    """MODES!!!!"""

    WAITING_FOR_TARGET = 0
    FLYING_TO_TARGET = 1
    ELIMINATING = 2

    """TARGET STATE"""
    QUEUED = 0
    ELIMINATED = 1
    NOT_ELIMINATED = 2


class PIDSettings:
    PID_PPM_UPDATE_TIME = 0.03

    PID_I_MAX = 30
    """wszystkie wartości od 0 do 1"""

    ROLL_SETPOINT = 0

    PITCH_SETPOINT = 0

