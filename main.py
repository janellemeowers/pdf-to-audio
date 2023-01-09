from tkinter import *
import customtkinter
from tkinter.filedialog import askopenfilename
import threading
from pathlib import Path
from PyPDF2 import PdfReader
#speak text
import pyttsx3
#for file path
import os

window = Tk()

global uploaded_pdf, pdf_name, pdf_text

def pdf_upload():
    global uploaded_pdf, pdf_name, pdf_text
    uploaded_pdf = askopenfilename()
    fullname_file = os.path.basename(uploaded_pdf)
    pdf_name = os.path.splitext(fullname_file)[0]
    pdf_text = Label(text=f"Converting {fullname_file}")
    pdf_text.place(x=100, y=110)
    pdf_to_audio()

def string_to_mp3():
    #download folder
    path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
    #engine module
    engine = pyttsx3.init()
    #pycharm bug, download should work
    engine.save_to_file(pdf_string, f"{path_to_download_folder}/{pdf_name}.mp3")
    engine.say(pdf_string)
    engine.runAndWait()
    print("done")

def pdf_to_audio():
    global pdf_string
    pdf_string = ""

    try:
        #PDF reader object
        reader = PdfReader(uploaded_pdf)
        pages_num = len(reader.pages)

        for number in range(pages_num):
            #read page
            page = reader.pages[number]
            #add text from each page
            pdf_string += page.extract_text()
        #print(pdf_string)
        #run multi functions without tkinter closing mloop
        #daemon means run in bg
        threading.Thread(
            target=string_to_mp3, daemon=True).start()
        pdf_text.configure(text=f"Success! {pdf_name}.mp3\n was downloaded", bg="green")

    except (NameError, FileNotFoundError):
        pdf_text.configure(text="Error with file", bg="red")




window.title("PDF to Audio Converter")
window.minsize(width=500, height=300)
window.config(padx=20, pady=50, bg='AliceBlue')

convert_btn = customtkinter.CTkButton(master=window, text="Convert PDF to Audio", width=200,
                     command=pdf_upload).place(x=100, y=80)







window.mainloop()