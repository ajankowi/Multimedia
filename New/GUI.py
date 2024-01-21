from select import select
import customtkinter
from PIL import ImageTk
from PIL import Image
from datetime import datetime
import cv2
import Camera
import Voice
import Face_Detector
global cam
global frame

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
app = customtkinter.CTk()
app.geometry("1100x530")
app.title("Porównywanie twarzy")

directory_to_search = 'Photos'

def camera_start():
    global cam
    global frame
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        img_update = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_update = ImageTk.PhotoImage(Image.fromarray(img_update))
        camera_image.configure(text="", image=img_update)

        app.update()
        frame_1.update()

def camera_stop():
    global cam
    cam.release()
    cv2.destroyAllWindows()
    camera_image.configure(text="Kamera wyłączona", image="")
    app.update()
    frame_1.update()

def button_take_photo_callback():
    global frame
    camera_photo_path = Camera.Capture(frame)
    Face_Detector.detect_save_face(camera_photo_path, False)

    checkbox_photo.toggle()
    check_checkboxes()
    
def button_take_voice_callback():
    user_input = Voice.recognize_speech()
    transcripted_text.configure(text=user_input)
    user_input = user_input.replace(" ", "")
    comparison_photo_path = Voice.get_photo_speech(user_input, directory_to_search)
    Face_Detector.detect_save_face(comparison_photo_path, True)
    
    checkbox_voice.toggle()
    check_checkboxes()

def button_display_comparison_callback():
    image1 = "best_face_voice.png"
    image2 = "best_face_camera.png"
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    min_height = min(img1.shape[0], img2.shape[0])
    img1 = cv2.resize(img1, (int(img1.shape[1] * min_height / img1.shape[0]), min_height))
    img2 = cv2.resize(img2, (int(img2.shape[1] * min_height / img2.shape[0]), min_height))

    concatenated_img = cv2.hconcat([img1, img2])

    cv2.imshow('Comparison View', concatenated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=0, padx=0, fill="y", expand=False, side="left")

button_1 = customtkinter.CTkButton(master=frame_1, command=camera_start, text="Włącz kamerę")
button_1.pack(pady=30, padx=10)

button_2 = customtkinter.CTkButton(master=frame_1, command=camera_stop,
                                   text="Wyłącz kamerę", fg_color=("white", "gray38"))
button_2.pack(pady=12, padx=10)


def check_checkboxes():
    # Check if both checkboxes are checked
    if checkbox_voice.get() == 1 and checkbox_photo.get() == 1:
        # Enable the button if both checkboxes are checked
        button_display_comparison.configure(state="normal")
    else:
        # Disable the button if any checkbox is not checked
        button_display_comparison.configure(state="disabled")


checkbox_voice = customtkinter.CTkCheckBox(master=frame_1, onvalue=1, offvalue=0, text="Wczytano obraz głosem")
checkbox_voice.pack(pady=12, padx=10, side="bottom")
checkbox_voice.deselect()
checkbox_voice.configure(command=check_checkboxes)

checkbox_photo = customtkinter.CTkCheckBox(master=frame_1, onvalue=1, offvalue=0, text="Zapisano obraz z kamery")
checkbox_photo.pack(pady=12, padx=10, side="bottom")
checkbox_photo.deselect()
checkbox_voice.configure(command=check_checkboxes)

frame_2 = customtkinter.CTkFrame(master=app)
frame_2.pack(pady=0, padx=20, fill="both", expand=True, side="left")

camera_image = customtkinter.CTkLabel(master=frame_2, text="Kamera wyłączona")
camera_image.pack(pady=0, padx=0, side="top", fill="none", expand=True,)


frame_3 = customtkinter.CTkFrame(master=app)
frame_3.pack(pady=0, padx=0, fill="both", expand=False, side="right")

label_1 = customtkinter.CTkLabel(master=frame_3, text="Transkrypcja:")
label_1.pack(pady=12, padx=10, side="top")

transcripted_text = customtkinter.CTkLabel(master=frame_3,
                                           text="",
                                           corner_radius=6,
                                           fg_color=("white", "gray38"),
                                           )
transcripted_text.pack(pady=10, padx=0, side="top", fill="x", expand=False)



button_display_comparison = customtkinter.CTkButton(master=frame_3, command=button_display_comparison_callback, text="Wyświetl porównanie")
button_display_comparison.pack(pady=12, padx=10, side="bottom")
button_display_comparison.configure(state="disabled")

button_delete_txt = customtkinter.CTkButton(master=frame_3, command=button_take_photo_callback, text="Zapisz obraz z kamery")
button_delete_txt.pack(pady=12, padx=10, side="bottom")

button_save_txt = customtkinter.CTkButton(master=frame_3, command=button_take_voice_callback, text="Pobierz próbkę głosu")
button_save_txt.pack(pady=12, padx=10, side="bottom")



app.mainloop()
