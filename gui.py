from tkinter import Tk, BOTH, X, Y, Menu, RAISED, LEFT, RIGHT, TOP, BOTTOM, END, N, S, E, W, EXTENDED, VERTICAL, StringVar, Listbox, Text
from tkinter.ttk import Frame, Button, Style, Label, OptionMenu, Entry, Scrollbar
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
        
        # Recipe list section
        frameRecipeList = Frame(self, borderwidth=1, width=200)
        frameRecipeList.pack_propagate(0)
        frameRecipeList.pack(side=LEFT, fill=Y)
        Label(frameRecipeList, text="Recipe List").pack()
        # Category option menu
        default = StringVar(frameRecipeList)
        default.set("----")
        recipeCatagories = OptionMenu(frameRecipeList, default,"----","None","Cat 1","Cat 2","Cat 3")
        recipeCatagories.pack(side=TOP, fill=X)
        # Filter Frame
        frameFilter = Frame(frameRecipeList, relief=RAISED, borderwidth=1, width=200)
        frameFilter.pack(side=TOP, fill=X)
        Label(frameFilter, text="Filter...").pack()
        # Filter text
        filterText = Entry(frameFilter)
        filterText.pack_propagate(0)
        filterText.pack(side=LEFT, fill=X)
        # Filter Button
        filterButton = Button(frameFilter, text="Go", command=self.placeholder)
        filterButton.pack_propagate(0)
        filterButton.pack(side=RIGHT)
        # Recipe Box Frame
        frameRecipeBox = Frame(frameRecipeList, relief=RAISED, borderwidth=1)
        frameRecipeBox.pack(side=TOP, fill=BOTH, expand=1)
        # Recipe List box
        recipeListScroll = Scrollbar(frameRecipeBox, orient=VERTICAL)
        recipeList = Listbox(frameRecipeBox, selectmode=EXTENDED, yscrollcommand=recipeListScroll.set)
        recipeList.pack(side=LEFT, fill=BOTH, expand=1)
        recipeListScroll.config(command=recipeList.yview)
        recipeListScroll.pack(side=RIGHT, fill=Y)
        for item in range(1,1001):
            recipeList.insert(END, "Recipe "+str(item))
        
        
        # Spacer
        frameSpacer1 = Frame(self, borderwidth=1, width=50)
        frameSpacer1.pack_propagate(0)
        frameSpacer1.pack(side=LEFT, fill=Y)
        
        # Recipe info section
        frameRecipeInfo = Frame(self, borderwidth=1, width=200)
        frameRecipeInfo.pack_propagate(0)
        frameRecipeInfo.pack(side=LEFT, fill=Y)
        # Recipe name
        Label(frameRecipeInfo, text="Recipe Name:", anchor=E, justify=LEFT).pack()
        recipeName = Entry(frameRecipeInfo)
        recipeName.pack(side=TOP, fill=X)
        # Prep Time
        framePrepTime = Frame(frameRecipeInfo)
        framePrepTime.pack(side=TOP, fill=X)
        Label(framePrepTime, text="Prep Time:", anchor=E, justify=LEFT).pack()
        prepTime = Entry(framePrepTime)
        prepTime.pack(side=LEFT, fill=X)
        default = StringVar(framePrepTime)
        default.set("----")
        prepTimeUnit = OptionMenu(framePrepTime, default,"----","Min","Hr")
        prepTimeUnit.pack(side=RIGHT, fill=X)
        # Cook Time
        frameCookTime = Frame(frameRecipeInfo)
        frameCookTime.pack(side=TOP, fill=X)
        Label(frameCookTime, text="Cook Time:", anchor=E, justify=LEFT).pack()
        cookTime = Entry(frameCookTime)
        cookTime.pack(side=LEFT, fill=X)
        default = StringVar(frameCookTime)
        default.set("----")
        cookTimeUnit = OptionMenu(frameCookTime, default,"----","Min","Hr")
        cookTimeUnit.pack(side=RIGHT, fill=X)
        
        # Spacer
        frameSpacer2 = Frame(self, borderwidth=1, width=10)
        frameSpacer2.pack_propagate(0)
        frameSpacer2.pack(side=LEFT, fill=Y)
        
        # Ingredient List
        frameIngredients = Frame(self, borderwidth=1, width=300)
        frameIngredients.pack_propagate(0)
        frameIngredients.pack(side=LEFT, fill=Y)
        Label(frameIngredients, text="Ingredients").pack()
        # Ingredient Name
        ingredientName = Entry(frameIngredients)
        ingredientName.pack(side=TOP, fill=X)
        # Ingredient info
        frameIngredientQuantity = Frame(frameIngredients)
        frameIngredientQuantity.pack(side=TOP, fill=X)
        Label(frameIngredientQuantity, text="Ingredient Quantity:", anchor=E, justify=LEFT).pack()
        ingredientQuantity = Entry(frameIngredientQuantity)
        ingredientQuantity.pack(side=LEFT, fill=X)
        default = StringVar(frameIngredientQuantity)
        default.set("----")
        ingredientUnit = OptionMenu(frameIngredientQuantity, default,"----","lbs","cups")
        ingredientUnit.pack(side=RIGHT, fill=X, expand=1)
        # Spacer
        frameSpacer3 = Frame(frameIngredients, height=10)
        frameSpacer3.pack_propagate(0)
        frameSpacer3.pack(side=TOP, fill=X)
        # Ingredient List buttons
        frameIngredientButtons = Frame(frameIngredients)
        frameIngredientButtons.pack(side=TOP, fill=X)
        ingredientAdd = Button(frameIngredientButtons, text="+", command=self.placeholder)
        ingredientAdd.pack(side=LEFT)
        ingredientDel = Button(frameIngredientButtons, text="-", command=self.placeholder)
        ingredientDel.pack(side=LEFT)
        ingredientUp = Button(frameIngredientButtons, text=u"\u25B2", command=self.placeholder)
        ingredientUp.pack(side=LEFT)
        ingredientDwn = Button(frameIngredientButtons, text=u"\u25BC", command=self.placeholder)
        ingredientDwn.pack(side=LEFT)
        # Ingredient List Box Frame
        frameIngredientList = Frame(frameIngredients, relief=RAISED, borderwidth=1)
        frameIngredientList.pack(side=TOP, fill=BOTH, expand=1)
        # Recipe List box
        ingredientListScroll = Scrollbar(frameIngredientList, orient=VERTICAL)
        ingredientList = Listbox(frameIngredientList, selectmode=EXTENDED, yscrollcommand=ingredientListScroll.set)
        ingredientList.pack(side=LEFT, fill=BOTH, expand=1)
        ingredientListScroll.config(command=ingredientList.yview)
        ingredientListScroll.pack(side=RIGHT, fill=Y)
        for item in range(1,1001):
            ingredientList.insert(END, "Ingredient "+str(item))
        
        # Spacer
        frameSpacer4 = Frame(self, borderwidth=1, width=10)
        frameSpacer4.pack_propagate(0)
        frameSpacer4.pack(side=LEFT, fill=Y)
        
        
        # Recipe Procedure
        frameProcedure = Frame(self, borderwidth=1)
        frameProcedure.pack(side=LEFT, fill=BOTH, expand=1)
        Label(frameProcedure, text="Procedure", anchor=E, justify=LEFT).pack(side=TOP)
        procedure = Text(frameProcedure, maxundo=30, undo=1)
        procedure.pack(side=TOP, fill=BOTH, expand=1)
        
    def placeholder(self):
        print("Coming soon!")
        
        



def main():
  
    root = Tk()
    root.geometry("1024x680+300+300")
    root.minsize(1024,350)
    app = windowFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  