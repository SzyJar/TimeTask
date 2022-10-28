from datetime import datetime

import tkinter as tk

startTime = 0
endTime = 0
taskOngoing = 0

class timeManagement():
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.taskOngoing = 0
    def setStartTime(self):
        self.startTime = (datetime.now())
        startTimeLabel=tk.Label(text=startTime, bg="white")
        startTimeLabel.place(x=25,y=85)
    def setEndTime(self):
       self.endTime = (datetime.now())
       endTimeLabel=tk.Label(text=endTime, bg="white")
       endTimeLabel.place(x=200,y=190)
## GUI
root = tk.Tk()
root.title("TimeTask")
root.resizable(width=True, height=True)

canvas = tk.Canvas(root, height=500, width=1000, bg ="#404040").pack()
if taskOngoing == 0:
    buttonStart=tk.Button(canvas, text="Start task", command=timeManagement.setStartTime)
    buttonStart.place(x=100,y=100)
if taskOngoing == 1:
    buttonEnd=tk.Button(canvas, text="End task", command=timeManagement.setEndTime)
    buttonEnd.place(x=100,y=200)

root.mainloop()