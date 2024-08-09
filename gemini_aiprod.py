import cv2
import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr

# Configure the Google Generative AI API
genai.configure(api_key="your key")

# Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

engine = pyttsx3.init()

# Set properties for the speech
engine.setProperty('rate', 180)    # Speed of speech
engine.setProperty('volume', 1)    # Volume level (0.0 to 1.0)

# Check if espeak is available and set properties
if 'espeak' in engine.getProperty('voices')[0].id:
    engine.setProperty('voice', 'en-us')
    engine.setProperty('pitch', 70)  # Set pitch (0-100)

# Function to capture a frame and save it as an image
def capture_frame():
    ret, frame = cap.read()
    if ret:
        image_path = "captured_frame.jpg"
        cv2.imwrite(image_path, frame)
        return image_path
    return None

# Function to upload an image and get the response from the AI model
def identify_object(image_path):
    sample_file = genai.upload_file(path=image_path, display_name="Captured Frame")
    response = model.generate_content([sample_file, "what product is this and where can I buy it"])
    return response.text

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to listen for the keyword and capture a frame
def listen_for_keyword():
    with sr.Microphone() as source:
        print("Listening for the keyword 'product'...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                speech_text = recognizer.recognize_google(audio)
                print("You said: " + speech_text)
                if "product" in speech_text.lower():
                    image_path = capture_frame()
                    if image_path:
                        result = identify_object(image_path)
                        print("Identified Object:", result)
                        sentences = result.split('. ')
                        for sentence in sentences:
                            engine.say(sentence)
                            engine.runAndWait()
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

# Start listening for the keyword
listen_for_keyword()

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
