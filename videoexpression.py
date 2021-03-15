from tkinter import *
import cv2
from PIL import Image, ImageTk
import face_recognition
import numpy as np
import keras
from keras.models import load_model
import datetime
from tkinter import messagebox
import os
from deepface import DeepFace

model1 = False
model2 = True

def faceML():
    img = Image.fromarray(frame1)
    img.save("pe.jpg")

    if model1:
        emotion_dict= {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3}
        face_image  = cv2.imread("pe.jpg")
        face_image = cv2.resize(face_image, (48,48))
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_image = np.reshape(face_image, [1, face_image.shape[0], face_image.shape[1], 1])

        model = load_model("model_v6_23.hdf5")
        predicted_class = np.argmax(model.predict(face_image))
        label_map = dict((v,k) for k,v in emotion_dict.items())
        predicted_label = label_map[predicted_class]
        messagebox.showinfo("Your Emotion FACERECOG_LIB", "Your current emotion is (Predicted off of pre-trained model from https://github.com/priya-dwivedi/face_and_emotion_detection/tree/master/emotion_detector_models): \n" + predicted_label)
    elif model2:
        face_image2 = cv2.imread("pe.jpg")
        face_image2 = cv2.cvtColor(face_image2, cv2.COLOR_BGR2RGB)
        predictionsD = DeepFace.analyze(face_image2)
        predictions = "Emotion: " + predictionsD["dominant_emotion"] +"\n"+"Age: " + str(predictionsD["age"]) +"\n" + "Gender: " + predictionsD["gender"] + "\n" + "Race: " +predictionsD["dominant_race"] + "\n"

        messagebox.showinfo("Your Emotion FACERECOG_DEEPFACE", "Your current emotion is (Predicted off of the pre-trained DeepFace library): \n" + predictions)


    os.remove('pe.jpg')


root = Tk()

root.title('Video Emotion')

root.geometry('400x400')

root.wm_attributes("-topmost", 1)

root.overrideredirect(True)

cam = cv2.VideoCapture(0)

vid = LabelFrame(root, height=400, width = 400)
vid.place(x=0, y=0)

video = Label(vid)
video.pack()

emotion = Button(root, text='Facial Check')
emotion.config(bg='white', borderwidth = 0, command=faceML)
emotion.pack(side=BOTTOM)

Lay = True

while Lay:
    frame = cam.read()[1]
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = ImageTk.PhotoImage(Image.fromarray(frame1))
    video['image'] = frame

    root.update()
