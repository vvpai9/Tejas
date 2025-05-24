import cv2

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
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