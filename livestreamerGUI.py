import Tkinter as tk
import subprocess as sub

#class to read streams from file
class Data:
    def __init__(self):
        self.fileName = 'Streams.txt'
        self.nameList = []
        self.urlList = []
        self.tempList = []
        try:
            self.fileObject = open(self.fileName, 'r')
            self.readFile()
            self.fileObject.close()
        except:
            pass
        pass

    #read file
    def readFile(self):
        for i in self.fileObject:
            self.tempString = i
            self.tempList = self.tempString.split()
            self.nameList.append(self.tempList[0])
            self.urlList.append(self.tempList[1])
        pass

    #write new stream to file
    def writeLine(self):
        self.fileObject.write(self.tempString + '\n')
        pass

    def newStream(self, name, url):
        self.nameList.append(name)
        self.urlList.append(url)
        pass

    def deleteStream(self, name):
        self.urlList.remove(self.urlList[self.nameList.index(name)])
        self.nameList.remove(name)
        pass

    def close(self):
        self.fileObject = open(self.fileName, 'w')
        for i in range(0, self.nameList.__len__()):
            self.tempString = self.nameList[i] + ' ' + self.urlList[i]
            self.writeLine()
        self.fileObject.close()
        pass

#class to create gui and store data
class GUI:
    #get names and urls from file, create widgets
    def __init__(self):
        self.data = Data()
        self.createWidgetsRoot()
        self.createWidgetsChild()
        self.childWindow.withdraw()
        pass

    #create main dialog
    def createWidgetsRoot(self):
        #create mainwindow
        self.root = tk.Tk()
        self.root.wm_iconbitmap('@icon.xbm')
        self.root.title('Livestreamer Interface')
        self.root.geometry('+500+200')

        self.app = tk.Frame(self.root)
        self.app.grid()

        #create labels
        self.streamLabel = tk.Label(self.app)
        self.streamLabel.configure(text = 'Choose your Stream: ')
        self.streamLabel.grid(row = 0, column = 0, sticky = 'w')

        self.qualityLabel = tk.Label(self.app)
        self.qualityLabel.configure(text = 'Choose quality: ')
        self.qualityLabel.grid(row = 1, column = 0, sticky = 'w')

        #create dropdown menus
        self.qualtiyOptionVar = tk.StringVar(self.root)
        self.qualtiyOptionVar.set('medium')
        self.qualityOption = tk.OptionMenu(self.app, self.qualtiyOptionVar, 'source', 'high', 'medium', 'low', 'mobile', 'audio')
        self.qualityOption.grid(row = 1, column = 1, sticky = 'w')

        self.nameOptionVar = tk.StringVar(self.root)
        try:
            self.nameOptionVar.set(self.data.nameList[0])
        except:
            self.nameOptionVar.set(None)
        self.nameOption = tk.OptionMenu(self.app, self.nameOptionVar, '') 
        self.updateNameOption()
        self.nameOption.grid(row = 0, column = 1, sticky = 'w')

        #create buttons
        self.okButton = tk.Button(self.app)
        self.okButton.configure(text = 'Start Stream')
        self.okButton.configure(command = self.startStream)
        self.okButton.configure(width = 20)
        self.okButton.grid(row = 2, column = 0, columnspan = 2)

        self.newStreamButton = tk.Button(self.app)
        self.newStreamButton.configure(text = 'New Stream')
        self.newStreamButton.configure(command = self.showChildWindow)
        self.newStreamButton.configure(width = 20)
        self.newStreamButton.grid(row = 3, column = 0, columnspan = 2)

        self.delteStreamButton = tk.Button(self.app)
        self.delteStreamButton.configure(text = 'Delete selected Stream')
        self.delteStreamButton.configure(command = self.deleteSelectedStream)
        self.delteStreamButton.configure(width = 20)
        self.delteStreamButton.grid(row = 4, column = 0, columnspan = 2)

        self.closeButton = tk.Button(self.app)
        self.closeButton.configure(text = 'Close')
        self.closeButton.configure(command = self.close)
        self.closeButton.configure(width = 20)
        self.closeButton.grid(row = 5, column = 0, columnspan = 2)

        self.root.protocol('WM_DELETE_WINDOW', self.close)
        pass


    #updates name option menu
    def updateNameOption(self):
        self.nameMenu = self.nameOption['menu']
        self.nameMenu.delete(0, 'end')
        try:
            self.nameOptionVar.set(self.data.nameList[0])
        except:
            self.nameOptionVar.set(None)
        for name in self.data.nameList:
            self.nameMenu.add_command(label = name, command = tk._setit(self.nameOptionVar, name))
        pass

    def createWidgetsChild(self):
        #create child window
        self.childWindow = tk.Toplevel(self.root)
        self.childWindow.wm_iconbitmap('@icon.xbm')
        self.childWindow.title('New Stream')
        self.childWindow.geometry('+500+200')
        
        #create child labels
        self.nameLabelChild = tk.Label(self.childWindow)
        self.nameLabelChild.configure(text = 'Name of Stream:')
        self.nameLabelChild.grid(row = 0, column = 0, sticky = 'w')
        
        self.urlLabelChild = tk.Label(self.childWindow)
        self.urlLabelChild.configure(text = 'Url of Stream:')
        self.urlLabelChild.grid(row = 1, column = 0, sticky = 'w')

        #create child entrys
        self.nameEntryChild = tk.Entry(self.childWindow)
        self.nameEntryChild.grid(row = 0, column = 1, sticky = 'w')

        self.urlEntryChild = tk.Entry(self.childWindow)
        self.urlEntryChild.grid(row = 1, column = 1, sticky = 'w')

        #create child buttons
        self.okButtonChild = tk.Button(self.childWindow)
        self.okButtonChild.configure(text = 'Add Stream')
        self.okButtonChild.configure(command = self.applyNewStream)
        self.okButtonChild.configure(width = 20)
        self.okButtonChild.grid(row = 2, column = 0, columnspan = 2)

        self.closeButtonChild = tk.Button(self.childWindow)
        self.closeButtonChild.configure(text = 'Close')
        self.closeButtonChild.configure(command = self.hideChildWindow)
        self.closeButtonChild.configure(width = 20)
        self.closeButtonChild.grid(row = 3, column = 0, columnspan = 2)

        self.childWindow.protocol('WM_DELETE_WINDOW', self.hideChildWindow)
        pass

    #shows child window
    def showChildWindow(self):
        self.nameEntryChild.delete(0, 'end')
        self.urlEntryChild.delete(0, 'end')
        self.root.withdraw()
        self.childWindow.deiconify()
        pass

    #hides child window
    def hideChildWindow(self):
        self.root.deiconify()
        self.childWindow.withdraw()
        pass


    #calls livestreamer, when clicking the 'Start Stream' button
    def startStream(self):
        sub.call(['livestreamer', self.data.urlList[self.data.nameList.index(self.nameOptionVar.get())], self.qualtiyOptionVar.get()])
        pass

    #run mainloop
    def run(self):
        self.root.mainloop()
        pass

    #adds new stream to program
    def applyNewStream(self):
        self.data.newStream(self.nameEntryChild.get(), self.urlEntryChild.get())
        self.updateNameOption()
        self.root.deiconify()
        self.childWindow.withdraw()
        pass

    #delete stream from lists
    def deleteSelectedStream(self):
        self.data.deleteStream(self.nameOptionVar.get())
        self.updateNameOption()
        pass

    #closes filestream and application
    def close(self):
        self.data.close()
        self.root.destroy()
        pass
       
def main():
    livestreamerGUI = GUI()
    livestreamerGUI.run()
    pass

if __name__ == '__main__':
    main()
