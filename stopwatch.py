import tkinter as Tkinter
from datetime import datetime


seconds = 79200
stopwatch_running = False


def update_label(lbl):
    def update_seconds():
        if stopwatch_running:
            global seconds

            tt = datetime.fromtimestamp(seconds)
            string = tt.strftime("%H:%M:%S")
            display = string

            lbl['text'] = display

            lbl.after(1000, update_seconds)
            seconds += 1

    update_seconds()


def start(lbl):
    global stopwatch_running
    stopwatch_running = True
    update_label(lbl)


def stop():
    global stopwatch_running
    stopwatch_running = False


def reset(lbl):
    global seconds, stopwatch_running
    seconds = 79200

    if stopwatch_running:
        stopwatch_running = False

    lbl['text'] = '00:00:00'


root = Tkinter.Tk()
root.title("Stopwatch")
root.minsize(width=250, height=70)

label = Tkinter.Label(root, text="00:00:00", fg="black", font="Verdana 30 bold")
label.pack()

f = Tkinter.Frame(root)
f.pack(anchor='center', pady=5)

root.protocol("WM_DELETE_WINDOW", lambda: None)

start(label)
root.mainloop()
