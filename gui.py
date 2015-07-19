from tkinter import Tk, BOTH, X, Y, Menu, RAISED, LEFT, RIGHT, TOP, BOTTOM, N, S, E, W
from tkinter.ttk import Frame, Button, Style, Label
import sys


class windowFrame(Frame):
    def __init__(self, parent):
    
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
        self.bind_all("<Control-w>", self.onExit)
        self.bind_all("<Control-s>", self.recipeSave)
    def helpAbout(self):
        print("Recipe Editor v2.0 - Theodore Lindsey")
    def xmlImport(self):
        print("Importing XML file...")
    def recipeAdd(self):
        print("Adding recipe...")
    def recipeDelete(self):
        print("Deleting recipe...")
    def recipeEdit(self):
        print("Editing recipe...")
    def recipeSave(self,event=""):
        print("Saving recipe...")
    def onExit(self,event=""):
        print("Quitting...")
        sys.exit(0)
        
    def initUI(self):
      
        self.parent.title("Recipe Editor")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1, side=BOTTOM)
        
        # Establish menu bar #
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        # Add file menu #
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Import recipe from XML file", command=self.xmlImport)
        filemenu.add_command(label="Add blank recipe to database", command=self.recipeAdd)
        filemenu.add_command(label="Delete recipe from database", command=self.recipeDelete)
        filemenu.add_command(label="Edit recipe", command=self.recipeEdit)
        filemenu.add_command(label="Save recipe to database", command=self.recipeSave, accelerator="Ctrl+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.onExit, accelerator="Ctrl+W")
        # Add help menu #
        helpmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.helpAbout)
        
        
        
        # Establish toolbar #
        frameToolbar = Frame(self.parent)#, relief=RAISED, borderwidth=1)
        frameToolbar.pack(side=TOP, fill=X)
        # Add buttons to toolbar #
        buffer = 2
        buttonspaceing = 100
        buttonwidth = 12
        buttonheight = 30
        bImportXML = Button(frameToolbar, text="Import XML", command=self.xmlImport, width=buttonwidth)
        bImportXML.pack(side=LEFT, padx=buffer, pady=buffer)
        bAddRecipe = Button(frameToolbar, text="Add Recipe", command=self.recipeAdd, width=buttonwidth)
        bAddRecipe.pack(side=LEFT, padx=buffer, pady=buffer)
        bDeleteRecipe = Button(frameToolbar, text="Delete Recipe", command=self.recipeDelete, width=buttonwidth)
        bDeleteRecipe.pack(side=LEFT, padx=buffer, pady=buffer)
        bEditRecipe = Button(frameToolbar, text="Edit Recipe", command=self.recipeEdit, width=buttonwidth)
        bEditRecipe.pack(side=LEFT, padx=buffer, pady=buffer)
        bSaveRecipe = Button(frameToolbar, text="Save Recipe", command=self.recipeSave, width=buttonwidth)
        bSaveRecipe.pack(side=LEFT, padx=buffer, pady=buffer)
        
        frameRecipeList = Frame(self, relief=RAISED, borderwidth=1, width=200)
        frameRecipeList.pack(side=LEFT, fill=Y)
        Label(frameRecipeList, text="Recipe List").pack()
        
        frameSpacer = Frame(self, relief=RAISED, borderwidth=1, width=50)
        frameSpacer.pack(side=LEFT, fill=Y)
        Label(frameSpacer, text="Spacer").pack()
        
        frameRecipeInfo = Frame(self, relief=RAISED, borderwidth=1, width=200)
        frameRecipeInfo.pack(side=LEFT, fill=Y)
        Label(frameRecipeInfo, text="Recipe Info").pack()
        
        frameIngredients = Frame(self, relief=RAISED, borderwidth=1, width=300)
        frameIngredients.pack(side=LEFT, fill=Y)
        Label(frameIngredients, text="Ingredients").pack()
        
        frameProcedure = Frame(self, relief=RAISED, borderwidth=1)
        frameProcedure.pack(side=LEFT, fill=BOTH, expand=1)
        Label(frameProcedure, text="Procedure").pack()
        
        
        
        
        
        
        
        
        
    def placeholder(self):
        print("Coming soon!")
        
        



def main():
  
    root = Tk()
    root.geometry("980x680+300+300")
    root.minsize(600,350)
    app = windowFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  