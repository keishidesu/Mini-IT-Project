import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import font
from tkinter.constants import *
import random
import datetime
import json

def clear_frame():
    for widget in tk.winfo_children():
        widget.destroy()

def initStorage():
    global usernames
    usernames = ["admin2019"]
    global passwords
    passwords = ["iamadmin"]
    global hour
    hour = datetime.datetime.now().minute
    global parkings
    parkings = [0,1,2,3,4,5]
    global rates
    rates = [2,3,4,5,6,7]
    global malls
    malls = ["Midvalley", "Dpulze", "Sunway Pymarid", "One Utama Mall", "IOI City Mall", "Pavillion"]
    global numSpace
    numSpace = [680,260,530,600,480,340]
    
    try:
        open("parkings.txt")
    except IOError:
        print("File not found, Creating one")
        print("Generating malls parking data")
        for mallid in range(0, len(malls)):
            parkings[mallid] = []
            for x in range(0, numSpace[mallid]):
                parkings[mallid].append(random.randint(0,3))
        file = open("parkings.txt", "w")
        data = [usernames, passwords, rates, hour, parkings]
        json.dump(data, file)
    else:
        file = open("parkings.txt", "r")
        print("File found! Loading data from file")
        data = json.load(file)
        usernames = data[0]
        passwords = data[1]
        rates = data[2]
        hour = data[3]
        parkings = data[4]

def saveStorage():
    file = open("parkings.txt", "w")
    data = [usernames, passwords, rates, hour, parkings]
    json.dump(data, file)

def authentication():
    clear_frame()
    
    Label(tk, text="\nCAR PARK FINDER 2019\n",font="Helvetica 20 bold").pack()
    Label(tk, text="AUTHENTICATION\n",font="Helvetica 15").pack()
    nameLabel = Label(tk, text="Username").pack()
    nameEntry = Entry(tk)
    nameEntry.pack()

    passwordLabel = Label(tk, text="Password").pack()
    passwordEntry = Entry(tk, show="*")
    passwordEntry.pack()

    Label(tk, text="").pack()
    loginButton = Button(tk, width=15, text="Login", command=lambda: checkLogin(nameEntry, passwordEntry))
    loginButton.pack()

    regLabel = Label(tk, text="\nDon't have an account?")
    regLabel.pack()

    regButton = Button(tk, width=15, text="Register", command=register)
    regButton.pack()

def register():
    clear_frame()
    Label(tk, text="\nREGISTRATION\n", font="Helvatica 15").pack()
    Label(tk, text="Enter your credentials here!\n").pack()
    
    nameLabel = Label(tk, text="Username").pack()
    nameEntry = Entry(tk)
    nameEntry.pack()

    passwordLabel = Label(tk, text="Password").pack()
    passwordEntry = Entry(tk, show="*")
    passwordEntry.pack()

    reconfirmLabel = Label(tk, text="Reconfirm Password").pack()
    reconfirmEntry = Entry(tk, show="*")
    reconfirmEntry.pack()

    regButton = Button(tk, width=15, text="Register!", command=lambda: checkRegister(nameEntry, passwordEntry, reconfirmEntry))
    regButton.pack(pady=10)

    cancelButton = Button(tk, width=15, text="Cancel", command=authentication)
    cancelButton.pack()

def checkRegister(nameEntry, passwordEntry, reconfirmEntry):
    username = nameEntry.get()
    password = passwordEntry.get()
    reconfirm = reconfirmEntry.get()
    if username == "" :
        messagebox.showinfo("Error", "Please enter a username!")
    elif password == "" :
        messagebox.showinfo("Error", "Please enter a password!")
    elif reconfirm == "":
        messagebox.showinfo("Error", "Please re-enter your password!")
    else:
        error = 0
        for u in usernames:
            if username == u:
                messagebox.showinfo("Error", "The name is already taken!")
                error = 1
                break
        if error == 0 and (len(password) < 8 or len(password) > 16):
            messagebox.showinfo("Error", "Your password must be between 8-16 characters!")
            reconfirmEntry.delete(0,END)
            error = 1
        if error == 0 and password != reconfirm:
            messagebox.showinfo("Error", "Your password does not match! Make sure you re-enter correctly!")
            reconfirmEntry.delete(0,END)
            error = 1
        if error == 0:
            usernames.append(username)
            passwords.append(password)
            saveStorage()
            messagebox.showinfo("Registration", "Register Successful!")
            authentication()

def checkLogin(nameEntry, passwordEntry):
    username = nameEntry.get()
    password = passwordEntry.get()
    if(username == ""):
        messagebox.showinfo("Error", "Please enter a username!")
    elif(password == ""):
        messagebox.showinfo("Error", "Please enter a password!")
    else:
        error = 1
        for ukey in range(0, len(usernames)):
            if(username == usernames[ukey]):
                if(password == passwords[ukey]):
                    messagebox.showinfo("Authentication", "Login Successful!")
                    global isAdmin
                    if(username == "admin2019"):
                        isAdmin = True
                    else:
                        isAdmin = False
                    mainMenu()
                    error = 0
                    break
        if error == 1:
            messagebox.showinfo("Error", "Username or Password is incorrect!")

def mainMenu():

    clear_frame()
    Label(tk, text="\nMAIN MENU\n").pack()
    Label(tk, text="Select a mall!", font="Helvatica 15").pack()
    frame = Frame(tk)
    bottomFrame = Frame(tk)
    frame.pack()
    bottomFrame.pack(pady=10)
    Button(frame, text=malls[0], width=15, command=lambda: showParkings(0)).grid(row=1, column=0, padx=10)
    Button(frame, text=malls[1], width=15, command=lambda: showParkings(1)).grid(row=1, column=1)
    Button(frame, text=malls[2], width=15, command=lambda: showParkings(2)).grid(row=2, column=0, pady=10)
    Button(frame, text=malls[3], width=15, command=lambda: showParkings(3)).grid(row=2, column=1)
    Button(frame, text=malls[4], width=15, command=lambda: showParkings(4)).grid(row=3, column=0)
    Button(frame, text=malls[5], width=15, command=lambda: showParkings(5)).grid(row=3, column=1)
    if isAdmin == True:
        Button(bottomFrame, text="Settings", width=15, command=showSettings).pack(pady=10)
    
    Button(bottomFrame, text="Logout", width=15, command=confirmLogout).pack()

def _on_mousewheel(event):
    canvas.yview_scroll(-1*(event.delta//120), "units")

def showParkings(mallid):
    clear_frame()
    
    reloadParkings(mallid)
    
    Label(tk, text=malls[mallid] + "\n").pack()

    topFrame = Frame(tk)

    Button(topFrame, width=15, text="Back", command=mainMenu).grid(column=1, row=0, padx=50)

    Button(topFrame, width=15, text="Refresh", command=lambda: reloadParkings(mallid)).grid(column=2, row=0)

    Button(topFrame, width=15, text="Calculate Fee", command=lambda: feeCalculation(mallid)).grid(column=3, row=0, padx=50)

    topFrame.pack(pady=10)
    
    parkSpaces = numSpace[mallid]
    mallParkings = parkings[mallid]
    global canvas
    canvas = Canvas(tk, height=1000, width=1053)

    canvas.focus_set()
    canvas.bind("<MouseWheel>", _on_mousewheel)

    vbar = Scrollbar(tk, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas.yview)

    hbar = Scrollbar(tk, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canvas.xview)

    canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
    
    count = 0
    column = 0
    row = 0
    x1 = 10
    y1 = 10
    x2 = 60
    y2 = 80
    difx = 0
    dify = 0
    for x in range(0, parkSpaces):
        if count >= 10:
            difx += 50
            count = 0
            column += 1
        if column > 1:
            row += 1
            dify += 70
            difx= 0
            column = 0
        if row > 1:
            dify += 70
            row = 0
        if mallParkings[x] > 0:
            canvas.create_rectangle(x1 + difx, y1 + dify, x2 + difx, y2 + dify, fill="red")
            canvas.create_text(x1 + difx + 10, y1 + dify + 10, text=mallParkings[x])
        else:
            canvas.create_rectangle(x1 + difx, y1 + dify, x2 + difx, y2 + dify, fill="green")
        count += 1
        difx += 50
    canvas.config(scrollregion=canvas.bbox(ALL))
    canvas.pack(expand=True)

def reloadParkings(mid):
    global hour
    currentHour = datetime.datetime.now().minute
    if currentHour != hour:  
        mallid = 0
        for mallParking in parkings:
            parkid = 0
            for parkhr in mallParking:
                if parkhr > 0:
                    parkings[mallid][parkid] -= 1
                elif parkhr == 0:
                    parkings[mallid][parkid] = random.randint(0,3)
                parkid += 1
            mallid += 1
        hour = currentHour
        file = open("parkings.txt", "w")
        data = [usernames, passwords, rates, hour, parkings]
        json.dump(data, file)
        showParkings(mid)

def calculateFee(parkEntry, mallid):
    try:
        hour = int(parkEntry.get())
    except ValueError:
        messagebox.showinfo("Error", "You can only enter integer!")
        parkEntry.delete(0, END)
    else:
        rate = rates[mallid]
        total_fee = hour * rate
        messagebox.showinfo("Calculation", "Your parking fee at " + malls[mallid] + " is RM" + str(total_fee))
        feeCalculation(mallid)

def feeCalculation(mallid):
    clear_frame()
    Label(tk, text= "\nCALCULATE PARKING FEE", font="Helvatica 15").pack()
    Label(tk, text="\n" + malls[mallid]).pack()
    Label(tk, text= "\nParking fee per hour is RM" + str(rates[mallid]) + " ").pack()
    Label(tk, text= "\nPlease enter how many hours will you be parking\n").pack()

    parkEntry = Entry(tk)
    parkEntry.pack()

    Button(tk, text="Calculate", width=15, command=lambda: calculateFee(parkEntry, mallid)).pack(pady=10)

    Button(tk, text="Back", width=15, command=lambda: showParkings(mallid)).pack()

#admin
def showSettings():
    clear_frame()
    Label(tk, text="\nSETTINGS", font="Helvatica 15").pack()
    Label(tk, text="Select a mall you want to change the rates of:\n").pack()
    Button(tk, text=malls[0], width=15, command=lambda: changeRate(0)).pack()
    Button(tk, text=malls[1], width=15, command=lambda: changeRate(1)).pack()
    Button(tk, text=malls[2], width=15, command=lambda: changeRate(2)).pack()
    Button(tk, text=malls[3], width=15, command=lambda: changeRate(3)).pack()
    Button(tk, text=malls[4], width=15, command=lambda: changeRate(4)).pack()
    Button(tk, text=malls[5], width=15, command=lambda: changeRate(5)).pack()
    Label(tk, text="").pack()

    backButton = Button(tk, text="Back", width=15, command=mainMenu).pack()

def changeRate(mallid):
    clear_frame()
    currentRate = rates[mallid]
    Label(tk, text="SETTINGS").pack()
    Label(tk, text="Current rate for " + malls[mallid] + " is RM" + str(currentRate)).pack()
    Label(tk, text="Change to: ").pack()

    rateEntry = Entry(tk)
    rateEntry.pack()
    
    applyButton = Button(tk, width=15, text="Apply", command=lambda: saveRate(rateEntry, mallid)).pack(pady=10)
    backButton = Button(tk, width=15, text="Back", command=showSettings).pack()

def saveRate(rateEntry, mallid):
    try:
        newRate = int(rateEntry.get())
    except ValueError:
        messagebox.showinfo("Error", "You can only enter integer!")
        rateEntry.delete(0, END)
    else:
        if newRate > 50:
            messagebox.showinfo("Error", "Maximum rate is RM50!")
            rateEntry.delete(0, END)
        else:            
            messagebox.showinfo("Settings", "You succesfully updated rates!")
            rates[mallid] = newRate
            saveStorage()
            changeRate(mallid)

def confirmLogout():
    if messagebox.askyesno("Logout", "Are you sure?"):
        authentication()

tk = tkinter.Tk()
tk.title("Car Park Finder 2019")
tk.geometry("700x500")
tk.option_add("*Font","Helvetica")

initStorage()
authentication()

tk.mainloop()
