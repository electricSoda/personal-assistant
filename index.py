#import
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from datetime import date
import base64
import requests
import urllib
import soundboard
import fileinput
import webbrowser
import os

NEWSURL = 'https://cnn.com/'

def main():
    global root, timeC, dateC, titleW, weatherCC, weatherCT, weatherCTF, tolist, news, settings, height, width, weathericon, weatherinfo, update, animated
    #root attributes
    root = Tk()
    root.attributes('-fullscreen', True)
    root.title('PA')
    root.config(background='white')


    #get screen dimensions
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    #upload pictures
    o1 = Image.open('settings.png')
    oo1 = ImageTk.PhotoImage(o1)

    #main animation loop
    #booleans
    animated = True
    update = True

    #functions
    def set(event):
        import settings

        settings.sett()

    def openW():
        webbrowser.open_new(NEWSURL)

    def openWC():#for webcam
        import videoexpression

    def websiteWEATHER(event):
        webbrowser.open_new("https://weather.com/weather/hourbyhour/l/237b374cb1a5761e0dabb5a7e5281aeab1fff78ebdb283e1608c12889fe4e0dd")

    def gotS():
        got = tolist.get(ANCHOR)
        soundboard.playcheck()

        indexfile = tolist.get(0, "end").index(got)
        tolist.delete(indexfile)
        tolist.insert(indexfile, "✓" + got)

    #root objects

    #time
    timeC = Label(root)
    timeC.config(font=('Berlin Sans FB', 120), background='white')
    timeC.pack(side=TOP)

    #date
    dateC = Label(root)
    dateC.config(font=('Berlin Sans FB', 40), background='white')
    dateC.pack(side=TOP)

    #weather forecast
    titleW = Label(root, text="Today's Weather")
    titleW.config(font=('Candara bold', 30), background='white')
    titleW.place(x=0, y=height/2)

    #icon
    weathericon = Label(root, bg='light blue')
    height1 = (height / 2) + 60
    weathericon.place(x=0, y=height1)

    weatherCT = Label(root)
    weatherCT.config(font=('Candara light', 20), background='white')
    height2 = (height/2) + 150
    weatherCT.place(x=0, y=height2)

    weatherCTF = Label(root)
    weatherCTF.config(font=('Candara light', 20), background='white')
    height3 = (height / 2) + 190
    weatherCTF.place(x=0, y=height3)

    weatherCC = Label(root)
    weatherCC.config(font=('Candara light', 20), background='white')
    height4 = (height/2) + 230
    weatherCC.place(x=0, y=height4)

    weatherinfo = Label(root, text='More Weather Information', font=('Candara light', 20), background = 'light gray')
    height5 = (height/2) + 270
    weatherinfo.place(x = 0, y = height5)
    weatherinfo.bind('<Button-1>', websiteWEATHER)

    #to do
    listbox_border = Frame(root, bd=1, relief="sunken", background="black")
    listbox_border.pack(padx=10, pady=10, side=RIGHT, expand=False)

    tolist = Listbox(listbox_border, width=60, height=20,
                         borderwidth=0, highlightthickness=0,
                         background=listbox_border.cget("background"),
                         bg='black',
                         fg='white',
                         font=('VT323', 16)
                         )
    vsb = Scrollbar(listbox_border, orient="vertical", command=tolist.yview)
    tolist.configure(yscrollcommand=vsb)
    vsb.pack(side=RIGHT,fill=BOTH)
    tolist.pack(padx=10, pady=10, side=RIGHT, expand=True)

    #tolistbtn
    finished = Button(listbox_border, text='Finished!', command=gotS)
    finished.config(borderwidth=0, bg='white', fg='black')
    finished.pack()

    #news
    news = Button(root, text='Latest News', command = openW)
    news.config(font=('Candara', 25), bg='light gray', fg='black', borderwidth = 0)
    news.place(x=0, y=height-100)

    #settings
    settings = Label(root, text='Settings')
    settings.config(image = oo1, width=45)
    settings.place(x=width-50, y=height-50)
    settings.bind('<Button-1>', set)

    #webcame
    webcame = Button(root, text='Enable Webcam', command = openWC)
    webcame.place(x=0,y=0)

    #files
    with open('tasks.txt', 'r') as ts:
        lines = ts.readlines()

        linecount = 0
        for line in lines:
            tolist.insert(linecount, line)
            linecount += 1

        ts.close()

    #loop
    while animated:
        #time
        now = datetime.now()
        current_time1 = now.strftime("%H")
        current_time2 = now.strftime("%M")
        if int(current_time1) > 12:
            current_time1 = int(current_time1)
            current_time1 = current_time1 - 12

            current_time = str(current_time1) + " : " +current_time2 + " PM"
        else:
            current_time = current_time1 + " : " + current_time2 + " AM"
        timeC.config(text=current_time)

        #date
        dat = date.today()
        datenow = dat.strftime("%B %d, %Y")
        dateC.config(text=datenow)

        #weather api (openweathermap)
        weather_address = "https://api.openweathermap.org/data/2.5/weather?appid=7d1e316e0f1d163abe9e508744e4e3f0&q=Longmont&units=metric"
        json_data = requests.get(weather_address).json()
        json_data1 = json_data['weather'][0]["description"]
        json_data2 = json_data['main']['temp']
        json_data3 = json_data['main']['feels_like']
        weatherCC.config(text='Weather Condition: '+json_data1)
        weatherCT.config(text='Temperature: '+ str(round(json_data2)) + " Celsius")
        weatherCTF.config(text='Feels like: '+ str(round(json_data3)) + " Celsius")

        #image
        jsonicon = json_data["weather"][0]['icon']
        siteicon = "http://openweathermap.org/img/wn/" + jsonicon + "@2x.png"
        u = urllib.request.urlopen(siteicon)
        raw_data = u.read() #returns binary data
        u.close()
        b64_data = base64.encodebytes(raw_data)
        imate = PhotoImage(data=b64_data)
        weathericon.config(image=imate)

        #updating the screen
        if update:
            root.update()
        else:
            root.destroy()
            quit()


def blackout():
    timeC.pack_forget()
    dateC.pack_forget()
    titleW.place_forget()
    weathericon.place_forget()
    weatherCC.place_forget()
    weatherCT.place_forget()
    weatherCTF.place_forget()
    weatherinfo.place_forget()
    tolist.pack_forget()
    news.place_forget()
    settings.place_forget()

    root.config(bg='black')

def unblackout():
    root.destroy()
    main()

def terminateI():
    global update, animated
    update = False
    animated = False
    root.destroy()
    quit()

def addO(addtxt):
    with open('tasks.txt', 'a') as tss:
        tss.write('\n' + addtxt)
        tss.close()
    tolist.insert(END, addtxt)

def deleO(deletxt):
    a = open('tasks.txt')
    b = enumerate(a)
    line_number = ""
    for number, line in b:
        if deletxt in line:
            line_number = number
            break
    tolist.delete(line_number)
    a.close()

    for line in fileinput.input('tasks.txt', inplace=1):
        line = line.strip()
        if not deletxt in line:
            print(line)

def changeURL(url):
    global NEWSURL
    NEWSURL = url
