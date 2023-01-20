from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import *
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3
import os
import ctypes

currentDatabase = ''
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
    files = os.listdir('databases')
    for file in files:
        if file[-3:] == '.db':
            databases.append(file)

def buildDatabase():
    global var
    global currentDatabase
    global dbDropdown
    global dbNameTextbox

    dbName = dbNameTextbox.get() + '.db'
    dbNameTextbox.delete(0, END)

    if dbName == '.db':
        outputTextbox.insert(END, 'ERROR: Please enter a name for your new database.\n\n')

    elif dbName in databases:
        outputTextbox.insert(END, 'ERROR: Database already exists.\n\n')
    else:
        try:
            with sqlite3.connect(dbName) as db:
                cursor = db.cursor()
                outputTextbox.insert(END, f'Successfully created database {dbName}.\n\n')
        except:
            outputTextbox.insert(END, 'ERROR: Please try again.\n\n')
        else:
            databases.append(dbName)
            currentDatabase = dbName
            dbDropdown.destroy()

            var = StringVar()
            var.set(dbName)
            dbDropdown = OptionMenu(frameButtons, var, *databases, command = chooseDatabase)
            dbDropdown.grid(row = 0, column = 0, sticky = NW)

def chooseDatabase(value):
    global currentDatabase
    currentDatabase = value
    
def clearOutput():
    clear = tkinter.messagebox.askquestion('Clear', 'Are you sure you want to clear the output table?')
    if clear == 'yes':
        outputTextbox.delete(0.0, END) 

def getTables():
    if currentDatabase == '':
        outputTextbox.insert(END, 'ERROR: Please choose a database.\n\n')
    else:
        query = '''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;'''
        runSql(query)

def quitTool():
    quit = tkinter.messagebox.askquestion('Quit', 'Are you sure you want to quit?')
    if quit == 'yes':
        window.withdraw()
        window.quit()


def help():
    root = Tk()

    root.title("Help with SQL")
    root.geometry('400x300')
        
    createTable = '''
CREATE TABLE table_name (
    column_1 datatype,
    column_2 datatype,
    column_3 datatype
);
    '''

    alterTable = '''
ALTER TABLE table_name
ADD column_name datatype;
    '''

    updateTable = '''
UPDATE table_name
SET column1 = value1, 
column2 = value2, ...
WHERE condition;
    '''

    deleteFromTable = '''
DELETE FROM table_name
WHERE condition;    
    '''

    frame = Frame(root)

    text_box = Text(
        frame,
        height=5,
        width=30,
        wrap='word'
    )
    text_box2 = Text(
        frame,
        height=5,
        width=30,
        wrap='word'
    )
    text_box.insert('end', createTable)
    text_box.pack(side=LEFT,expand=True)
    text_box2.insert('end', alterTable)
    text_box2.pack(side=LEFT,expand=True)

    sb = Scrollbar(frame)
    sb.pack(side=RIGHT, fill=BOTH)

    sb.config(command=text_box.yview)
    sb.config(command=text_box2.yview)


    frame.pack(expand=True)
    root.mainloop()

def runQuery():
    if currentDatabase == '':
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
        userInp = simpledialog.askstring(title = 'View Items', prompt = 'What table do you want to view:')
        runSql(f'''SELECT * FROM {userInp}''')

    except:
        if userInp != None:
            if userInp == '':
                outputTextbox.insert(END, 'There was no input')
            else:
                outputTextbox.insert(END, f'There is no such table as {userInp}')
   
# ----------------------------------------------------------------- Main Code -----------------------------------------------------------------
window = Tk()
window.title('Python Database Tool')

pythonLogo = PhotoImage(file = 'python-logo.gif')
sqliteLogo = PhotoImage(file = 'sqlite-logo.gif')

if not os.path.isdir("databases"):
    os.makedirs("databases")

updateDatabases()    
os.chdir('databases')

frameNewDb = Frame(window)
frameNewDb.grid(row = 3, column = 0, pady = 20, sticky = SW)

frameButtons = Frame(window)
frameButtons.grid(row = 0, column = 0)

frameQuery = Frame(window)
frameQuery.grid(row = 2, column = 0, sticky = NW)

frameOutput = Frame(window)
frameOutput.grid(row = 2, column = 1, rowspan = 2)

Label(frameNewDb, text='Create a new database:').grid(row = 0, column = 0, columnspan = 2, sticky = NW)
Label(frameNewDb, text='Choose a name: ').grid(row = 1, column = 0, sticky = NW)
Label(frameQuery, text='Add SQL:').grid(row = 0, column = 0, sticky = NW)
Label(frameOutput, text='Output: ').grid(row = 0, column = 0, sticky = NW)

dbNameTextbox = Entry(frameNewDb, width = 10)
dbNameTextbox.grid(row = 1, column = 1, sticky = NW)

sqlTextbox = Text(frameQuery, width = 50, height = 10, background = textboxColour)
sqlTextbox.grid(row = 1, column = 0, sticky = NW)

outputTextbox = ScrolledText(frameOutput, width = 65, height = 20, background = textboxColour)
outputTextbox.grid(row = 1, column = 0, sticky = NW)

Label(window, image=pythonLogo).grid(row = 1, column = 0, sticky = NW)
Label(window, image=sqliteLogo).grid(row = 1, column = 1, sticky = NW)

buttonQuit = Button(frameButtons, text = "Quit", width = 10, command = quitTool)
buttonQuit.grid(row = 0, column = 4, sticky = NE)
buttonHelp = Button(frameButtons, text = "Help", width = 10, command = help)
buttonHelp.grid(row = 0, column = 3, sticky = NE)
buttonList = Button(frameButtons, text = "List items", width = 15, command = listItems)
buttonList.grid(row = 0, column = 2, sticky = NE)
buttonClear = Button(frameOutput, text = "Clear result box", command = clearOutput)
buttonClear.grid(row = 2, column = 0, sticky = NE)
buttonRun = Button(frameQuery, text = "Run SQL", width = 10, command = runQuery)
buttonRun.grid(row = 2, column = 0, sticky = NW)
buttonTables = Button(frameButtons, text = "List Tables", width = 15, command = getTables)
buttonTables.grid(row = 0, column = 1, sticky = NE)
buttonSubmit = Button(frameNewDb, text = "Build database", command = buildDatabase)
buttonSubmit.grid(row = 2, column = 0, sticky = NW)

var = StringVar()
var.set('Choose database:')
dbDropdown = OptionMenu(frameButtons, var, *databases if databases else ['empty'], command = chooseDatabase)
dbDropdown.grid(row = 0, column = 0, sticky = NW)

def about():
    messagebox.showinfo('PythonGuides', 'Python Guides aims at providing best practical tutorials')

def darkMode():
    if darkmode.get() == 1:
        darkMode.config(background='black')
    elif darkmode.get() == 0:
        darkMode.config(background='white')
    else:
        messagebox.showerror('PythonGuides', 'Something went wrong!')

menubar = Menu(darkMode, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
file = Menu(menubar, tearoff=1, background='#ffcc99', foreground='black')  
file.add_command(label="New")  
file.add_command(label="Open")  
file.add_command(label="Save")  
file.add_command(label="Save as")    
file.add_separator()  
file.add_command(label="Exit", command=darkMode.quit)  
menubar.add_cascade(label="File", menu=file)  

edit = Menu(menubar, tearoff=0)  
edit.add_command(label="Undo")  
edit.add_separator()     
edit.add_command(label="Cut")  
edit.add_command(label="Copy")  
edit.add_command(label="Paste")  
menubar.add_cascade(label="Edit", menu=edit)  

minimap = BooleanVar()
minimap.set(True)
darkmode = BooleanVar()
darkmode.set(False)

view = Menu(menubar, tearoff=0)
view.add_checkbutton(label="show minimap", onvalue=1, offvalue=0, variable=minimap)
view.add_checkbutton(label='Darkmode', onvalue=1, offvalue=0, variable=darkmode, command=darkMode)
menubar.add_cascade(label='View', menu=view)

help = Menu(menubar, tearoff=0)  
help.add_command(label="About", command=about)  
menubar.add_cascade(label="Help", menu=help)  
    
window.config(menu=menubar)

# Run mainloop
window.mainloop()
