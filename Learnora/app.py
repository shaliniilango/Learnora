from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
from gtts import gTTS
from openvino.runtime import Core
import os
import uuid
import requests
import cv2
import numpy as np

app = Flask(__name__)

# --- Configs ---
CONFUSION_EMOTIONS = ['neutral', 'sad', 'fear']
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"
OPENVINO_MODEL_PATH = r"C:\Users\ilang\OneDrive\Desktop\emotico\models\face-detection-adas-0001.xml"

# Ensure audio folder exists
os.makedirs("static/audio", exist_ok=True)

# --- Load OpenVINO Face Detection Model ---
core = Core()
model = core.read_model(OPENVINO_MODEL_PATH)
compiled_model = core.compile_model(model, "CPU")
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

def detect_face_openvino(image_path):
    frame = cv2.imread(image_path)
    ih, iw = frame.shape[:2]
    resized = cv2.resize(frame, (672, 384))
    input_image = resized.transpose((2, 0, 1))
    input_image = np.expand_dims(input_image, axis=0)

    result = compiled_model([input_image])[output_layer]

    for detection in result[0][0]:
        conf = detection[2]
        if conf > 0.5:
            x_min = int(detection[3] * iw)
            y_min = int(detection[4] * ih)
            x_max = int(detection[5] * iw)
            y_max = int(detection[6] * ih)
            face = frame[y_min:y_max, x_min:x_max]
            return face
    return None

# --- Routes ---
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/detect')
def detect():
    return render_template("detect.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat_page():
    if request.method == 'POST':
        question = request.form.get('question', '')
        try:
            response = requests.post(OLLAMA_API_URL, json={
                "model": MODEL_NAME,
                "prompt": question,
                "stream": False
            })
            response.raise_for_status()
            reply = response.json().get("response", "No response.")
        except Exception as e:
            reply = f"Error: {str(e)}"
        return render_template("chatbot.html", question=question, answer=reply)
    return render_template("chatbot.html")

@app.route('/api/emotion', methods=['POST'])
def detect_emotion():
    try:
        file = request.files['frame']
        img_path = f"temp_{uuid.uuid4()}.jpg"
        file.save(img_path)

        face_img = detect_face_openvino(img_path)
        if face_img is not None:
            cv2.imwrite(img_path, face_img)

        result = DeepFace.analyze(img_path, actions=['emotion'], enforce_detection=False)
        os.remove(img_path)

        dominant_emotion = result[0]['dominant_emotion']
        is_confused = dominant_emotion.lower() in CONFUSION_EMOTIONS

        return jsonify({
            "emotion": dominant_emotion,
            "confused": is_confused
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        qn = request.json.get("question", "")
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODEL_NAME,
            "prompt": qn,
            "stream": False
        })
        response.raise_for_status()
        reply = response.json().get("response", "No response.")
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

@app.route('/api/speak', methods=['POST'])
def speak():
    try:
        text = request.json.get("text", "")
        filename = f"static/audio/{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        return jsonify({"audio_url": "/" + filename})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
