from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2

model = YOLO("/content/best (7).pt") #ruta de acceso del modelo
cap = cv2.VideoCapture("/content/demo2.mp4") #ruta de acceso del video
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS)) #inicializamos coordenadas

# Define region points
region_points = [(0, 1080), (1920, 1080), (1920, 0), (0, 0)] #establecemos las coordenadas de los 4 puntos donde van a ser contadas las personas
#en nuestro caso hemos puesto los putnos en las esquinas del video.

# Video writer
video_writer = cv2.VideoWriter("salida_video.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))

# Init Object Counter
counter = object_counter.ObjectCounter()
counter.set_args(view_img=True,
                 reg_pts=region_points,
                 classes_names=model.names,
                 draw_tracks=True,
                 line_thickness=2)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, show=False)

    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()