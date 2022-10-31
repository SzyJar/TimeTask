from datetime import datetime
import tkinter as tk
from tkinter import StringVar, messagebox
import csv as csv

startTime = 0
endTime = 0
taskOngoing = 0
taskName = ''

## Open data file if exists, if not then make new data file
try:
    with open('savedTasks.csv', newline='') as file:
        reader = csv.reader(file, delimiter=";")
except:
    with open('savedTasks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
    messagebox.showinfo("New data file has been created", "Unable to find existing data file, new data file has been created")

## Set task name
def setTaskName():
    global taskName
    taskName = entryTaskName.get()
    if taskName !='':
        statusInfo.set('Currnet task name: '+ taskName)
    else:
        statusInfo.set('Waiting for task name...')

## Get start time
def setStartTime():
    if taskName != "":
        global startTime
        startTime = datetime.now()
        global taskOngoing
        taskOngoing = 1
        root.title("TimeTask (Current task: "+taskName+")")
    else:
        messagebox.showwarning("No task name", "Please set task name before starting task time counter.")

## Get task time and write it to data file
def setEndTime():
    global endTime
    endTime = datetime.now()
    global taskOngoing
    if taskOngoing == 1:
        taskOngoing = 0
        root.title("TimeTask (Idle - no task ongoing)")
        global taskTime    
        taskTime = endTime - startTime
        print(taskTime)
        with open('savedTasks.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([taskTime, taskName])

#### GUI
root = tk.Tk()
root.title("TimeTask (Idle - no task ongoing)")
root.resizable(width=False, height=False)

canvas = tk.Canvas(root, height=500, width=500, bg ="#404040").pack()

## Buttons
buttonStart=tk.Button(canvas, text="Start task", command=setStartTime, font=("Tahoma 9 bold"))
buttonStart.place(x=50,y=430, height = 50, width = 100)

buttonEnd=tk.Button(canvas, text="Set task name", command=setTaskName, font=("Tahoma 9 bold"))
buttonEnd.place(x=200,y=430, height = 50, width = 100)

buttonEnd=tk.Button(canvas, text="End task", command=setEndTime, font=("Tahoma 9 bold"))
buttonEnd.place(x=350,y=430, height = 50, width = 100)

## Entry box
entryTaskName=tk.Entry(canvas)
entryTaskName.place(x=250, y=380, height = 30, width = 150)

labelTaskName=tk.Label(canvas, text="Enter task name:", bg="#404040", fg="white", font=("Tahoma", 12), justify="left")
labelTaskName.place(x=100, y=380, height = 30, width = 150)

## show status
statusInfo=StringVar()
statusInfo.set('Waiting for task name...')
labelStatus=tk.Label(canvas, textvariable=statusInfo, bg="#404040", fg="white", font=("Tahoma", 12), justify="center")
labelStatus.place(x=150, y=340, height = 30, width = 200)

##show data from file
frameTasks=tk.Frame(canvas, height=320, width=483, bg ="#595959")
frameTasks.place(x=10, y=10)


root.mainloop()