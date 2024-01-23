import Camera
import Voice
import Face_Detector
import cv2

directory_to_search = 'Photos'


def display_and_save_images(image1, image2):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    # Resize images if needed to have the same height
    min_height = min(img1.shape[0], img2.shape[0])
    img1 = cv2.resize(img1, (int(img1.shape[1] * min_height / img1.shape[0]), min_height))
    img2 = cv2.resize(img2, (int(img2.shape[1] * min_height / img2.shape[0]), min_height))

    # Concatenate images horizontally
    concatenated_img = cv2.hconcat([img1, img2])

    # Display the concatenated image
    cv2.imshow('Comparison View', concatenated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the concatenated image
    cv2.imwrite("Input.jpg", concatenated_img)
    print(f"Concatenated image saved as '{save_path}'")



cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(-1, cv2.CAP_V4L2)
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Webcam View', frame)
    
        # Check for Enter key press
        if cv2.waitKey(1) == 13:
           camera_photo_path = Camera.Capture(frame) # Enter key
           comparison_photo_path = Voice.get_photo_speech(directory_to_search)

           Face_Detector.detect_save_face(camera_photo_path, False)
           Face_Detector.detect_save_face(comparison_photo_path, True)
           display_and_save_images("best_face_voice.png", "best_face_camera.png")


