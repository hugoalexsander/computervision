import cv2 as cv
import controller as ct
import os

cap = cv.VideoCapture(0) # Inicia a captura de vídeo da câmera padrão.
if not cap.isOpened():
    print("Cannot open camera")
    exit()
exec = ct.Controller(cap)
exec.config_update()
last_mod_time = os.path.getmtime("config.ini")
while True:
    current_mod_time = os.path.getmtime("config.ini")
    if current_mod_time != last_mod_time:
        last_mod_time = current_mod_time
        exec.config_update()
    exec.render()
    key = cv.waitKey(1)
    if key == ord('q'):
        break
cap.release() # Libera a captura de vídeo.
cv.destroyAllWindows() # Fecha todas as janelas abertas pelo OpenCV.
