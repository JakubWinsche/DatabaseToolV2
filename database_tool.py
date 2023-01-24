from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import sqlite3
import os
import pyperclip as pc
import shutil
import sys

databases = []
textboxColour = 'linen'

def dbTableFormat(info, body):
    columnWidths = []
    headings = []
    
    for row in info:
        headings.append(row[0])
        columnWidths.append(len(row[0]))

    for row in body:
        counter = 0
        for item in row:
            length = len(str(item))
            if length > columnWidths[counter]:
                columnWidths[counter] = length
            counter = counter + 1
        
    topRow = '+'
    headingText = '| '
    bodyText = '| '
    for width in columnWidths:
        topRow = topRow + '-' * (width+3)
    topRow = topRow[:-1] + '+\n'
    
    counter = 0
    for item in headings:
        padding = ' ' * (columnWidths[counter] - len(str(item)))
        headingText = headingText + item + padding + ' | '
        counter = counter + 1
    headingText = headingText + '\n'

    for row in body:
        counter = 0
        for item in row:
            padding = ' ' * (columnWidths[counter] - len(str(item)))
            bodyText = bodyText + str(item) + padding + ' | '
            counter = counter + 1
        bodyText = bodyText + '\n| '
    bodyText = bodyText[:-2]
        
    text = topRow + headingText + topRow + bodyText + topRow
    return text

def updateDatabases():
    numberOfDbs = 0

    for db in os.listdir():
        print(db)
        if db != 'databases':
            files = os.listdir()
        else:
            files = os.listdir('databases')
    for file in files:
        if file[-3:] == '.db':
            databases.append(file)

def buildDatabase():
    global var
    global currentDatabase
    global dbDropdown
    global dbNameTextbox

    root = tkinter.Tk()

    try:
        root.withdraw()
        name = simpledialog.askstring(title = 'Create Database', prompt = 'What do you want to call your database?')

    except:
        if name != None:
            if name == '':
                outputTextbox.insert(END, 'ERROR: There was no input.')
            else:
                outputTextbox.insert(END, f'ERROR: Unknown error has occured.')

    dbName = name + '.db'

    if dbName == '.db':
        outputTextbox.insert(END, 'ERROR: Please enter a name for your new database.\n\n')

    elif dbName in databases:
        outputTextbox.insert(END, 'ERROR: Database already exists.\n\n')
    else:
        try:
            with sqlite3.connect(dbName) as db:
                cursor = db.cursor()
                outputTextbox.insert(END, f'Successfully created database {dbName[:-3]}.\n\n')
        except:
            outputTextbox.insert(END, 'ERROR: Please try again.\n\n')
        else:
            databases.append(dbName)
            currentDatabase = dbName
            window.title(f'Python Database Tool: Currently in {currentDatabase}')
            mb = menubar()
            mb.createMenubar()

def chooseDatabase(table):
    global currentDatabase
    currentDatabase = table
    outputTextbox.insert(END, f'You are currently in: {currentDatabase}\n\n')
    window.title(f'Python Database Tool: Currently in {currentDatabase}')

def deleteDatabase(table):
    clear = tkinter.messagebox.askquestion('Delete', f'Are you sure you want to delete {table[:-3]}?\n\n')
    if clear == 'yes':
        os.remove(table)
        currentDatabase = ''
        window.title('Python Database Tool')
        mb = menubar()
        mb.createMenubar()

    
def clearOutput():
    clear = tkinter.messagebox.askquestion('Clear', 'Are you sure you want to clear the output table?')
    if clear == 'yes':
        outputTextbox.delete(0.0, END) 

def getTables():
    if currentDatabase == '':
        if os.listdir() == []:
            outputTextbox.insert(END, 'ERROR: Please create a database.\n\n')
        else:
            outputTextbox.insert(END, 'ERROR: Please choose a database.\n\n')
    else:
        query = '''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;'''
        runSql(query)

def quitTool():
    quit = tkinter.messagebox.askquestion('Quit', 'Are you sure you want to quit?')
    if quit == 'yes':
        window.withdraw()
        window.quit()

def helpS(i):
    win = Tk() 

    win.geometry("250x170") 

    T = Text(win, height = 6, width = 53) 

    l = Label(win, text = "How to do XYZ: ") 
    l.config(font =("Courier", 14)) 

    Quote = ['''words on a screen''', 'kys']

    b1 = Button(win, text = "Next", command = lambda: helpS(i + 1))
    print(i)

    b2 = Button(win, text = "Exit", command = win.destroy) 

    l.pack() 
    T.pack() 
    b1.pack() 
    b2.pack() 

    T.insert(tkinter.END, Quote[i]) 

    tkinter.mainloop()

def runQuery():
    if currentDatabase == '':
        if os.listdir() == []:
            outputTextbox.insert(END, 'ERROR: Please create a database.\n\n')
        else:
            outputTextbox.insert(END, 'ERROR: Please choose a database.\n\n')
    else:
        query = sqlTextbox.get(0.0, END)
        runSql(query)
        outputTextbox.insert(END, 'Successfully ran the command.\n\n')

def runSql(sql):
    with sqlite3.connect(currentDatabase) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        
        result = cursor.fetchall()
        if sql[:6].upper() == 'SELECT':
            tableInfo = cursor.description
            result = dbTableFormat(tableInfo, result)
        else:
            result = str(result)
            
        result = result + '\n\n'
        outputTextbox.insert(END, result)

def listItems():
    root = tkinter.Tk()

    try:
        root.withdraw()
        userInp = simpledialog.askstring(title = 'View Items', prompt = 'Which table do you want to view:')
        runSql(f'''SELECT * FROM {userInp}''')

    except:
        if userInp != None:
            if userInp == '':
                outputTextbox.insert(END, 'There was no input.\n\n')
            else:
                outputTextbox.insert(END, f'There is no such table as {userInp}.\n\n')

def about():
    messagebox.showinfo('Database Tool', f'Database Tool\n\n\n\nVersion: 2.1.1 (console setup)\nCommit: 86a97cd\nDate: 2023-01-22 T10:05\nPip: 3.10.9\nOS: {sys.platform}\nSandboxed: No\nLicense: GNU General Public License v3.0\nCreated by: Jakub Winczewski')

def darkMode():
    mb = darkmode.get()

    if mb == 1:
        window.config(background = '#282A3A')
        sqlTextbox = Text(frameQuery, width = 50, height = 20, background = 'lightgray')
        sqlTextbox.grid(row = 1, column = 0, sticky = NW)

        outputTextbox = ScrolledText(frameOutput, width = 65, height = 20, background = 'lightgray')
        outputTextbox.grid(row = 1, column = 0, sticky = NW)

    elif mb == 0: 
        window.config(background = 'SystemButtonFace')
        sqlTextbox = Text(frameQuery, width = 50, height = 20, background = textboxColour)
        sqlTextbox.grid(row = 1, column = 0, sticky = NW)

        outputTextbox = ScrolledText(frameOutput, width = 65, height = 20, background = textboxColour)
        outputTextbox.grid(row = 1, column = 0, sticky = NW)
    else:
        outputTextbox.insert(END, 'ERROR: Something went wrong!\n\n')

def copy():
    pc.copy(sqlTextbox.get(0.0, END))

def paste():
    sqlTextbox.insert(END, f'{pc.paste()}')

def cut():
    pc.copy(sqlTextbox.get(0.0, END))
    sqlTextbox.delete('1.0', END)


def open():
    Tk().withdraw()
    filename = str(askopenfilename())
    print(f'{os.getcwd()}/databases')
    try:
        if filename[-3:] == '.db':
            shutil.move(filename, f'{os.getcwd()}')
            mb = menubar()
            mb.createMenubar()
            
        elif filename != '':
            outputTextbox.insert(END, f'ERROR: This is not a database file.\n\n')

    except:
        outputTextbox.insert(END, f'ERROR: This file is already in the databases folder.\n\n')

def enterMode():
    em = entermode.get()
    if em == True:
        sqlTextbox.bind('<Return>', lambda enter: runQuery())
    else:
        sqlTextbox.unbind('<Return>')

def rWorkspace():
    reset = tkinter.messagebox.askquestion('Reset', 'Are you sure you want to reset your workspace?\n(NOTE: This action will delete all files and cannot be undone)')
    if reset == 'yes':
        try:
            files = os.listdir('../databases')
            print('fileS:', files)
            for file in files:
                os.remove(file)
            sqlTextbox.delete(0.0, END)
            outputTextbox.delete(0.0, END)
            outputTextbox.insert(END, 'Workspace reset successfull.\n\n')

        except:
            outputTextbox.insert(END, f'ERROR: System was unable to perform this action: \nCheck permissions and try again.\n\n') 

# ----------------------------------------------------------------- Main Code -----------------------------------------------------------------

window = Tk()
window.title('Python Database Tool')

darkmode = BooleanVar()
darkmode.set(False)
entermode = BooleanVar()
entermode.set(False)

pythonLogo = PhotoImage(file = 'python-logo.gif')
sqliteLogo = PhotoImage(file = 'sqlite-logo.gif')

if not os.path.isdir('databases'):
    os.makedirs('databases')

updateDatabases()    
os.chdir('databases')

frameQuery = Frame(window)
frameQuery.grid(row = 2, column = 0, sticky = NW)

frameOutput = Frame(window)
frameOutput.grid(row = 2, column = 1, rowspan = 2)

Label(frameQuery, text = 'Add SQL:').grid(row = 0, column = 0, sticky = NW)
Label(frameOutput, text = 'Output: ').grid(row = 0, column = 0, sticky = NW)

sqlTextbox = Text(frameQuery, width = 50, height = 20, background = textboxColour)
sqlTextbox.grid(row = 1, column = 0, sticky = NW)



outputTextbox = ScrolledText(frameOutput, width = 65, height = 20, background = textboxColour)
outputTextbox.grid(row = 1, column = 0, sticky = NW)

Label(window, image = pythonLogo).grid(row = 1, column = 0, sticky = NW)
Label(window, image = sqliteLogo).grid(row = 1, column = 1, sticky = NW)

button_clear = Button(frameOutput, text = "Clear result box", command = clearOutput)
button_clear.grid(row = 2, column = 0, sticky = NE)
button_run = Button(frameQuery, text = "Run SQL", width = 10, command = runQuery)
button_run.grid(row = 2, column = 0, sticky = NW)


class menubar:
    def createMenubar(self):
        global darkmode
        global view
        global entermode

        menubar = Menu(window, background = '#ff8000', foreground = 'black', activebackground = 'white', activeforeground = 'black')  
        file = Menu(menubar, tearoff = 0)  
        file.add_command(label = 'New', command = buildDatabase)  
        file.add_command(label = 'Open', command = open)  
        file.add_separator()  

        dirs = os.listdir()
        deleteDB = Menu(file, tearoff = 0)

        if len(dirs) == 0: deleteDB.add_command(label = 'empty')
        for i in range(0, len(dirs)): 
            if dirs[i - 1][-3:] == '.db': deleteDB.add_command(label = f'{dirs[i - 1]}', command = lambda n = i: deleteDatabase(dirs[n - 1]))
        file.add_cascade(label = 'Delete DB', menu = deleteDB)

        chDB = Menu(file, tearoff = 0)

        if len(dirs) == 0: chDB.add_command(label = 'empty')
        for i in range(0, len(dirs)): 
            if dirs[i - 1][-3:] == '.db': chDB.add_command(label = f'{dirs[i - 1]}', command = lambda n = i: chooseDatabase(dirs[n - 1]))
        file.add_cascade(label = 'Choose DB', menu = chDB) 
        file.add_command(label = 'Encrypt DB')
        file.add_separator()  
        file.add_command(label = 'Exit', command = quitTool)
        menubar.add_cascade(label = 'File', menu = file)  

        edit = Menu(menubar, tearoff = 0)  
        edit.add_command(label = 'Undo')  
        edit.add_separator()     
        edit.add_command(label = 'Cut', command = cut)  
        edit.add_command(label = 'Copy', command = copy)  
        edit.add_command(label = 'Paste', command = paste)
        edit.add_separator()  
        edit.add_command(label = 'Reset Workspace', command = rWorkspace)
        menubar.add_cascade(label = 'Edit', menu = edit)
        
        view = Menu(menubar, tearoff = 0)
        
        view.add_checkbutton(label = 'Dark mode', onvalue = True, offvalue = False, variable = darkmode)
        view.add_checkbutton(label = 'Enter Mode', onvalue = True, offvalue = False, variable = entermode, command = enterMode)
        view.add_separator()  
        view.add_cascade(label = 'View Table', command = lambda: listItems()) 
        menubar.add_cascade(label = 'View', menu = view)

        help = Menu(menubar, tearoff = 0)  
        help.add_command(label = 'Help', command = lambda: helpS(0))
        help.add_separator()    
        help.add_command(label = 'License')   
        help.add_command(label = 'About', command = about)   
        menubar.add_cascade(label = 'Help', menu = help)  
            
        window.config(menu = menubar)

mb = menubar()
mb.createMenubar()

# Run mainloop
window.mainloop()
