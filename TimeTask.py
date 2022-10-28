from datetime import datetime

import tkinter as tk

startTime = 0
endTime = 5
taskOngoing = 0

def setStartTime():
    global startTime
    startTime = datetime.now()
    global taskOngoing
    taskOngoing = 1
    startTimeLabel=tk.Label(text=startTime, bg="white")
    startTimeLabel.place(x=25,y=85)
    print(taskOngoing)

def setEndTime():
    global endTime
    endTime = datetime.now()
    global taskOngoing
    taskOngoing = 0
    endTimeLabel=tk.Label(text=endTime, bg="white")
    endTimeLabel.place(x=200,y=85)

## GUI
root = tk.Tk()
root.title("TimeTask")
root.resizable(width=True, height=True)

canvas = tk.Canvas(root, height=500, width=1000, bg ="#404040").pack()
if taskOngoing == 0:
    buttonStart=tk.Button(canvas, text="Start task", command=setStartTime )
    buttonStart.place(x=100,y=100)
else:
    buttonEnd=tk.Button(canvas, text="End task", command=setEndTime )
    buttonEnd.place(x=300,y=100)






root.mainloop()