import wx, mysql.connector, webbrowser
from mysql.connector import Error
import wx.lib.scrolledpanel, sys
import clipboard

#Testing
try:
    connection = mysql.connector.connect(host = 'localhost', database = "resources_db", user = "your_username", password = "your_password")
    if connection.is_connected():
        print("Connected to MySQL Server")      
except Error as e:
    print("Error while connecting")

class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt = True)
        #initialize frame
        frame = MyFrame()
        frame.Show()

class FileMenu(wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        self.OnInit()
        self.parentFrame = parentFrame    

    def OnInit(self):
        aboutItem = wx.MenuItem(parentMenu = self, id = wx.ID_ANY, text = "&About")
        self.Append(aboutItem)
        self.Bind(wx.EVT_MENU, handler = self.onAbout, source = aboutItem)
        quitItem = wx.MenuItem(parentMenu = self, id = wx.ID_ANY, text = '&Quit\tCtrl+Q')
        self.Append(quitItem)
        self.Bind(wx.EVT_MENU, handler = self.onQuit, source = quitItem)

    def onAbout(self, event):
        aboutFrame = AboutFrame()
        aboutFrame.Show()

    def onQuit(self, event):
        sys.exit()

class EditMenu(wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        self.OnInit()
        self.parentFrame = parentFrame

    def OnInit(self):
        pasteItem = wx.MenuItem(parentMenu = self, id = wx.ID_PASTE, text = '&Paste\tCtrl+V')
        self.Append(pasteItem)
        self.Bind(wx.EVT_MENU, handler = self.onPaste, source = pasteItem)

    def onPaste(self, event):
        clipboard.paste()

class HelpMenu(wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        self.OnInit()
        self.parentFrame = parentFrame
    def OnInit(self):
        helpItem = wx.MenuItem(parentMenu = self, id = wx.ID_ANY, text = "How to Get Started")
        self.Append(helpItem)
        self.Bind(wx.EVT_MENU, handler = self.onHelp, source = helpItem)
    def onHelp(self, event):
        helpFrame = HelpFrame()
        helpFrame.Show()
        
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = "Coding Resources Database", pos = (10, 27), size = (1355, 720))
        #initialize the panel
        self.OnInit()

    def OnInit(self):
        self.panel = MyPanel(self) 
        menuBar = wx.MenuBar()
        fileMenu = FileMenu(parentFrame = self)
        editMenu = EditMenu(parentFrame = self)
        helpMenu = HelpMenu(parentFrame = self)
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(editMenu, '&Edit')
        menuBar.Append(helpMenu, '&Help')
        self.SetMenuBar(menuBar)
        

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent = parent)

        #button to quit the program
        quitButton = wx.Button(self, label = "Quit", pos = (1090, 640))
        quitButton.Bind(wx.EVT_BUTTON, self.onQuit)

        panelScroll = wx.lib.scrolledpanel.ScrolledPanel(self, size = (1295, 250), pos = (35, 100), style = wx.SIMPLE_BORDER)
        boxSizer = wx.BoxSizer(wx.VERTICAL)

        #Setting up the resource headers
        idLabel = wx.StaticText(self, label = "ID", pos = (35, 65))
        titleLabel = wx.StaticText(self, label = "Title", pos = (70, 65))
        topicLabel = wx.StaticText(self, label = "Topic", pos = (525, 65))    
        urlLabel = wx.StaticText(self, label = "URL", pos = (650, 65))  

        idAppend = wx.StaticText(panelScroll, label = "", pos = (50, 65))
        titleAppend = wx.StaticText(panelScroll, label = "", pos = (35, 0))
        topicAppend = wx.StaticText(panelScroll, label = "", pos = (487, 0))
        urlAppend = wx.StaticText(panelScroll, label = "", pos = (610, 0))

        #setting up the search headers
        searchLabel = wx.StaticText(self, label = "Search Resource", pos = (105, 365))
        searchTitleLabel = wx.StaticText(self, label = "Search by Title", pos = (105, 390))
        andOrLabel = wx.StaticText(self, label = "And/Or", pos = (480, 386))
        searchByTopicLabel = wx.StaticText(self, label = "Search by Topic", pos = (555, 390))
        
        #setting up search inputs
        global searchTitleInput, searchTopicInput
        searchTitleInput = wx.TextCtrl(self, pos = (105, 415), size = (350, 25))
        searchTopicInput = wx.TextCtrl(self, pos = (555, 415), size = (100, 25))

        #setting up launch header and input
        launchIdLabel = wx.StaticText(self, label = "Open Resource by ID", pos = (910, 365))
        launchIdInstruction = wx.StaticText(self, label = "Insert ID: ", pos = (910, 405))
        launchIdInput = wx.TextCtrl(self, pos = (985, 402), size = (60, 25))
        
        #setting up the insert headers
        insertLabel = wx.StaticText(self, label = "Insert New Resource", pos = (105, 450))
        insertTitleLabel = wx.StaticText(self, label = "Title", pos = (105, 475))
        insertTopicLabel = wx.StaticText(self, label = "Topic", pos = (472, 475))
        insertUrlLabel = wx.StaticText(self, label = "URL", pos = (660, 475))

        #setting up the insert inputs
        insertTitleInput = wx.TextCtrl(self, pos = (105, 500), size = (350, 25))
        insertTopicInput = wx.TextCtrl(self, pos = (470, 500), size = (175, 25))
        insertUrlInput = wx.TextCtrl(self, pos = (660, 500), size = (415, 25))

        #setting up the delete headers and input
        deleteLabel = wx.StaticText(self, label = "Delete Resource by ID", pos = (105, 535))
        deleteId = wx.StaticText(self, label = "Insert ID: ", pos = (105, 570))
        deleteIdInput = wx.TextCtrl(self, pos = (180, 568), size = (45, 25))
        
        #setting font
        headerFont = wx.Font(14, wx.DEFAULT, wx.BOLD, wx.NORMAL)
        idLabel.SetFont(headerFont)
        titleLabel.SetFont(headerFont)
        topicLabel.SetFont(headerFont)
        urlLabel.SetFont(headerFont)
        searchLabel.SetFont(headerFont)
        insertLabel.SetFont(headerFont)
        launchIdLabel.SetFont(headerFont)
        deleteLabel.SetFont(headerFont)

        def create_table_if_not_exists():
            connection = mysql.connector.connect(host = 'localhost', database = "resources_db", user = "your_username", password = "your_password")
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS resources (
                id_number INTEGER PRIMARY KEY AUTO_INCREMENT,
                title text,
                topic text,
                url text);""")
            connection.commit()
            connection.close()

        def insertResource(title, topic, url):
            connection = mysql.connector.connect(host = 'localhost', database = "resources_db", user = "your_username", password = "your_password")
            cursor = connection.cursor()

            cursor.execute("ALTER TABLE resources MODIFY id_number integer;")
            cursor.execute("ALTER TABLE resources DROP PRIMARY KEY;")
            cursor.execute("UPDATE resources SET id_number = 0;")
            cursor.execute("ALTER TABLE resources MODIFY id_number int;")
            cursor.execute("ALTER TABLE resources MODIFY COLUMN id_number int NOT NULL Primary Key auto_increment First;")
            
            cursor.execute("""INSERT INTO resources (title, topic, url) VALUES
                (%s, %s, %s);""", (title, topic, url,))
            cursor.execute("ALTER TABLE resources MODIFY id_number integer;")
            cursor.execute("ALTER TABLE resources DROP PRIMARY KEY;")
            cursor.execute("UPDATE resources SET id_number = 0;")
            cursor.execute("ALTER TABLE resources MODIFY id_number int;")
            cursor.execute("ALTER TABLE resources MODIFY COLUMN id_number int NOT NULL Primary Key auto_increment First;")

            connection.commit()
            connection.close()

        def showData(query):
            connection = mysql.connector.connect(host = 'localhost', database = "resources_db", user = "your_username", password = "your_password")
            cursor = connection.cursor()
            cursor.execute(query)
             
            allResources = cursor.fetchall()
            appendedId = ""
            appendedTitle = ""
            appendedTopic = ""
            appendedUrl = ""

            for id_number, title, topic, url in allResources:
                appendedId += str(id_number) + '\n'
                appendedTitle += str(title) + '\n'
                appendedTopic += topic + '\n'
                appendedUrl += url + '\n'
                  
            idAppend.SetLabel(appendedId)
            titleAppend.SetLabel(appendedTitle)
            topicAppend.SetLabel(appendedTopic)
            urlAppend.SetLabel(appendedUrl)
            
            connection.commit()
            connection.close()
            panelScroll.SetupScrolling(scroll_x = True, scroll_y = True)

        def onSearch(event):
            getSearchTitleInput = searchTitleInput.GetValue()
            print(getSearchTitleInput)
            getSearchTopicInput = searchTopicInput.GetValue()
            print(getSearchTopicInput)

            showData("SELECT * FROM resources WHERE title LIKE '%%{}%' AND topic LIKE '%%{}%';".format(getSearchTitleInput, getSearchTopicInput))

        def onLaunch(event):
            getLaunchId = int(launchIdInput.GetValue())
            print(getLaunchId)
            connection = mysql.connector.connect(host = 'localhost', database = "resources_db", user = "your_username", password = "your_password")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM resources WHERE id_number = (%s);"%getLaunchId)
            for row in cursor:
                print("{url}".format(url=row[3]))
                webbrowser.get('firefox').open_new_tab("{url}".format(url=row[3]))
                
            connection.commit()
            connection.close()
            
        def onInsert(event):
            getInsertTitleInput = str(insertTitleInput.GetValue())
            print(getInsertTitleInput)
            getInsertTopicInput = insertTopicInput.GetValue()
            print(getInsertTopicInput)
            getInsertUrlInput = insertUrlInput.GetValue()
            print(getInsertUrlInput)

            insertResource(getInsertTitleInput, getInsertTopicInput, getInsertUrlInput)
            showData("SELECT * FROM resources;")

            insertTitleInput.Clear()
            insertTopicInput.Clear()
            insertUrlInput.Clear()

        def onDelete(event):
            idToDelete = deleteIdInput.GetValue()
            connection = mysql.connector.connect(host = 'localhost', database = "resources_db", user = "your_username", password = "your_password")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM resources WHERE id_number = (%s);"%idToDelete)
            cursor.execute("ALTER TABLE resources MODIFY id_number integer;")
            cursor.execute("ALTER TABLE resources DROP PRIMARY KEY;")
            cursor.execute("UPDATE resources SET id_number = 0;")
            cursor.execute("ALTER TABLE resources MODIFY id_number int;")
            cursor.execute("ALTER TABLE resources MODIFY COLUMN id_number int NOT NULL Primary Key auto_increment First;")
            showData("SELECT * FROM resources;")
            
            connection.commit()
            connection.close()
            deleteIdInput.Clear()
            
        boxSizer.Add(idAppend)
        panelScroll.SetSizer(boxSizer)
        panelScroll.SetupScrolling(scroll_x = True, scroll_y = True)
    
        create_table_if_not_exists()
        showData("SELECT * FROM resources;")

        #Search button
        searchButton = wx.Button(parent = self, label = "Search", pos = (700, 405))
        searchButton.Bind(wx.EVT_BUTTON, onSearch)

        #Launch button
        launchButton = wx.Button(self, label = "Open in Firefox", pos = (1060, 403))
        launchButton.Bind(wx.EVT_BUTTON, onLaunch)

        #Insert button
        insertButton = wx.Button(parent = self, label = "Insert", pos = (1088, 500))
        insertButton.Bind(wx.EVT_BUTTON, onInsert)

        #Delete button
        deleteButton = wx.Button(parent = self, label = "Delete", pos = (247, 570))
        deleteButton.Bind(wx.EVT_BUTTON, onDelete)

    def onQuit(self, event):
        sys.exit()

class AboutFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = "About", pos = (100, 100), size = (380, 170))
        #initialize the about panel
        self.OnInit()

    def OnInit(self):
        self.panel = AboutPanel(self)
        self.panel.SetBackgroundColour(wx.Colour(255, 255, 255))

class AboutPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent = parent)
        wx.StaticText(self, label = "Resources Database Manager", pos = (100, 30))
        wx.StaticText(self, label = "Contact ryamanaka807@gmail.com for support.", pos = (40, 60))
        wx.StaticText(self, label = "Copyright 2020 Reo Yamanaka. All Rights Reserved.", pos = (30, 90))

class HelpFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = "How to Get Started", pos = (100, 100), size = (745, 220))
        #init help panel
        self.OnInit()

    def OnInit(self):
        self.panel = HelpPanel(self)
        self.panel.SetBackgroundColour(wx.Colour(255, 255, 255))

class HelpPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent = parent)
        wx.StaticText(self, label = "1. This program was written for a local database. Download and install a program such as XAMPP or AMPPS.\n", pos = (40, 40)) 
        wx.StaticText(self, label = "2. Create a local database called resources_db and create a user with all privileges.\n", pos = (40, 80))
        wx.StaticText(self, label = "3. Type in the appropriate database name, username and password into the connection variables.", pos = (40, 120))
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
