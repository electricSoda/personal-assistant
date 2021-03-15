from tkinter import *
from tkinter import simpledialog
import index

todO = True

def sett():
    win = Tk()

    win.title('Settings')

    win.iconbitmap(r'settings.ico')

    win.geometry("800x500")

    win.resizable(False, False)

    options = Listbox(win)
    options.config(bg='black', fg='white', width = 20, height = 40, font=('VT323',15))
    options.pack(side=LEFT)



    #functions
    def todoO():
        global add, submit1, dele, submit2, todO
        if todO:
            def addtodo():
                got = add.get()
                index.addO(got)

            def deletodo():
                got = dele.get()
                index.deleO(got)

            add = Entry(win)
            add.pack()

            submit1 = Button(win, text='Add', command=addtodo)
            submit1.pack()

            dele = Entry(win)
            dele.pack()

            submit2 = Button(win, text='Delete', command=deletodo)
            submit2.pack()
            todO = False
        else:
            add.pack_forget()
            submit1.pack_forget()
            dele.pack_forget()
            submit2.pack_forget()
            todO = True

    def newssite():
        siteurl = simpledialog.askstring(title="Site URL", prompt="Please Enter Your Prefered Site URL:")
        index.changeURL(siteurl)
        win.destroy()

    def black():
        def reopen(event):
            win.destroy()
            index.unblackout()

        options.pack_forget()
        win.geometry('50x30')

        back = Label(win, text='Resume Session')
        back.pack()

        back.bind('<Button-1>', reopen)

        index.blackout()
        win.update()


    def terminate():
        win.destroy()
        index.terminateI()

    def getL(event):
        got = options.get(ANCHOR)

        if got == 'To do list options':
            todoO()
        elif got == 'News Configuration':
            newssite()
        elif got == 'Hide GUI':
            black()
        elif got == 'Exit':
            terminate()

    def on_closing():
        win.withdraw()

    #insert
    options.insert(0,'To do list options')
    options.insert(1,'News Configuration')
    options.insert(2, 'Hide GUI')
    options.insert(3, 'Exit')

    #insert listeners
    options.bind('<<ListboxSelect>>', getL)
    win.protocol("WM_DELETE_WINDOW", on_closing)

    win.mainloop()