# import cv2
# import pytesseract
# import numpy as np

# pytesseract.pytesseract.tesseract_cmd = "D:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# cap = cv2.VideoCapture("15_1.mp4")

# while True:
#     ret, frame = cap.read()
#     imgH, imgW, _ = frame.shape
#     x1, x2, w1, h1 = 0, 0, imgH, imgW
#     imgchar = pytesseract.image_to_string(frame, lang='rus')
#     # cv2.putText(frame, imgchar, (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
#     print(imgchar)
#     # font = cv2.FONT_HERSHEY_SIMPLEX
#     cv2.imshow('text', frame)
#     if cv2.waitKey(2) & 0xFF == ord('q'):
#         break
    
# cap.release()
# cv2.destroyAllWindows()

import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text
    except sr.UnknownValueError:
        return "Речь не была распознана"
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания речи; {e}"
    
def video_to_text(video_file_path):
    video = VideoFileClip(video_file_path)
    audio = video.audio
    temp_audio_file = "temp_audio.wav"
    audio.write_audiofile(temp_audio_file, codec='pcm_s16le')

    recognizer = sr.Recognizer()

    audio_segment = AudioSegment.from_wav(temp_audio_file)

    if audio_segment.frame_rate != 16000:
        audio_segment = audio_segment.set_frame_rate(16000)
    audio_segment = audio_segment.set_channels(1)

    temp_audio_file = "temp_audio.wav"
    audio_segment.export(temp_audio_file, format="wav")

    with sr.AudioFile(temp_audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text
    except sr.UnknownValueError:
        return "Речь не была распознана"
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания речи; {e}"

# Пример использования функции
# audio_file_path = "1_2.wav"
# text = audio_to_text(audio_file_path)
# print(text)

# Пример использования функции
video_file_path = "17_2.mp4"
text = video_to_text(video_file_path)
print(text)