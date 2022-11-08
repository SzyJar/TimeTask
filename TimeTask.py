from datetime import datetime, timedelta
import tkinter as tk
from tkinter import StringVar, messagebox
import csv as csv

startTime = 0
endTime = 0
taskOngoing = 0
taskName = ''
newFileMessage = 0
editWindowIsOpen = 0
## Open data file if exists, if not then make new data file
try:
    with open('savedTasks.csv', newline='') as file:
        reader = csv.reader(file, delimiter=";")
except:
    with open('savedTasks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
    newFileMessage = 1

## Set task name
def setTaskName():
    global taskName
    taskName = entryTaskName.get()
    if taskName !='':
        statusInfo.set('Current task name: '+ taskName)
    else:
        statusInfo.set('Waiting for task name...')

## Get start time
def setStartTime():
    if taskName != "":
        global startTime
        startTime = datetime.now()
        global taskOngoing
        taskOngoing = 1
        root.title("TimeTask (Current task running: "+taskName+")")
    else:
        messagebox.showwarning("No task name", "Please set task name before starting task time counter.")

## Get task time and write it to data file
def setEndTime():
    global endTime
    endTime = datetime.now()
    global taskOngoing
    if taskOngoing == 1:
        taskOngoing = 0
        root.title("TimeTask (Idle - no task running)")
        global taskTime    
        taskTime = endTime - startTime
        with open('savedTasks.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([taskTime, taskName])
        getTask()

## List all tasks found in data file
def getTask():
    listTasks.delete(0,'end')
    taskHolderTime = [datetime.now()-datetime.now()]
    taskDataDate = datetime.now()-datetime.now()
    taskHolderName = []
    ## Read exisitng tasks
    with open('savedTasks.csv', newline='') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            taskData=''.join(row)
            taskDataName = taskData[14:]
            taskDataDate = timedelta(hours=int(taskData[:1]), minutes=int(taskData[2:4]), seconds=int(taskData[5:7]))
            match=0
            for i in range(len(taskHolderName)):
                if taskHolderName[i] == taskDataName:
                    taskHolderTime[i] = taskHolderTime[i]+taskDataDate
                    match=1
                    break
            if match == 0:
                taskHolderName.append(taskDataName)
                taskHolderTime.append(taskDataDate)
            listTasks.delete(0,'end')
            ## List tasks
            for i in range(len(taskHolderName)):
                stringList = "Task: "+str(taskHolderName[i])+"\t Time: \t"+str(taskHolderTime[i])
                listTasks.insert('end', stringList)
   
## Get task name from program list
def getName():
    if listTasks.curselection() !=():
        record = 0
        name =''
        for char in listTasks.get(listTasks.curselection()):
            if char  =='\t':
                break
            if record == 1:
                name = name+char
            if char==' ' and record != 1:
                record=1
        return(name)

## Record deletion
def deleteRecord():
    if listTasks.curselection() !=():
        nameToDel = getName()
        recordList=[]
        newList=[]       
        with open('savedTasks.csv', newline='') as file:
            eraser = csv.reader(file, delimiter=";")
            for row in eraser:
                recordList.append(row)
        for i in range(len(recordList)):
            if recordList[i][1] != nameToDel:
                newList.append(recordList[i])
        with open('savedTasks.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for i in range(len(newList)):
                writer.writerow([newList[i][0], newList[i][1]])
        getTask()

## Edit time
def editTask():
    if listTasks.curselection() !=():
        global editName
        editName = getName()
        global editWindowIsOpen
        if editWindowIsOpen == 0:
            global editWindow
            editWindow = tk.Toplevel(root)
            editWindow.title("Edit task time")
            editWindow.protocol('WM_DELETE_WINDOW', lambda: closeWindow(editWindow))
            editCanvas = tk.Canvas(editWindow, height=150, width=310, bg ="#404040").pack()
            labelText=StringVar()
            labelText.set("Add time to: "+str(editName)+" [mm:ss]")
            labelEdit=tk.Label(editWindow, textvariable=labelText, bg="#404040", fg="white", font=("Tahoma", 12), justify="center")
            labelEdit.place(x=5, y=20, height = 30, width = 300)

            global entryEdit_M
            entryEdit_M=tk.Entry(editWindow, justify="center")
            entryEdit_M.place(x=100, y=50, height = 30, width = 50)
            entryEdit_M.insert(0,'00')
            global entryEdit_S
            entryEdit_S=tk.Entry(editWindow, justify="center")
            entryEdit_S.place(x=160, y=50, height = 30, width = 50)
            entryEdit_S.insert(0,'00')

            buttonEditApply=tk.Button(editWindow, text="Add time", font=("Tahoma 9 bold"), command=lambda: applyChange())
            buttonEditApply.place(x=105,y=90, height = 50, width = 100)
            editWindowIsOpen = 1

def applyChange():
    try:
        taskMinute = int(entryEdit_M.get())
        taskSecond = int(entryEdit_S.get())
        if taskMinute>59:
            taskMinute = 59
            entryEdit_M.delete(0, 'end')
            entryEdit_M.insert(0, '59')
        if taskSecond>59:
            taskSecond = 59
            entryEdit_S.delete(0, 'end')
            entryEdit_S.insert(0, '59')
        if taskMinute<0:
            taskMinute = 0
            entryEdit_M.delete(0, 'end')
            entryEdit_M.insert(0, '0')
        if taskSecond<0:
            taskSecond = 0
            entryEdit_S.delete(0, 'end')
            entryEdit_S.insert(0, '0')
        taskTimeEdit=timedelta(hours=0, minutes=taskMinute, seconds=taskSecond, microseconds=1)
        with open('savedTasks.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([taskTimeEdit, editName])
        getTask()
    except:
        entryEdit_M.delete(0, 'end')
        entryEdit_S.delete(0, 'end')
        labelInput=tk.Label(editWindow, text="Unable to process input", bg="#404040", fg="#ffcccc", font=("Tahoma", 9), justify="center")
        labelInput.place(x=5, y=8, height = 15, width = 300)

def closeWindow(window):
    global editWindowIsOpen
    editWindowIsOpen = 0
    window.destroy()

#### GUI
root = tk.Tk()
root.title("TimeTask (Idle - no task running)")
root.resizable(width=False, height=False)

canvas = tk.Canvas(root, height=500, width=500, bg ="#404040").pack()

## Buttons
buttonStart=tk.Button(canvas, text="Start task", command=setStartTime, font=("Tahoma 9 bold"))
buttonStart.place(x=50,y=430, height = 50, width = 100)

buttonSet=tk.Button(canvas, text="Set task name", command=setTaskName, font=("Tahoma 9 bold"))
buttonSet.place(x=200,y=430, height = 50, width = 100)

buttonEnd=tk.Button(canvas, text="End task", command=setEndTime, font=("Tahoma 9 bold"))
buttonEnd.place(x=350,y=430, height = 50, width = 100)

## Entry box
entryTaskName=tk.Entry(canvas, justify="center")
entryTaskName.place(x=250, y=380, height = 30, width = 150)

labelTaskName=tk.Label(canvas, text="Enter task name:", bg="#404040", fg="white", font=("Tahoma", 12), justify="left")
labelTaskName.place(x=100, y=380, height = 30, width = 150)

## Show status
statusInfo=StringVar()
statusInfo.set('Waiting for task name...')
labelStatus=tk.Label(canvas, textvariable=statusInfo, bg="#404040", fg="white", font=("Tahoma", 12), justify="center")
labelStatus.place(x=50, y=340, height = 30, width = 400)

## Show data from file
frameTasks=tk.Frame(canvas, height=320, width=485, bg ="#595959")
frameTasks.place(x=10, y=10)

refreshImage=tk.PhotoImage(file=r"refresh.png")
buttonRefresh=tk.Button(frameTasks, image=refreshImage, bg="#ffffff", command=getTask)
buttonRefresh.place(x=5,y=3, height = 27, width = 27)
listTasks=tk.Listbox(frameTasks, bg ="#595959", fg="white", height=19, width=50, font=("Tahoma 14"), selectmode="single", relief="solid")
listTasks.place(x=-2, y=30)

## Delete record
buttonRecord=tk.Button(frameTasks, text="Delete task", command=deleteRecord, font=("Tahoma 9"))
buttonRecord.place(x=380,y=3, height = 27, width = 100)

## Edit Task time
buttonEdit=tk.Button(frameTasks, text="Edit task", command=editTask, font=("Tahoma 9"))
buttonEdit.place(x=270,y=3, height = 27, width = 100)

## New data file message
if newFileMessage == 1:
    messagebox.showinfo("New data file has been created", "Unable to find existing data file, new data file has been created")

getTask()
root.mainloop()