# Learnora
Learnora is a smart learning assistant that uses real-time emotion recognition and AI-powered chatbot responses to enhance virtual education. Built with Flask, DeepFace, OpenVINO, and integrated with a local LLM (Phi-3 via Ollama), it offers personalized help to students based on their facial expressions and emotional state.

## 🎯 Problem Statement

Many students hesitate to raise doubts during virtual learning. Traditional learning tools lack emotional awareness, making it difficult to identify disengaged or confused learners. Learnora solves this by:

- **Detecting emotion** through facial expressions.
- **Prompting timely assistance** during confusion.
- **Allowing both voice and text-based interaction** with an LLM chatbot.

---

## ✨ Features

- 🎥 Real-time emotion recognition via webcam.
- 🤖 Chatbot assistance powered by **Phi-3** via **Ollama**.
- 🔊 Text-to-speech (TTS) using **gTTS** for voice responses.
- 🧠 Emotion classification using **DeepFace** and **OpenVINO face detection**.
- 🌐 Web-based UI with **Flask + HTML/CSS/JS**.
- ✅ Confusion state triggers a "Do you need help?" prompt.
- 🎤 Speech-to-text input using **Web Speech API**.

---

## 🧠 Technologies Used

| Category              | Tool/Library                        | Description                                                                 |
|-----------------------|-------------------------------------|-----------------------------------------------------------------------------|
| Frontend              | HTML, CSS, JavaScript               | User interface, camera access, interaction buttons                         |
| Backend               | Flask                               | Python web framework for routing and APIs                                  |
| Emotion Recognition   | DeepFace                            | Emotion classification (FER-2013, AffectNet)                               |
|                      | OpenVINO                            | Real-time face detection acceleration                                      |
| Text-to-Speech (TTS)  | gTTS                                 | Converts chatbot responses to speech (MP3)                                 |
| Chatbot               | Ollama + Phi-3                      | Lightweight LLM running locally via Ollama                                |
| Speech Input          | Web Speech API                      | Captures user voice input in browser                                       |
| Image Processing      | OpenCV                              | Captures webcam frames                                                     |
| API Communication     | Requests                            | Sends/receives data between client, server, and LLM                        |

---

## 🧰 Project Structure

learnora/

│

├── app.py # Flask backend

├── requirements.txt # Project dependencies
│

├── templates/

│ ├── index.html # Home page

│ ├── detect.html # Emotion detection view

│ └── chatbot.html # Chatbot interface
│

├── static/

│ ├── css/

│ │ └── style.css # Custom styling

│ ├── js/

│ │ └── script.js # Webcam, speech, emotion logic

│ ├── gif/

│ │ └── background.gif # Animated background

│ └── audio/

│ └── *.mp3 # TTS-generated audio files



---

## 🧪 Emotion Detection Pipeline

1. Capture webcam frame every 5 seconds via `script.js`.
2. Send frame to Flask `/api/emotion`.
3. Use OpenVINO `face-detection-adas-0001` to extract face.
4. Classify emotion using **DeepFace**.
5. If emotion ∈ `['neutral', 'sad', 'fear']` → **confused state**.
6. Prompt user with **Yes/No** → "Do you need help?"

---

## 🧠 LLM Integration via Ollama

- Queries sent to [Ollama](https://ollama.com/) server running locally.
- Uses **Phi-3**, a compact transformer-based model fine-tuned for question answering.
- Endpoint: `http://localhost:11434/api/generate`.

---

## 🔊 Text-to-Speech Pipeline

- When chatbot responds, Flask uses **gTTS** to convert the message into `.mp3`.
- This audio file is returned and played in-browser using JavaScript.

---

## ⚙️ Installation Instructions

### 1. Clone Repository

git clone https://github.com/shaliniilango/learnora.git

cd learnora

2. Create Virtual Environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install Dependencies

pip install -r requirements.txt

5. Download OpenVINO Model (Optional Step if Needed)

cd open_model_zoo/tools/model_tools

python downloader.py --name face-detection-adas-0001

6. Start Ollama with Phi-3

ollama run phi3

7. Run Flask Server

python app.py

🧪 Sample Workflow

User visits http://127.0.0.1:5000/

Clicks Start

Emotion is continuously analyzed.

If confused → prompted for help (Yes/No).

If Yes → Chatbot opens

User speaks/types question → Answer shown and spoken.

📊 Result Metrics

Component	Metric	Value / Comment

Emotion Detection	Accuracy	~85–90% (DeepFace + OpenVINO)

Face Detection Speed	Inference Time	~5–10 ms per frame using OpenVINO

LLM Response Time	Response Time (Phi-3)	~1–3 seconds (depending on hardware)

TTS Generation	Audio File Size	~10–50 KB / prompt


🔚 Conclusion

Learnora combines emotion AI and generative AI to make virtual learning more responsive and empathetic. By proactively assisting students when they’re confused, it replicates the experience of an attentive human tutor, making education more inclusive, intelligent, and impactful.


📄 License

MIT License – feel free to use, share, and contribute!

🙋‍♀️ Author

Shalini I

Final Year – B.Tech CSE

Passionate about AI, Education, and Human-Computer Interaction
