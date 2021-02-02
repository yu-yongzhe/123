import threading
import time
import djitellopy
import cv2

#线程一，完成自动航行任务
class mythread1(threading.Thread):
    def run(self):
        drone.takeoff()
        time.sleep(3)
        drone.move_up(100)
       # time.sleep(3)
       #  drone.move_left(100)
       #  time.sleep(3)
       #  drone.move_forward(100)



# 线程二，完成人脸捕捉部分
class mythread2(threading.Thread):
    def run(self):
        drone.streamon()
        try:
            cap = drone.get_video_capture()
            while 1:
                ret, frame = cap.read()
                faces = face_cascad.detectMultiScale(frame, 1.3, 10)
                img = frame
                for (x, y, w, h) in faces:
                    img = cv2.rectangle(img, (x, y), (x + w, x + h), (255, 0, 0), 2)
                    # face_area = img[y:y+h, x:x+w]

                    # eyes = eye_cascade.detectMultiScale(face_area)
                    # for(ex,ey,ew,eh) in eyes:
                    #     cv2.rectangle(face_area,(ex,ew),(ex+ew, ey+eh),(0,255,0),1)
                    # drone.flip_forward()
                    if x != 0:
                        drone.flip_forward()
                
                cv2.imshow("frame", img)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
        except Exception as ex:
            print(ex)
        finally:
            # drone.quit()
            pass

if __name__ == '__main__':
    def handler(event, sender, data, **args):
        drone = sender
        if event is drone.EVENT_FLIGHT_DATA:
            print(data)
    face_cascad = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    drone = djitellopy.Tello()
    time.sleep(2)
    drone.connect()
    time.sleep(2)

    threadl = []
    t1 = mythread1()
    t2 = mythread2()
    threadl.append(t1)
    threadl.append(t2)
    t1.start()
    time.sleep(2)
    t2.start()
    print('Ending now %s' % time.ctime())
