import cv2

def Capture(frame):
    cv2.imshow('Webcam View', frame)
    cv2.waitKey(0)  # Wait for Enter key press
    cv2.imwrite('captured_image.jpg', frame)
    print("Image saved as 'captured_image.jpg'")
    return 'captured_image.jpg'