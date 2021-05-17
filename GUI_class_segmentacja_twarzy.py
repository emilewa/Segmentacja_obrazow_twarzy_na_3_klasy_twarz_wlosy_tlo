# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 22:38:34 2020

@author: emilk
"""

import time
import tkinter as tk
import cv2
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
from PIL import ImageTk, Image
import os
from predict2 import *    

WIDTH_IMG = 420
HEIGHT_IMG = 420
    
COLOR_1 = '#000060'
COLOR_2 = '#1c2bca'

class App():
    STAN = 0
    SCIEZKA_OBRAZU_ORYGINALNEGO = ""
    SCIEZKA_OBRAZU = ""
    WYBRANY_ALGORYTM = ""
    NAZWA_FOLDERU_ROBOCZEGO = ""
    SCIEZKA_OBRAZU_WYNIKOWEGO = ""
    
    def __init__(self,window, frame0):
        
        self.frame0 = frame0
        self.window = window

        button_zaladujPlik = tk.Button(master=frame_1, text='ZAŁADUJ ZDJĘCIE', font=font ,bd=10, width=15, bg=COLOR_2, fg="#ffffff", command=otworzPlik )
        button_zaladujPlik.pack(fill=tk.BOTH, expand=True)
        
        #Pole tekstowe wypisujace scieżke wybranego pliku
        self.text = tk.StringVar()
        self.text.set("C://...")
        text_sciezka = tk.Label(master=frame_2, textvariable=self.text,font=font ,relief=tk.SUNKEN,bd=10, bg=COLOR_1,  fg="#ffffff")
        text_sciezka.pack(fill=tk.BOTH, expand=True)   
        
        
        #2 kolumna frame2
        self.frame1 = tk.Frame(master=self.window, width=200)
        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
         #3 kolumna w frame2 , podział na frame2_1 , frame2_2
        self.frame1_1 = tk.Frame(master=self.frame1)
        self.frame1_1.pack(fill=tk.BOTH, expand=True)
        self.frame1_2 = tk.Frame(master=self.frame1)
        self.frame1_2.pack(fill=tk.BOTH, expand=True)
        
        #3 kolumna frame2 
        self.frame2 = tk.Frame(master=self.window, width=10, bg="yellow")
        self.frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        #3 kolumna w frame2 , podział na frame2_1 , frame2_2
        self.frame2_1 = tk.Frame(master=self.frame2)
        self.frame2_1.pack(fill=tk.BOTH, expand=True)
        self.frame2_2 = tk.Frame(master=self.frame2)
        self.frame2_2.pack(fill=tk.BOTH, expand=True)
        
        #4 kolumna form3
        self.frame3 = tk.Frame(master=self.window, width=200)
        self.frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        #4 kolumna w frame3 , podział na frame3_1 , frame3_2
        self.frame3_1 = tk.Frame(master=self.frame3)
        self.frame3_1.pack(fill=tk.BOTH, expand=True)
        self.frame3_2 = tk.Frame(master=self.frame3)
        self.frame3_2.pack(fill=tk.BOTH, expand=True)


        #frame0_4 z 1 kolumny 
        self.frame0_4 = tk.Frame(master=self.frame0, height=100)
        self.frame0_4.pack(fill=tk.BOTH, expand=True)
        
        
        #Przycisk uchuchom
        self.button_ZDJ_CAM = tk.Button(master=self.frame0_4, text='ZDJĘCIE KAMERA',bd=15, font=("Arial", 10, 'bold'),   bg=COLOR_2, fg="#ffffff", command=self.Zdj_camera)
        self.button_ZDJ_CAM.pack(fill=tk.BOTH, expand=True)
        
        #Przycisk uchuchom
        self.button_uruchom = tk.Button(master=self.frame0_4, text='URUCHOM',bd=15, font=("Arial", 10, 'bold'),   bg=COLOR_2, fg="#ffffff", command=self.Uruchom)
        self.button_uruchom.pack(fill=tk.BOTH, expand=True)


    


    def Zdj_camera(self):
        
        for w2_1 in self.frame1.winfo_children():
                w2_1.destroy()
        
        self.video = MyVideoCapture(0)
        ret, obraz  = self.video.get_frame()
        obraz = obraz[0:480,0:480]
        obraz = cv2.flip(obraz,1)
        
        
        #cv2.rectangle(obraz,(0,0),(480,480),(255, 0, 0) ,1)
        nazwa = "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S")    
        self.ZapisDoFolderu(nazwa, nazwa, PIL.Image.fromarray(cv2.cvtColor(obraz, cv2.COLOR_BGR2RGB)))
 
        print ("SCIEZKA_OBRAZU:  "+ self.SCIEZKA_OBRAZU)
        print("SCIEZKA_OBRAZU_ORYGINALNEGO:  "+ self.SCIEZKA_OBRAZU_ORYGINALNEGO)
        print ("SCIEZKA_OBRAZU_WYNIKOWEGO:  " + self.SCIEZKA_OBRAZU_WYNIKOWEGO)

        #Przetwarzanie obrazu wczytywanego do canvas
        img = PIL.Image.fromarray(cv2.cvtColor(obraz, cv2.COLOR_BGR2RGB))
        img = img.resize((WIDTH_IMG,HEIGHT_IMG), Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(img)
                
        self.frameObrazek(self.frame1, photo, "ZDJĘCIE Z KAMERY")
        
        self.window.mainloop()
        self.video.__del__()
        
    def frameObrazek(self, master, obraz, opis):
        
        frame0 = tk.Frame(master=master, bg="purple")
        frame0.pack()
    
        frame = tk.Frame(master=frame0, relief=tk.SUNKEN, borderwidth=6)
        frame.pack(fill=tk.X)
        label = tk.Label(master=frame, text=opis, font=("Arial", 10, 'bold'))
        label.pack(side=tk.TOP)
    
        frame1 = tk.Frame(master=frame0, width=WIDTH_IMG, relief=tk.SUNKEN, height=HEIGHT_IMG, borderwidth=5)
        frame1.pack(fill=tk.X)
        
        canvas = tk.Canvas(frame1, width = WIDTH_IMG, height = HEIGHT_IMG)
        canvas.pack(fill=tk.X)
        #canvas.place(x = 0)
        canvas.create_image(0, 0, image = obraz, anchor = tk.NW)
        
        
    def OdczytajRysuj(self, master, sciezka, opis):    
        for w2_1 in master.winfo_children():
                w2_1.destroy()
        
        img = Image.open(sciezka)
        img = img.resize((WIDTH_IMG, HEIGHT_IMG), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.frameObrazek(master, img, opis)
        self.window.mainloop()
    
    def Uruchom_algorytm(self):
        print("Uruchom algorytm !")
        Predict_Img(self.SCIEZKA_OBRAZU, self.NAZWA_FOLDERU_ROBOCZEGO)
    
    def Czysc(self):
        self.SCIEZKA_OBRAZU_ORYGINALNEGO = ""
        self.SCIEZKA_OBRAZU = ""
        self.WYBRANY_ALGORYTM = ""
        self.NAZWA_FOLDERU_ROBOCZEGO = ""
        
        for w1 in self.frame1.winfo_children():
            w1.destroy()
        if self.STAN != 0 :
            print("USUN")
            for w2_1 in self.frame2_1.winfo_children():
                w2_1.destroy()
               
            for w2_2 in self.frame2_2.winfo_children():
                w2_2.destroy()
                
            for w3_1 in self.frame3_1.winfo_children():
                w3_1.destroy()
                
            for w3_2 in self.frame3_2.winfo_children():
                w3_2.destroy()    
           

    #Utworzenie folderu z wynikami i zapis obrazu
    def ZapisDoFolderu(self, nazwafolderu, nazwaObrazu, obraz):
        
        if os.path.exists(nazwafolderu):
            print("Istnieje!")
        else:
            os.mkdir(nazwafolderu)
        sciezka = nazwafolderu+"/"+nazwaObrazu+".png"
        obraz.save(sciezka)
        self.NAZWA_FOLDERU_ROBOCZEGO = nazwafolderu
        self.SCIEZKA_OBRAZU = sciezka
        self.SCIEZKA_OBRAZU_WYNIKOWEGO = nazwafolderu+"/"+"wynik.png"

        print("Nazwa folderu roboczego: "+ self.NAZWA_FOLDERU_ROBOCZEGO)
        return sciezka  
            

    def Uruchom(self):
    
        
        if  os.path.isfile(self.SCIEZKA_OBRAZU):
            print("Uruchom z danymi :")
            
            self.Uruchom_algorytm() # FUNKJA ODPOWIEDZIALNA ZA URUCHOMIENIR ALGORYTMU I TWORZENIE OBRAZU PREDICT
            self.OdczytajRysuj(self.frame3_1, self.SCIEZKA_OBRAZU_WYNIKOWEGO, "WYNIK DZIAŁANIA ALGORYTMU")
            
        
        self.window.mainloop()
            
#############################################################################################################################################################
#Otwórz plik okno wyboru pliku
def openfn():
    filename = filedialog.askopenfilename(title='ZAŁADUJ OBRAZ',filetypes = (("png","*.png"),("jpg","*.jpg")))
    print("Scieżka: "+filename)
    return filename

#Nazwa pliku z sciezki        
def NazwaPliku(sciezka):
    nazwaiRozszerznie = os.path.basename(sciezka)
    nazwaPliku = nazwaiRozszerznie.split('.')[0]
    return nazwaPliku

#Wybór, załadowanie pliku 
def otworzPlik():

        x = openfn()     
        if x != "":
            a.text.set(x) 
            img = Image.open(x)        
            nazwapliku = NazwaPliku(x)
            a.Czysc()
            a.SCIEZKA_OBRAZU_ORYGINALNEGO = x;
            print(x)
            sciezka = a.ZapisDoFolderu(nazwapliku, "obraz_oryginalny", img)
            print("Scieżka obrazu: "+sciezka)
            if os.path.isfile(a.SCIEZKA_OBRAZU):
                    a.STAN = 1
                    a.OdczytajRysuj(a.frame1, a.SCIEZKA_OBRAZU,"WCZYTANY OBRAZ")
                    

class MyVideoCapture:
     def __init__(self, video_source):
         #otwieram wideo w tym przypadku video_source = 0 bo kamera 
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
             
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
     def get_frame(self):
             ret, frame = self.vid.read()
             if ret:
                 return (ret, frame)
             else:
                 return (ret, None)
       
     def __del__(self):
             self.vid.release()
       
#############################################################################################################################################################        
window = tk.Tk()
window.title("Segmentacja twarzy")
window.geometry("1200x600+1+1")
window.resizable(width=True, height=True)
font = ("Arial", 10, 'bold')

frame = tk.Frame(master=window)
frame.pack(fill=tk.X)

frame_1 = tk.Frame(master=frame, width=100,height=30, relief=tk.SUNKEN, bg=COLOR_1)
frame_1.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

frame_2 = tk.Frame(master=frame, width=300,height=30, relief=tk.SUNKEN, bg=COLOR_1)
frame_2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


     
#1 kolumna frame1                        
frame0 = tk.Frame(master=window,relief=tk.SUNKEN)
frame0.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

#1 kolumna w frame1, podział na frame0_1, frame0_2, frame0_3, frame0_4 
frame0_1 = tk.Frame(master=frame0,bd=10, bg=COLOR_1)
frame0_1.pack(fill=tk.BOTH, expand=True)
frame0_2 = tk.Frame(master=frame0,bd=10, bg=COLOR_1)
frame0_2.pack(fill=tk.BOTH, expand=True)
frame0_3 = tk.Frame(master=frame0,bd=10, bg=COLOR_1)
frame0_3.pack(fill=tk.BOTH, expand=True)

#Instancja klasy App inicjalizacja głównego modułu programu
a = App(window,frame0)

window.update()
window.mainloop()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        