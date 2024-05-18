# import cv2
# import pytesseract
# import numpy as np
# import msvcrt

# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# cap = cv2.VideoCapture("15_1.mp4")
# cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
# text_on_frame = ""

# while True:
#     ret, frame = cap.read()
#     imgH, imgW, _ = frame.shape
#     x1, x2, w1, h1 = 0, 0, imgH, imgW
#     imgchar = pytesseract.image_to_string(frame, lang='rus')
#     print(imgchar)
#     # text_on_frame += imgchar
#     if msvcrt.kbhit():
#         key = msvcrt.getch()
#         if key == b'q' or key == b'Q':
#             break
#     # cv2.imshow('text', frame)
#     # if cv2.waitKey(2) & 0xFF == ord('q'):
#     #     break
# # print(text_on_frame)
    
# cap.release()
# cv2.destroyAllWindows()

import os
# import speech_recognition as sr
# from moviepy.editor import VideoFileClip
# from pydub import AudioSegment

# def audio_to_text(audio_file_path):
#     recognizer = sr.Recognizer()

#     with sr.AudioFile(audio_file_path) as source:
#         audio_data = recognizer.record(source)

#     try:
#         text = recognizer.recognize_google(audio_data, language="ru-RU")
#         return text
#     except sr.UnknownValueError:
#         return "Речь не была распознана"
#     except sr.RequestError as e:
#         return f"Ошибка сервиса распознавания речи; {e}"
    
# def video_to_text(video_file_path):
#     video = VideoFileClip(video_file_path)
#     audio = video.audio
#     temp_audio_file = "temp_audio.wav"
#     audio.write_audiofile(temp_audio_file, codec='pcm_s16le')

#     recognizer = sr.Recognizer()

#     audio_segment = AudioSegment.from_wav(temp_audio_file)

#     if audio_segment.frame_rate != 16000:
#         audio_segment = audio_segment.set_frame_rate(16000)
#     audio_segment = audio_segment.set_channels(1)

#     temp_audio_file = "temp_audio.wav"
#     audio_segment.export(temp_audio_file, format="wav")

#     with sr.AudioFile(temp_audio_file) as source:
#         audio_data = recognizer.record(source)

#     try:
#         text = recognizer.recognize_google(audio_data, language="ru-RU")
#         return text
#     except sr.UnknownValueError:
#         return "Речь не была распознана"
#     except sr.RequestError as e:
#         return f"Ошибка сервиса распознавания речи; {e}"
    
def process_in_folder(folder_path):
    texts = {}
    for filename in os.listdir(folder_path):
        print(filename)
        if filename.endswith((".mp4")):  # Добавить нужные форматы
            video_file_path = os.path.join(folder_path, filename)
            text = video_to_text(video_file_path)
            texts[filename] = text
            #print(f"Processed {filename}: {text}...")
        if filename.endswith((".wav")) and filename != "temp_audio.wav":  # Добавить нужные форматы
            audio_file_path = os.path.join(folder_path, filename)
            text = audio_to_text(audio_file_path)
            texts[filename] = text
            #print(f"Processed {filename}: {text}...")
    return texts

folder_path = os.path.abspath(os.getcwd() + "/files")
texts = process_in_folder(folder_path)

# # output_file = "output_texts.txt"
# # with open(output_file, "w", encoding="utf-8") as f:
# #     for filename, text in texts.items():
# #         f.write(f"Filename: {filename}\n")
# #         f.write(f"Text: {text}\n\n")

# for name, text in texts.items():
#     # if "скидка" in text and "доставка" in text:
#     #     print(name, 'segment: 3')
#     # elif "скидка" in text:
#     #     print(name, 'segment: 0')
#     # elif "карта" in text:
#     #     print(name, 'segment: 8')
#     print(text)
# #print(texts)

# txt = """
# ПРОМО - Акция, Скидка, Низкая цена, **% and !=карта(проценты но не карта)
# Доставка - Доставка, довезем
# ИМИДЖ - Подарочный набор, Подарочная карта, Подарок, 
# Лояльность - Постоянный покупатель, Бонусная карта, Накопительная карта, Бонусы
# Кредитование - Кредит 
# Range - Скидки and дата(9.9.22), Новый год 
# Услуги бизнесу - Перевод для бизнеса, счёт для бизнеса, бизнес and банк
# Кредитные карты - Кредитная карта
# Инвестиционные продукты - Вклад, Накопительный счет
# Экосистемные сервисы - Подписка, Youtube Premium
# Музыка - Музыка, слушать, чарт
# Колонки+Голосовой помощник - станция, капсула, колонка
# Клипы - Клипы, короткие ролики, (если считают любое видео, то фильм, эфир)
# Соц сети - Vkontakte and Вконтакте, Odnoklassniki Одноклассники
# """

# import re

# pattern = re.compile(
#     r"\b("
#     r"акци[яиюейям](?:ми|х)?|"
#     r"скидк[ауеои]|"
#     r"низк[аяуеи][\s-]*цен[ауыеио]|"
#     r"доставк[ауеои]|"
#     r"довез(?:ём|ем)|"
#     r"подарочн(?:ый|ая|ым|ую|ого|ому|ым|ом|е)[\s-]*(?:набор|карт[ауеои])|"
#     r"подар[оккауеио]{1,2}|"
#     r"постоянн[аяуюыеои]{1,2}[\s-]*покупател[ьяюеио]{1,2}|"
#     r"бонусн[аяуюыеои]{1,2}[\s-]*карт[ауеои]|"
#     r"накопительн[аяуюыеои]{1,2}[\s-]*карт[ауеои]|"
#     r"бонус[ыаеиоу]{0,2}|"
#     r"кредит[ауеои]|"
#     r"нов[ыйаяоеуюыми]{1,2}[\s-]*год[ауеои]?|"
#     r"перевод[\s-]*для[\s-]*бизнес[ауеио]?|"
#     r"сч[её]т[\s-]*для[\s-]*бизнес[ауеио]?|"
#     r"бизнес[ауеио]?|"
#     r"банк[ауеио]?|"
#     r"кредитн[аяуюыеои]{1,2}[\s-]*карт[ауеои]|"
#     r"вклад[ауеои]?|"
#     r"накопительн[аяуюыеои]{1,2}[\s-]*сч[её]т[ауеои]?|"
#     r"подписк[ауеои]|"
#     r"youtube[\s-]*premium|"
#     r"музык[ауеои]|"
#     r"слуша[тьюием]|"
#     r"чарт[ауеои]?|"
#     r"станци[яиюейям]|"
#     r"колонк[ауеои]|"
#     r"вконтакт[еую]|"
#     r"клип[ыуеоаи]"
#     r")\b",
#     re.IGNORECASE
# )

# matches = pattern.findall(txt)
# print(matches)

# import pymorphy2

# morph = pymorphy2.MorphAnalyzer()
# target_word = "Накопительный счет"
# target_lemmas = {target_word}

# for parse in morph.parse(target_word):
#     target_lemmas.update(parse.lexeme)

# matches = []
# for word in txt.split():
#     normalized_word = morph.parse(word.strip(".,!?"))[0].normal_form
#     if normalized_word in target_lemmas:
#         matches.append(word.strip(".,!?"))

# print(matches)

# # Пример использования функции
# # audio_file_path = "1_2.wav"
# # text = audio_to_text(audio_file_path)
# # print(text)

# # Пример использования функции
# # video_file_path = "17_2.mp4"
# # text = video_to_text(video_file_path)
# # print(text)

# from vosk import Model, KaldiRecognizer, SetLogLevel
# from pydub import AudioSegment
# import subprocess
# import json
# import os

# SetLogLevel(0)

# # Проверяем наличие модели
# # if not os.path.exists("vosk-model-ru-0.22"):
# #     print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
# #     exit (1)

# # Устанавливаем Frame Rate
# FRAME_RATE = 16000
# CHANNELS=1

# model = Model("C:\\Users\\faser\\Downloads\\media_wise\\media_wise\\To_text\\To_text\\vosk-model-ru-0.22")
# rec = KaldiRecognizer(model, FRAME_RATE)
# rec.SetWords(True)

# # Используя библиотеку pydub делаем предобработку аудио
# mp3 = AudioSegment.from_mp3('1_2.wav')
# mp3 = mp3.set_channels(CHANNELS)
# mp3 = mp3.set_frame_rate(FRAME_RATE)

# # Преобразуем вывод в json
# rec.AcceptWaveform(mp3.raw_data)
# result = rec.Result()
# text = json.loads(result)["text"]

# # Добавляем пунктуацию
# #cased = subprocess.check_output('python3 recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)

# print(text)

# # Записываем результат в файл "data.txt"
# #with open('data.txt', 'w') as f:
# #    json.dump(cased, f, ensure_ascii=False, indent=4)