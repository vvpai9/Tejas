import cv2
import numpy as np

# Load YOLOv4 Tiny
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# Load COCO classes
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getUnconnectedOutLayersNames()
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(layer_names)
        h, w = frame.shape[:2]
        center_x = 320

        person_detected = False
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if classes[class_id] == "person" and scores[class_id] > 0.5:
                    box = detection[0:4] * np.array([w, h, w, h])
                    x, y, bw, bh = box.astype("int")
                    center_x = x
                    person_detected = True
                    cv2.rectangle(frame, (x - bw//2, y - bh//2), (x + bw//2, y + bh//2), (0, 255, 0), 2)
                    break

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()