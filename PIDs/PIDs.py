from PID.PID import PID
from settings.settings import PIDSettings as ps, Values
from threading import Timer
import csv
import os


class PIDs:
    def __init__(self):
        self._timer = None
        self.dt = ps.PID_PPM_UPDATE_TIME
        self.is_running = False
        self.update_pids = False

        #values = self.get_pid_values()

        self.rollPID = PID(ps.ROLL_SETPOINT, 0, 180, 30, 2, 1)
        self.pitchPID = PID(ps.PITCH_SETPOINT, 0, 180, 30, 2, 1)

        self.start()

    def update(self, mid):

        if mid is not None:
            x = (mid[0] / Values.CAMERA_WIDTH - 0.5) * 2
            y = (0.5 - mid[1] / Values.CAMERA_HEIGHT) * 2

        else:
            x = ps.ROLL_SETPOINT
            y = ps.PITCH_SETPOINT
        self.rollPID.update(x)
        self.pitchPID.update(y)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.dt, self._run)
            self._timer.start()
            self.is_running = True

    def _run(self):
        self.is_running = False
        self.start()
        self.calculate_pids()

    def stop(self):
        print("Closing pids!")
        self._timer.cancel()
        self.is_running = False
        self.update_pids = False


    def calculate_pids(self):
        if self.update_pids:

            self.rollPID.calculate()
            self.pitchPID.calculate()
        else:
            self.rollPID.reset()
            self.pitchPID.reset()

    def get_pid_values(self):
        values = []
        with open(os.path.join("settings", "pidValues.csv"), 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                values.append(row)
        return values

    def update_P_I_D_values(self):
        values = self.get_pid_values()

        self.pitchPID.Kp = float(values[0][0])
        self.pitchPID.Ki = float(values[1][0])
        self.pitchPID.Kd = float(values[2][0])

        self.rollPID.Kp = float(values[0][1])
        self.rollPID.Ki = float(values[1][1])
        self.rollPID.Kd = float(values[2][1])

