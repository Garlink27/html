import tkinter as tk
import speech_recognition as sr
from threading import Thread

class RealTimeSubtitles:
    def __init__(self, root):
        self.root = root
        self.root.title("ISHA")

        self.label = tk.Label(root, text="Hable ahora...", font=("Helvetica", 16))
        self.label.pack(pady=5)

        self.text = tk.Text(root, height=5, width=50, font=("Helvetica", 20), wrap=tk.WORD)
        self.text.pack(pady=40)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.keep_listening = True
        self.listen_thread = Thread(target=self.recognize_speech)
        self.listen_thread.start()

        self.transcribed_text = []

        self.root.bind('<p>', self.stop_and_save)

    def recognize_speech(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.keep_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=4)
                    Thread(target=self.process_audio, args=(audio,)).start()
                except sr.WaitTimeoutError:
                    continue

    def process_audio(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language='es-ES')
            self.update_text(text)
            self.transcribed_text.append(text)
        except sr.UnknownValueError:
            self.update_text("No se pudo entender el audio")
        except sr.RequestError as e:
            self.update_text(f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}")

    def update_text(self, text):
        lines = self.split_text(text, 40)
        for line in lines:
            self.text.insert(tk.END, line + "\n")
            self.text.see(tk.END)

    def split_text(self, text, length):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > length:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " "
                current_line += word

        if current_line:
            lines.append(current_line)

        return lines

    def stop_and_save(self, event):
        self.keep_listening = False
        self.listen_thread.join()

        with open("subtitulos.txt", "w", encoding="utf-8") as file:
            for line in self.transcribed_text:
                lines = self.split_text(line, 40)
                for line in lines:
                    file.write(line + "\n")

        self.root.destroy()

    def on_closing(self):
        self.keep_listening = False
        self.listen_thread.join()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeSubtitles(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
