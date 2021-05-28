import time
from settings.settings import Values


class RosTopicSubscriber:

    def __init__(self, pids):
        self.start_shooting_time = time.time()
        self.unsteady_time = time.time()
        self.pids = pids
        self.current_mode = Values.WAITING_FOR_TARGET

        #subuj topic


    def flyToTarget(self, latitude, longitude, altitude):
        self.current_mode = Values.FLYING_TO_TARGET


    def onMessageReceived(self):
        pass
        #if msg == start shooting:
            #self.start_shooting = True
            #self.start_shooting_time = time.time()
            #self.current_mode = Values.ELININATING


    def sendServoPosition(self, pitch, roll):
        pass
        #print(pitch, roll)
        #sendRollROS(roll)
        #sendPitchROS(pitch)
