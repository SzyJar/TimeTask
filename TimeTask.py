from datetime import datetime
import tkinter as tk
import csv
import sys

startTime = 0
endTime = 0
taskOngoing = 0

def setStartTime():
    global startTime
    startTime = datetime.now()
    global taskOngoing
    taskOngoing = 1

def setEndTime():
    global endTime
    endTime = datetime.now()
    global taskOngoing
    taskOngoing = 0
    global taskTime 
    taskTime = endTime - startTime
    print(taskTime)
    with open('savedTasks.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([taskTime])

## Open data file if possible, if not then make data file
try:
    with open('savedTasks.csv', newline='') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            print(', '.join(row))
except:
    with open('savedTasks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
## GUI
root = tk.Tk()
root.title("TimeTask")
root.resizable(width=False, height=False)

canvas = tk.Canvas(root, height=500, width=500, bg ="#404040").pack()

buttonStart=tk.Button(canvas, text="Start task", command=setStartTime)
buttonStart.place(x=50,y=400, height = 50, width = 150)

buttonEnd=tk.Button(canvas, text="End task", command=setEndTime)
buttonEnd.place(x=300,y=400, height = 50, width = 150)

root.mainloop()