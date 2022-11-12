from datetime import datetime, timedelta
import tkinter as tk
from tkinter import StringVar, messagebox
import csv as csv

class Database:
    def __init__(self):
        self.fileName = "savedTasks.csv"
        self.startTime = 0
        self.taskOngoing = 0
        self.taskName = ''
        self.editWindowIsOpen = 0
    
    # Set database file
    def currentFileSet(self, fileName):
        self.fileName = fileName
        try:
            with open(self.fileName, newline='') as file:
                reader = csv.reader(file, delimiter=";")
                return(0)
        except:
            with open(self.fileName, 'w', newline='') as file:
                writer = csv.writer(file)
                return(1)

    # Get data from database file
    def getTasks(self):
        taskHolderName = []
        taskHolderTime = []
        with open(self.fileName, newline='') as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                taskData=''.join(row)
                taskName = taskData[14:]
                taskTime = timedelta(hours=int(taskData[:1]), minutes=int(taskData[2:4]), seconds=int(taskData[5:7]))
                match=0
                for i in range(len(taskHolderName)):
                    if taskHolderName[i] == taskName:
                        taskHolderTime[i] = taskHolderTime[i]+taskTime
                        match=1
                        break
                if match == 0:
                    taskHolderName.append(taskName)
                    taskHolderTime.append(taskTime)
                listTasks.delete(0,'end')
                ## List tasks
                for i in range(len(taskHolderName)):
                    stringList = "Task: "+str(taskHolderName[i])+"\t Time: \t"+str(taskHolderTime[i])
                    listTasks.insert('end', stringList)                

    ## Set task name
    def setTaskName(self, taskName):
        self.taskName = taskName
        if self.taskName !='':
            return('Current task name: '+ self.taskName)
        else:
            return('Waiting for task name...')

    ## Get start time
    def setStartTime(self):
        if self.taskName != "":
            self.startTime = datetime.now()
            self.taskOngoing = 1

    ## Get task time and write it to data file
    def setEndTime(self):
        endTime = datetime.now()
        if self.taskOngoing == 1:
            self.taskOngoing = 0
            taskTime = endTime - self.startTime
            with open(self.fileName, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([taskTime, self.taskName])

    ## Get task name from program list
    def getName(self, listSelection):
        if listSelection !='':
            record = 0
            name =''
            for char in listSelection:
                if char  =='\t':
                    break
                if record == 1:
                    name = name+char
                if char==' ' and record != 1:
                    record=1
            return(name)

    ## Record deletion
    def deleteRecord(self, listSelection):
        if  listSelection != '':
            nameToDel = self.getName(listSelection)
            recordList=[]
            newList=[]       
            with open(self.fileName, newline='') as file:
                eraser = csv.reader(file, delimiter=";")
                for row in eraser:
                    recordList.append(row)
            for i in range(len(recordList)):
                if recordList[i][1] != nameToDel:
                    newList.append(recordList[i])
            with open(self.fileName, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=";")
                for i in range(len(newList)):
                    writer.writerow([newList[i][0], newList[i][1]])

    ## Edit time
    def editTask(self, listSelection):
        if listSelection !='':
            self.editName = self.getName(listSelection)
            if self.editWindowIsOpen == 0:
                self.editWindow = tk.Toplevel(root)
                self.editWindow.title("Edit task time")
                self.editWindow.protocol('WM_DELETE_WINDOW', lambda: self.closeWindow(self.editWindow))
                editCanvas = tk.Canvas(self.editWindow, height=150, width=310, bg ="#404040").pack()
                labelText=StringVar()
                labelText.set("Add time to: "+str(self.editName)+" [mm:ss]")
                labelEdit=tk.Label(self.editWindow, textvariable=labelText, bg="#404040", fg="white", font=("Tahoma", 12), justify="center")
                labelEdit.place(x=5, y=20, height = 30, width = 300)

                self.entryEdit_M=tk.Entry(self.editWindow, justify="center")
                self.entryEdit_M.place(x=100, y=50, height = 30, width = 50)
                self.entryEdit_M.insert(0,'00')

                self.entryEdit_S=tk.Entry(self.editWindow, justify="center")
                self.entryEdit_S.place(x=160, y=50, height = 30, width = 50)
                self.entryEdit_S.insert(0,'00')

                buttonEditApply=tk.Button(self.editWindow, text="Add time", font=("Tahoma 9 bold"), command=lambda:
                 [self.applyChange(), self.getTasks()])
                buttonEditApply.place(x=105,y=90, height = 50, width = 100)
                self.editWindowIsOpen = 1

    def applyChange(self):
        try:
            taskMinute = int(self.entryEdit_M.get())
            taskSecond = int(self.entryEdit_S.get())
            if taskMinute>59:
                taskMinute = 59
                self.entryEdit_M.delete(0, 'end')
                self.entryEdit_M.insert(0, '59')
            if taskSecond>59:
                taskSecond = 59
                self.entryEdit_S.delete(0, 'end')
                self.entryEdit_S.insert(0, '59')
            if taskMinute<0:
                taskMinute = 0
                self.entryEdit_M.delete(0, 'end')
                self.entryEdit_M.insert(0, '0')
            if taskSecond<0:
                taskSecond = 0
                self.entryEdit_S.delete(0, 'end')
                self.entryEdit_S.insert(0, '0')
            taskTimeEdit=timedelta(hours=0, minutes=taskMinute, seconds=taskSecond, microseconds=1)
            with open(self.fileName, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([taskTimeEdit, self.editName])
        except:
            self.entryEdit_M.delete(0, 'end')
            self.entryEdit_S.delete(0, 'end')
            labelInput=tk.Label(self.editWindow, text="Unable to process input", bg="#404040", fg="#ffcccc", font=("Tahoma", 9), justify="center")
            labelInput.place(x=5, y=8, height = 15, width = 300)

    def closeWindow(self, window):
        self.editWindowIsOpen = 0
        window.destroy()

###

def noNameMessage():
    if data.taskOngoing == 0:
        messagebox.showwarning("No task name", "Please set task name before starting task time counter.")

def windowName():
    if data.taskOngoing == 0:
        root.title("TimeTask (Idle - no task running)")
    else:
        root.title("TimeTask (Current task running: "+data.taskName+")")

data = Database()

#### GUI
root = tk.Tk()
root.title("TimeTask (Idle - no task running)")
root.resizable(width=False, height=False)
canvas = tk.Canvas(root, height=500, width=500, bg ="#404040").pack()

## Buttons
buttonStart=tk.Button(canvas, text="Start task", font=("Tahoma 9 bold"), command=lambda:
 [data.setStartTime(), noNameMessage(), windowName()])
buttonStart.place(x=50,y=430, height = 50, width = 100)

buttonSet=tk.Button(canvas, text="Set task name", font=("Tahoma 9 bold"), command=lambda:
 statusInfo.set(data.setTaskName(entryTaskName.get())))
buttonSet.place(x=200,y=430, height = 50, width = 100)

buttonEnd=tk.Button(canvas, text="End task", font=("Tahoma 9 bold"), command=lambda:
 [data.setEndTime(), windowName(), data.getTasks()])
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

## List with tasks from data file
frameTasks=tk.Frame(canvas, height=320, width=485, bg ="#595959")
frameTasks.place(x=10, y=10)

listTasks=tk.Listbox(frameTasks, bg ="#595959", fg="white", height=19, width=50, font=("Tahoma 14"), selectmode="single", relief="solid")
listTasks.place(x=-2, y=30)

## Delete record
buttonRecord=tk.Button(frameTasks, text="Delete task", font=("Tahoma 9"), command=lambda:
 [data.deleteRecord(listTasks.get(listTasks.curselection())), data.getTasks()])
buttonRecord.place(x=380,y=3, height = 27, width = 100)

## Edit Task time
buttonEdit=tk.Button(frameTasks, text="Edit task", font=("Tahoma 9"), command=lambda:
 [data.editTask(listTasks.get(listTasks.curselection()))])
buttonEdit.place(x=270,y=3, height = 27, width = 100)

if data.currentFileSet("savedTasks.csv") == 1:
    messagebox.showinfo("New data file has been created", "Unable to find existing data file, new data file has been created")

data.getTasks()
root.mainloop()