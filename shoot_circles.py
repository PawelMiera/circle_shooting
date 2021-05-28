import traceback
import cv2
from camera.camera import *
from settings.settings import Values
from rosTopicSubscriber.rosTopicSubscriber import RosTopicSubscriber
from firebase.firebase import FirebaseConnection
from PIDs.PIDs import PIDs
import time
import numpy as np


if __name__ == '__main__':

    pids = PIDs()
    ros = RosTopicSubscriber(pids)
    firebase = FirebaseConnection()
    camera = BasicCamera2()

    firebase.update_target(0, Values.ELIMINATED)

    if Values.PRINT_FPS:
        last_time = time.time()
        ind = 0

    current_target = None

    #ros.current_mode = Values.ELIMINATING
    #pids.update_pids = True               ###te 3  do wywalenia tylko zeby ciagle dzialalo do testow
    #ros.start_shooting_time = time.time()

    while True:
        try:

            if ros.current_mode == Values.ELIMINATING:

                frame = camera.get_frame()
                #frame = cv2.imread("0.png")
                if frame is None:
                    continue

                #frame = cv2.resize(frame, (Values.CAMERA_WIDTH, Values.CAMERA_HEIGHT))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.medianBlur(gray, 5)

                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200,
                                           param1=80, param2=50, minRadius=50, maxRadius=150)

                mid = None

                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for c in circles[0, :]:
                        cv2.circle(frame, (c[0], c[1]), c[2], (0, 0, 255), 3)

                    mid = circles[0, 0, :2]

                    pids.update(mid)
                else:
                    pids.update(None)

                ros.sendServoPosition(int(pids.pitchPID.output_pwm), int(pids.rollPID.output_pwm))

                cv2.imshow("circles", frame)        #mozna zakomentowac kiedys

                if mid is not None and pids.rollPID.value is not None and pids.pitchPID.value is not None:

                    if not (abs(pids.pitchPID.value) < 0.1 and abs(pids.rollPID.value) < 0.1):
                        ros.unsteady_time = time.time()

                else:
                    ros.unsteady_time = time.time()

                if time.time() - ros.unsteady_time > 2:
                    print("Shooting!")
                    # send firebase target executed
                    ros.current_mode = Values.WAITING_FOR_TARGET
                    pids.update_pids = False
                    ros.sendServoPosition(0, 0)
                    firebase.update_target(current_target, Values.ELIMINATED)
                    cv2.destroyAllWindows()

                if time.time() - ros.start_shooting_time > 20:
                    print("Timeout!")
                    pids.update_pids = False
                    ros.current_mode = Values.WAITING_FOR_TARGET
                    ros.sendServoPosition(0, 0)
                    firebase.update_target(current_target, Values.NOT_ELIMINATED)
                    cv2.destroyAllWindows()

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if Values.PRINT_FPS:
                    ind += 1
                    if time.time() - last_time > 1:
                        print("FPS:", ind)
                        ind = 0
                        last_time = time.time()

            elif ros.current_mode == Values.WAITING_FOR_TARGET:

                for index, target in enumerate(firebase.all_targets):
                    if int(target['eliminated']) == Values.QUEUED:
                        ros.flyToTarget(float(target['latitude']), float(target['longitude']), 6)
                        current_target = index

                time.sleep(1)

        except Exception:
            print("Some error accrued: ")
            traceback.print_exc()

    pids.stop()
    firebase.close()

    #camera.close()

