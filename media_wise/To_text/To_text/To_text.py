import cv2
import pytesseract
import numpy as np
import os
import wave
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, ffmpeg_tools
import re
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

model_path = "vosk-model-ru-0.22"
model = Model(model_path)

def transcribe_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    
    audio = audio.set_channels(1).set_frame_rate(16000)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    full_result = []
    while True:
        data = wf.readframes(8000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            full_result.append(res)
        else:
            res = json.loads(rec.PartialResult())
            full_result.append(res)
    
    res = json.loads(rec.FinalResult())
    full_result.append(res)

    text = " ".join(res.get('text', '') for res in full_result if 'text' in res)

    return text

def transcribe_video(video_path):
    if video_path.endswith((".avi")):
        video_temp_path = "temp_video.mp4"        
        path = os.path.abspath(os.getcwd() +"/ffmpeg/bin/ffmpeg.exe")
        cmd_mp4 = [path, '-i', video_path, '-vcodec', 'libx264', video_temp_path]
        process = subprocess.run(cmd_mp4, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # path.input(video_path).output(video_temp_path, vcodec='libx264').run(capture_stdout=True, capture_stderr=True)
        video = VideoFileClip(video_temp_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        video.close()
        
        text = transcribe_audio(audio_path)
        os.remove(audio_path)
        os.remove(video_temp_path)
    else:
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        video.close()
    
        text = transcribe_audio(audio_path)
        os.remove(audio_path)
    
    return text
    
def video_to_text(video_file_path):
    pytesseract.pytesseract.tesseract_cmd = os.path.abspath(os.getcwd() + "/Tesseract-OCR/tesseract.exe")
    cap = cv2.VideoCapture(video_file_path)
    current_time = 0
    text = ""

    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time)
        ret, frame = cap.read()        
        if not ret:
            break
        imgchar = pytesseract.image_to_string(frame, lang='rus')
        text += imgchar
        current_time += 1000
        
    cap.release()
    cv2.destroyAllWindows()

    return text  
    
def process_in_folder(folder_path):
    texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith((".wav")) and filename != "temp_audio.wav" and filename != "temp.wav":
            audio_file_path = os.path.join(folder_path, filename)
            text = transcribe_audio(audio_file_path)
            texts[filename] = text
        else:
            video_file_path = os.path.join(folder_path, filename)
            text = video_to_text(video_file_path)
            text_audio = transcribe_video(video_file_path)
            texts[filename] = text + text_audio        
    return texts

folder_path = os.path.abspath(os.getcwd() + "/data")
texts = process_in_folder(folder_path)
segments = {}

# import work_with_excel as exc

# exc.start("uploads/file.xlsx")

# for name, text in texts.items():
#     text_low = text.lower()
#     print(text_low)
#     if (re.search(r"скидк[ауеои]", text_low) or re.search(r"акци[яиюейям](?:ми|х)?", text_low) or re.search(r"низк[аяуеи][\s-]*цен[ауыеио]", text_low)) and (re.search(r"доставк[ауеои]", text_low) or re.search(r"довез(?:ём|ем)", text_low)):
#         segments[name] = 3
#         exc.work("uploads/file.xlsx", [3, name])
#     elif (re.search(r"скидк[ауеои]", text_low) or re.search(r"акци[яиюейям](?:ми|х)?", text_low) or re.search(r"низк[аяуеи][\s-]*цен[ауыеио]", text_low)) and (re.search(r"постоянн[аяуюыеои]{1,2}[\s-]*покупател[ьяюеио]{1,2}", text_low) or re.search(r"бонусн[аяуюыеои]{1,2}[\s-]*карт[ауеои]", text_low) or re.search(r"накопительн[аяуюыеои]{1,2}[\s-]*карт[ауеои]", text_low) or re.search(r"бонус[ыаеиоу]{0,2}", text_low)):
#         segments[name] = 4
#         exc.work("uploads/file.xlsx", [4, name])
#     elif re.search(r"скидк[ауеои]", text_low) or re.search(r"акци[яиюейям](?:ми|х)?", text_low) or re.search(r"низк[аяуеи][\s-]*цен[ауыеио]", text_low):
#         segments[name] = 6
#         exc.work("uploads/file.xlsx", [6, name])
#     elif (re.search(r"подарочн(?:ый|ая|ым|ую|ого|ому|ым|ом|е)[\s-]*(?:набор|карт[ауеои])", text_low) or re.search(r"подар[оккауеио]{1,2}", text_low)) and (re.search(r"доставк[ауеои]", text_low) or re.search(r"довез(?:ём|ем)", text_low)):
#         segments[name] = 5
#         exc.work("uploads/file.xlsx", [5, name])
#     elif (re.search(r"подарочн(?:ый|ая|ым|ую|ого|ому|ым|ом|е)[\s-]*(?:набор|карт[ауеои])", text_low) or re.search(r"подар[оккауеио]{1,2}", text_low)) and (re.search(r"постоянн[аяуюыеои]{1,2}[\s-]*покупател[ьяюеио]{1,2}", text_low) or re.search(r"бонусн[аяуюыеои]{1,2}[\s-]*карт[ауеои]", text_low) or re.search(r"накопительн[аяуюыеои]{1,2}[\s-]*карт[ауеои]", text_low) or re.search(r"бонус[ыаеиоу]{0,2}", text_low)):
#         segments[name] = 2
#         exc.work("uploads/file.xlsx", [2, name])
#     elif re.search(r"подарочн(?:ый|ая|ым|ую|ого|ому|ым|ом|е)[\s-]*(?:набор|карт[ауеои])", text_low) or re.search(r"подар[оккауеио]{1,2}", text_low):
#         segments[name] = 1
#         exc.work("uploads/file.xlsx", [1, name])
#     elif re.search(r"кредит[ауеои]", text_low):
#         segments[name] = 8
#         exc.work("uploads/file.xlsx", [8, name])
#     elif (re.search(r"нов[ыйаяоеуюыми]{1,2}[\s-]*год[ауеои]?", text_low) or re.search(r'\b(первое|второе|третье|четвёртое|пятое|шестое|седьмое|восьмое|девятое|десятое|одиннадцатое|двенадцатое|тринадцатое|четырнадцатое|пятнадцатое|шестнадцатое|семнадцатое|восемнадцатое|девятнадцатое|двадцатое|двадцать (первое|второе|третье|четвёртое|пятое|шестое|седьмое|восьмое|девятое)|тридцатое|тридцать первое)\s(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s(две тысячи (первого|второго|третьего|четвёртого|пятого|шестого|седьмого|восьмого|девятого|десятого|одиннадцатого|двенадцатого|тринадцатого|четырнадцатого|пятнадцатого|шестнадцатого|семнадцатого|восемнадцатого|девятнадцатого|двадцатого|двадцать первого|двадцать второго|двадцать третьего|двадцать четвёртого|двадцать пятого|двадцать шестого|двадцать седьмого|двадцать восьмого|двадцать девятого|тридцатого|тридцать первого))\sгода\b', text_low) and re.search(r"скидк[ауеои]", text_low) or re.search(r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})\b', text_low) and re.search(r"скидк[ауеои]", text_low)):
#         segments[name] = 9
#         exc.work("uploads/file.xlsx", [9, name])
#     elif (re.search(r"перевод[\s-]*для[\s-]*бизнес[ауеио]?", text_low) or re.search(r"сч[её]т[\s-]*для[\s-]*бизнес[ауеио]?", text_low) or re.search(r"бизнес[ауеио]?", text_low)) and re.search(r"банк[ауеио]?", text_low):
#         segments[name] = 11
#         exc.work("uploads/file.xlsx", [11, name])
#     elif re.search(r"кредитн[аяуюыеои]{1,2}[\s-]*карт[ауеои]", text_low):
#         segments[name] = 12
#         exc.work("uploads/file.xlsx", [12, name])
#     elif re.search(r"вклад[ауеои]?", text_low) or re.search(r"накопительн[аяуюыеои]{1,2}[\с-]*сч[её]т[ауеои]?", text_low):
#         segments[name] = 13
#         exc.work("uploads/file.xlsx", [13, name])
#     elif re.search(r"подписк[ауеои]", text_low) or re.search(r"youtube[\s-]*premium", text_low):
#         segments[name] = 14
#         exc.work("uploads/file.xlsx", [14, name])
#     elif re.search(r"музык[ауеои]", text_low) or re.search(r"слуша[тьюием]", text_low) or re.search(r"чарт[ауеои]?", text_low):
#         segments[name] = 15
#         exc.work("uploads/file.xlsx", [15, name])
#     elif re.search(r"станци[яиюейям]", text_low) or re.search(r"колонк[ауеои]", text_low) or re.search(r"капсул[ауе]", text_low) or re.search(r"алис[ауе]", text_low):
#         segments[name] = 16
#         exc.work("uploads/file.xlsx", [16, name])
#     elif re.search(r"клип[ыуеоаи]", text_low) or re.search(r'\bкоротк\w* ролик\w*\b', text_low) or re.search(r'\bфильм\w*\b', text_low) or re.search(r'\bэфир\w*\b', text_low):
#         segments[name] = 17
#         exc.work("uploads/file.xlsx", [17, name])
#     elif re.search(r"вконтакт[еую]", text_low) or re.search(r'\bодноклассник(?:и|ов|ам|ами|ах)\b', text_low):
#         segments[name] = 18
#         exc.work("uploads/file.xlsx", [18, name])
        
app = Flask(__name__, static_folder='uploads')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
@app.route('/<filename>')
def display_file(filename='file.xlsx'): #- здесь потом пропишете название с путём файла, немного костыльный метод, сам файл пихать в uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_excel(file_path)
    
    # # Графики собираются из первого столбца с числами - желательно запихнуть числа в первый столбец 
    # numerical_columns = df.select_dtypes(include=['number']).columns
    # if len(numerical_columns) == 0:
    #     return "No numerical columns found in the file."

    if len(df.columns) < 3:
        return "Должно быть три столбца в файле"

    brands = df.iloc[:, 2].unique().tolist()
    selected_brand = request.form.get('brand', brands[0])

    filtered_df = df[df.iloc[:, 2] == selected_brand]
    numbers = filtered_df.iloc[:, 0]
    names = filtered_df.iloc[:, 1]
    
    unique_counts = {}
    for name in numbers:
        if str(name) in unique_counts:
            unique_counts[str(name)] += 1
        else:
            unique_counts[str(name)] = 1
    print(unique_counts)
    numbers_2 = df.iloc[:, 0]
    names_2 = df.iloc[:, 1]
    brands_2 = df.iloc[:, 2]

    unique_counts_2 = {}
    
    for num in numbers_2:
        if num in unique_counts_2:
            unique_counts_2[num] += 1
        else:
            unique_counts_2[num] = 1
        
    # Гистограмма
    plt.figure(figsize=(14, 8))
    plt.bar(unique_counts.keys(), unique_counts.values())
    plt.title(f'Гистограмма для бренда {selected_brand}')
    plt.xlabel('Названия')
    plt.ylabel('Количество')
    histogram_path = os.path.join(app.config['UPLOAD_FOLDER'], 'histogram.png')
    plt.xticks(rotation=90)
    plt.savefig(histogram_path)
    plt.close()
        
    # Круговая диаграмма
    plt.figure(figsize=(14, 8))
    plt.pie(unique_counts_2.values(), labels=unique_counts_2.keys(), autopct='%1.1f%%')
    plt.title('Общая круговая диаграмма')
    piechart_path = os.path.join(app.config['UPLOAD_FOLDER'], 'piechart.png')
    plt.savefig(piechart_path)
    plt.close()


    # # Линейный график
    # plt.figure(figsize=(14, 8))
    # df[numerical_columns[0]].plot(kind='line')
    # plt.title(f'Линейный график {numerical_columns[0]}')
    # #plt.xlabel('Index')
    # plt.ylabel(numerical_columns[0])
    # lineplot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'lineplot.png')
    # plt.savefig(lineplot_path)
    # plt.close()


    wb = load_workbook(file_path)
    ws = wb.active

    # Изображи в excel в виде картинок
    img1 = Image(histogram_path)
    #img2 = Image(lineplot_path)
    img3 = Image(piechart_path)


    ws.add_image(img1, 'F10')
    #ws.add_image(img2, 'F30')
    ws.add_image(img3, 'F30')

    updated_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'updated_' + filename)
    wb.save(updated_file_path)

    return render_template('display.html', 
                           histogram_url=url_for('static', filename='histogram.png'),
                           piechart_url=url_for('static', filename='piechart.png'),
                           download_url=url_for('download_file', filename='updated_' + filename),
                           brands=brands,
                           selected_brand=selected_brand,
                           filename=filename)


@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
app.run(debug=True)
