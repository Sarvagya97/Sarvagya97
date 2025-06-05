import speech_recognition as sr
import pyttsx3
import pocketsphinx
import os
import subprocess
import webbrowser
import datetime
import ctypes
import pyautogui
import cv2

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processcommand(command):
    command = command.lower()

    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("start notepad")

    elif "open command prompt" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "open file explorer" in command:
        speak("Opening File Explorer")
        os.system("explorer")

    elif "lock my computer" in command:
        speak("Locking your computer")
        ctypes.windll.user32.LockWorkStation()

    elif "take screenshot" in command:
        speak("Taking screenshot")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot saved")

    elif "increase volume" in command:
        speak("Increasing volume")
        for _ in range(5):
            pyautogui.press("volumeup")

    elif "decrease volume" in command:
        speak("Decreasing volume")
        for _ in range(5):
            pyautogui.press("volumedown")

    elif "mute" in command:
        speak("Muting volume")
        pyautogui.press("volumemute")

    elif "what can you do" in command:
        speak("I can open apps, search Google, take screenshots, open camera, tell the time, and much more.")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open gmail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")

    elif "what time is it" in command:
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        speak(f"The time is {time}")

    elif "open camera" in command or "start camera" in command:
        speak("Opening your camera...")
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            speak("Camera not available.")
        else:
            speak("Press 's' to take a photo and 'q' to quit the camera.")
            while True:
                ret, frame = cam.read()
                if not ret:
                    speak("Failed to grab frame.")
                    break
                cv2.imshow("Jarvis Camera", frame)

                k = cv2.waitKey(1)
                if k % 256 == ord('s'):
                    img_name = "captured_photo.png"
                    cv2.imwrite(img_name, frame)
                    speak("Photo captured and saved.")
                elif k % 256 == ord('q'):
                    speak("Closing the camera.")
                    break

            cam.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                word = r.recognize_google(audio)

            print(f"You said: {word}")
            if word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("Jarvis active...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=7)
                    command = r.recognize_google(audio)
                    print(f"Command: {command}")
                    processcommand(command)

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            continue
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Error: {e}")