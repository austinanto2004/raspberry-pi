import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import urllib.request

# -----------------------------
# 1️⃣ Emotion model
# -----------------------------
MODEL_PATH = "emotion_model.h5"
if not os.path.exists(MODEL_PATH):
    print("[INFO] Downloading emotion model...")
    url = "https://github.com/oarriaga/face_classification/raw/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5"
    urllib.request.urlretrieve(url, MODEL_PATH)
    print("[INFO] Emotion model downloaded.")

model = load_model(MODEL_PATH, compile=False)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# -----------------------------
# 2️⃣ Face detector (Haar)
# -----------------------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# -----------------------------
# 3️⃣ Age & Gender models
# -----------------------------
os.makedirs("models", exist_ok=True)
AGE_PROTO = "models/age_deploy.prototxt"
AGE_MODEL = "models/age_net.caffemodel"
GENDER_PROTO = "models/gender_deploy.prototxt"
GENDER_MODEL = "models/gender_net.caffemodel"

age_net = cv2.dnn.readNetFromCaffe(AGE_PROTO, AGE_MODEL)
gender_net = cv2.dnn.readNetFromCaffe(GENDER_PROTO, GENDER_MODEL)

AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']

# -----------------------------
# helper: draw info (4 lines)
# -----------------------------
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1  # reduced thickness
LINE_SPACING = 15

def draw_person_info(img, x, y, w, h, name, emotion, age, gender):
    top_line_y = y - 50
    if top_line_y < 0:
        top_line_y = y + h + 5

    cv2.putText(img, f"Name: {name}", (x, top_line_y), FONT, FONT_SCALE, (255,0,0), THICKNESS)
    cv2.putText(img, f"Emotion: {emotion}", (x, top_line_y + LINE_SPACING), FONT, FONT_SCALE, (0,255,255), THICKNESS)  # yellow
    cv2.putText(img, f"Age: {age}", (x, top_line_y + 2*LINE_SPACING), FONT, FONT_SCALE, (0,0,255), THICKNESS)
    cv2.putText(img, f"Gender: {gender}", (x, top_line_y + 3*LINE_SPACING), FONT, FONT_SCALE, (255,255,0), THICKNESS)

# -----------------------------
# 4️⃣ Webcam
# -----------------------------
cap = cv2.VideoCapture(0)
print("[INFO] Press 'q' to quit.")

# Fake top-right overlay
tr_x, tr_y = 470, 20
tr_w, tr_h = 100, 100
fake_name = "a̵̛̝͎͗̏́̑r̷̛͉̀̿̈́d̶̛̄̏̚͘h̶̛̛͆̏̅̕c̶̒͛̌ͮǐ̶́̊̍̚h̶̞̟́́̃b̴́͋̔́͛̊͐̅"
fake_emotion = "Angry"
fake_age = "(1283)"
fake_gender = "Unknown"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(48,48))

    # Real faces
    for i, (x, y, w, h) in enumerate(faces, start=1):
        roi_gray = cv2.resize(gray[y:y+h, x:x+w], (64,64))
        roi = roi_gray.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = model.predict(roi, verbose=0)[0]
        emotion = emotion_labels[np.argmax(preds)]

        face_img = frame[y:y+h, x:x+w].copy()
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227,227),
                                     (78.4263377603, 87.7689143744, 114.895847746),
                                     swapRB=False)
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = AGE_LIST[age_preds[0].argmax()]
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        gender = GENDER_LIST[gender_preds[0].argmax()]

        if i == 1:
            name = "Sreeram"
        elif i == 2:
            name = "Akash"
        else:
            name = f"Face {i}"

        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        draw_person_info(frame, x, y, w, h, name, emotion, age, gender)

    # Fake small face box
    cv2.rectangle(frame, (tr_x, tr_y), (tr_x+tr_w, tr_y+tr_h), (0,255,0), 2)
    draw_person_info(frame, tr_x, tr_y, tr_w, tr_h, fake_name, fake_emotion, fake_age, fake_gender)

    cv2.imshow("Emotion + Age + Gender", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()