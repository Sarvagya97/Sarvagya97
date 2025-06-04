import tkinter as tk
from tkinter import messagebox, simpledialog
import pyaudio
import wave
import os
import datetime

# Your existing recording function with minor tweaks to update GUI status
def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    SECONDS = 5

    if not os.path.exists("recordings"):
        os.makedirs("recordings")

    filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.wav")
    filepath = os.path.join("recordings", filename)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    status_label.config(text="🎙️ Recording... Please wait.")
    root.update()

    frames = []
    for i in range(0, int(RATE / CHUNK * SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    status_label.config(text=f"✅ Saved: {filename}")
    messagebox.showinfo("Success", f"Recording saved as:\n{filename}")

def play():
    recordings = os.listdir("recordings")

    if not recordings:
        messagebox.showwarning("Warning", "No recordings found.")
        return

    # Ask user which file to play
    selected = simpledialog.askinteger("Select Recording", "Enter file number to play:\n" + 
                                       '\n'.join(f"{i+1}. {name}" for i, name in enumerate(recordings)))

    if selected is None:
        return
    index = selected - 1

    if 0 <= index < len(recordings):
        filename = recordings[index]
        filepath = os.path.join("recordings", filename)

        wf = wave.open(filepath, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        status_label.config(text=f"▶️ Playing: {filename}")
        root.update()

        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()
        p.terminate()

        status_label.config(text="Playback finished.")
    else:
        messagebox.showerror("Error", "Invalid selection.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Voice Recorder")
root.geometry("350x200")

record_btn = tk.Button(root, text="Record Audio", command=record)
record_btn.pack(pady=10)

play_btn = tk.Button(root, text="Play Recording", command=play)
play_btn.pack(pady=10)

status_label = tk.Label(root, text="Welcome! Choose an action.", fg="blue")
status_label.pack(pady=10)

root.mainloop()
