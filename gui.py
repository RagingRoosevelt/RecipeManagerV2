from tkinter import Tk, BOTH, X, Y, Menu, RAISED, LEFT, RIGHT, TOP, BOTTOM, END, N, S, E, W, EXTENDED, SINGLE, VERTICAL, StringVar, Listbox, Text, Toplevel, Message, ACTIVE, WORD
from tkinter.ttk import Frame, Button, Style, Label, OptionMenu, Entry, Scrollbar
#from tkinter import *
#from tkinter.ttk import *
from tkinter.messagebox import askokcancel, showwarning, showerror
from operator import itemgetter

import sys
from data import Data


class windowFrame(Frame):
    def __init__(self, parent):
        self.Data = Data()
        self.getReciepList()
    
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.recipeList = None         # Listbox
        self.recipeName = None         # Entry
        self.prepTime = None           # Entry
        self.prepTimeUnit = None       # OptionMenu
        self.cookTime = None           # Entry
        self.cookTimeUnit = None       # OptionMenu
        self.ingredientName = None     # Entry
        self.ingredientQuantity = None # Entry
        self.ingredientUnit = None     # OptionMenu
        self.ingredientList = None     # Listbox
        self.procedure = None          # Text
        
        self.recipes = []
        self.ingredients = []
        self.activeRecipeID = {"lst": None, "db": None}     # (listID, dbID)
        self.activeIngredientID = {"lst": None, "db": None} # (listID, dbID)
        
        self.initUI()
        
        self.bind_all("<Control-w>", self.onExit)
        self.bind_all("<Control-s>", self.recipeSave)
        
    
    # display an error message to the user
    def msgError(self, error):
        print("error: " + error)
        showerror("ERROR!", error)
        
    
    # dispaly a warning to the user
    def msgWarning(self, warning):
        showwarning("Warning!", warning)
    
    
    # display caution message to user
    def msgCaution(self, caution):
        return askokcancel("Caution!", caution)
    
    
    # Get current ingredient selection from ingredient list
    def getIngredientSelection(self):
        if self.ingredients == []:
            self.msgWarning("No ingredient selected.  Try loading a recipe.")
            return -1
        else:
            return self.ingredientList.index(ACTIVE)
    
    
    # Get current recipe selection from recipe list
    def getRecipeSelection(self):
        if self.recipes == []:
            self.msgError("No recipes available.")
            return -1
        else:
            selection = list(self.recipeList.curselection())
            
            if selection == []:
                self.msgError("No recipe selected.")
                return -1
            else:
                return selection
    
    
    # retrieve recipe list from the database
    def getReciepList(self):
        self.recipes = self.Data.dbGetRecipeList()
        
    
    # retrieve recipe info from the database by recipe ID
    def getRecipeInfo(self, recipeID):
        return self.Data.dbGetRecipeInfo(recipeID)
        
    
    # retrieve ingredient info from the database by ingredient ID
    def getIngredientInfo(self, ingredientID):
        return self.Data.dbGetIngredientInfo(ingredientID)
        
    
    # Populate the recipe list from a provided list of recipes
    def populateIngredientList(self, ingredients):
        self.ingredients = sorted(self.ingredients,key=itemgetter(-1))
    
        self.ingredientList.delete(0,END)
        for ingredient in self.ingredients:
            ingredientName = str(ingredient[2])
            ingredientQuantity = str(ingredient[3])
            ingredientUnit = str(ingredient[4])
            self.ingredientList.insert(END, ingredientQuantity + " " + ingredientUnit + " of " + ingredientName)
    
    
    # Populate the recipe list from a provided list of recipes
    def populateRecipeList(self, recipes):
        self.recipeList.delete(0,END)
        for recipe in [recipe[1] for recipe in recipes]:
            self.recipeList.insert(END, recipe)
            
    
    # save currently loaded ingredient info to database
    def ingredientSaveInfo(self):
        if self.activeIngredientID["lst"] == None:
            self.msgWarning("No ingredient is loaded.")
        else:
            print("Saving ingredient info")
            
            name = self.ingredientName.get()
            quantity = self.ingredientQuantity.get()
            unit = self.ingredientUnit.get()
            
            ingredient = self.ingredients[self.activeIngredientID["lst"]]
            
            print(ingredient)
            
            ingredient = (ingredient[0], ingredient[1], name, quantity, unit, ingredient[-1])
            
            print(ingredient)
            
            self.ingredients[self.activeIngredientID["lst"]] = ingredient
            
            self.populateIngredientList(self.ingredients)
        
        
    # load active ingredient info into GUI elements
    def ingredientLoadInfo(self, ID=None):
        
        if ID == None:
            currentSelection = self.getIngredientSelection()
            if currentSelection == -1:
                return -1
            else:
                self.activeIngredientID["lst"] = currentSelection
                self.activeIngredientID["db"] = self.ingredients[currentSelection][0]
                print("\n\nLoading ingredient info for ID " + str(self.activeIngredientID))
                ingredient = self.ingredients[self.activeIngredientID["lst"]]
        elif ID >= 0:
            self.activeIngredientID["lst"] = ID
            self.activeIngredientID["db"] = self.ingredients[ID][0]
            ingredient = self.ingredients[self.activeIngredientID["lst"]]
        elif ID == -1:
            print("Clearing ingredient info...")
            self.activeIngredientID = {"lst": None, "db": None}
            ingredient = ["","","","",""]
            
        name = ingredient[2]
        quantity = ingredient[3]
        unit = ingredient[4]
        
        self.ingredientName.delete(0,END)
        self.ingredientName.insert(END, name)
        self.ingredientQuantity.delete(0,END)
        self.ingredientQuantity.insert(END,quantity)
        self.ingredientUnit.delete(0,END)
        self.ingredientUnit.insert(END,unit)
            

    # Move an ingredient further up in the ingredient list
    def ingredientMoveUp(self):
        currentSelection = self.getIngredientSelection()
        if currentSelection == -1:
            return -1
        elif currentSelection > 0:
            if currentSelection == self.activeIngredientID["lst"] or currentSelection-1 == self.activeIngredientID["lst"]:
                if not self.msgCaution("Reordering the actively loaded ingredient could cause duplicate and deleted entries when saving.  Continue?"):
                    return
            print("ingredient %d up\n\n" % currentSelection)
            
            self.ingredients[currentSelection] = self.ingredients[currentSelection][0:-1] + (self.ingredients[currentSelection][-1]-1,)
            self.ingredients[currentSelection-1] = self.ingredients[currentSelection-1][0:-1] + (self.ingredients[currentSelection-1][-1]+1,)
            
            self.populateIngredientList(self.ingredients)
            
            self.ingredientList.select_set(currentSelection-1)
            self.ingredientList.event_generate("<<ListboxSelect>>")
            
            
    # Move an ingredient further down in the ingredient list
    def ingredientMoveDown(self):
   
        #####################################################
        # Bug: when repeatedly pressing the down button,    #
        # every press after the first switches the order of #
        # the first ingredient with the second ingredient.  #
        #####################################################
   
        currentSelection = self.getIngredientSelection()
        if currentSelection == -1:
            return -1
        elif currentSelection < len(self.ingredients)-1:
            if currentSelection == self.activeIngredientID["lst"] or currentSelection + 1 == self.activeIngredientID["lst"]:
                if not self.msgCaution("Reordering the actively loaded ingredient could cause duplicate and deleted entries when saving.  Continue?"):
                    return
            print("ingredient %d down\n\n" % currentSelection)
            
            self.ingredients[currentSelection] = self.ingredients[currentSelection][0:-1] + (self.ingredients[currentSelection][-1]+1,)
            self.ingredients[currentSelection+1] = self.ingredients[currentSelection+1][0:-1] + (self.ingredients[currentSelection+1][-1]-1,)
            
            self.populateIngredientList(self.ingredients)
            
            self.ingredientList.select_set(currentSelection+1)
            self.ingredientList.event_generate("<<ListboxSelect>>")
    
    
    # Add an ingredient slot to the bottom of the list
    def ingredientAdd(self):
        if self.activeRecipeID["lst"] == None:
            self.msgWarning("No recipe loaded.")
        else:
            blankIngredient = (None, self.activeRecipeID["db"], "blank", "?", "?", len(self.ingredients))
            self.ingredients.append(blankIngredient)
                
            self.populateIngredientList(self.ingredients)
            
            
            self.ingredientLoadInfo(len(self.ingredients)-1)
    
    
    # Delete the currently selected ingredient
    def ingredientDelete(self):
        
        #######################################################
        # BUG: when pressing the delete button several times, #
        # all but the first press just deletes the first      #
        # ingredient in the list.                             #
        #######################################################
        
        currentSelection = self.getIngredientSelection()
        if currentSelection == -1 or self.activeRecipeID["lst"] == None:
            return -1
        elif currentSelection < len(self.ingredients) and currentSelection >= 0:
            print("remove ingredient %d\n\n" % currentSelection)
            
            del self.ingredients[currentSelection]
            
            for ingredient in range(currentSelection,len(self.ingredients)):
                self.ingredients[ingredient] = self.ingredients[ingredient][0:-1] + (self.ingredients[ingredient][-1]-1,)
                
            self.populateIngredientList(self.ingredients)
            
            self.ingredientList.select_set(currentSelection)
            self.ingredientList.event_generate("<<ListboxSelect>>")
            
            print(self.ingredients)
    
    
    # Display help: about dialogue
    def helpAbout(self):
        print("Digital Cookbook v1.0 - Theodore Lindsey")
        aboutDialog = Toplevel()
        aboutDialog.geometry("200x100+300+300")
        aboutDialog.title("About Digital Cookbook")
        Message(aboutDialog, text="Digital Cookbook v1.0\nTheodore Lindsey").pack(side=TOP,fill=BOTH, expand=1)
        Button(aboutDialog, text="Ok", command=aboutDialog.destroy).pack(side=TOP)
        
    
    # Import recipe from XML file - need to implement
    def xmlImport(self):
        print("Importing XML file...")
        
    
    # add a recipe to the database and create a blank space for the recipe to go - need to implement
    def recipeAdd(self):
        print("Adding recipe...")
        
    
    # delete the currently selected recipe - need to implement
    def recipeDelete(self):
        recipeID = self.recipeList.curselection()
        print(recipeID)
        if len(recipeID) == 0:
            self.msgError("No recipes selected.")
            return
        elif len(recipeID) > 1:
            if not askokcancel("Caution!", "Are you sure you want to delete these %d recipes?" % len(recipeID)):
                return
            print("\nDeleting %d recipes..." % len(recipeID))
        else:
            if not askokcancel("Caution!", "Are you sure you want to delete this recipe?"):
                return
            print("\nDeleting recipe %d..." % recipeID)
            
        blankrecipe = ((None, '', None, '', '', '', '', ''), [])
        self.recipeLoad(blankrecipe)
        
    
    # load currently selected recipe
    def recipeLoad(self, recipe=None):
        activeSelection = self.getRecipeSelection()
        
        if activeSelection == -1:
            return -1
        elif len(activeSelection) > 1:
            self.msgError("Too many recipes selected.")
            return -1
        else:
            if recipe == None:
                listID = activeSelection[0]
                
                self.activeRecipeID["lst"] = listID
                self.activeRecipeID["db"] = self.recipes[listID][0]
                
                print(self.activeRecipeID)
                
                recipe = self.getRecipeInfo(self.activeRecipeID["db"])
            else:
                print("Clearing recipe info...")
                self.activeRecipeID = {"lst": None, "db": None}
                self.ingredientLoadInfo(-1)
            print(recipe)
            name = recipe[0][1]
            servings = recipe[0][2]
            prepTime = recipe[0][3]
            prepTimeUnits = recipe[0][4]
            cookTime = recipe[0][5]
            cookTimeUnits = recipe[0][6]
            procedure = recipe[0][7]
            self.ingredients = recipe[1]
            
            self.recipeName.delete(0,END)
            self.recipeName.insert(END, name)
            
            self.prepTime.delete(0,END)
            self.prepTime.insert(END, prepTime)
            
            self.cookTime.delete(0,END)
            self.cookTime.insert(END, cookTime)
            
            self.populateIngredientList(self.ingredients)
                
            self.procedure.delete(0.0,END)
            self.procedure.insert(END, procedure)
        
    
    # save changes to active recipe to database
    def recipeSave(self,event=""):
        print(self.activeRecipeID)
        
        if self.activeRecipeID["lst"] == None:
            self.msgError("No active recipe to save.")
            return -1
        
        
        listID = self.activeRecipeID["lst"]
        dbID = self.activeRecipeID["db"]
        
        name = self.recipeName.get()
        servings = 0#self.recipes[listID][2]
        prepTime = self.prepTime.get()
        prepUnit = None#self.prepTimeUnit.????()
        cookTime = self.cookTime.get()
        cookUnit = None#self.cookTimeUnit.????()
        procedure = self.procedure.get(0.0, END)
    
        recipeInfo = (dbID, name, servings, prepTime, prepUnit, cookTime, cookUnit, procedure)
        
        recipe = (recipeInfo, self.ingredients) 
        
        self.recipes[listID] = (dbID, name)
        
        self.populateRecipeList(self.recipes)
        
    
    # quit the program
    def onExit(self,event=""):
        print("Quitting...")
        sys.exit(0)
        
    
    # Create the UI layout
    def initUI(self):
      
        self.parent.title("Digital Cookbook")
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
        filemenu.add_command(label="Load recipe", command=self.recipeLoad)
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
        bEditRecipe = Button(frameToolbar, text="Load Recipe", command=self.recipeLoad, width=buttonwidth)
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
        # ==== Recipe List box ====
        recipeListScroll = Scrollbar(frameRecipeBox, orient=VERTICAL)
        self.recipeList = Listbox(frameRecipeBox, selectmode=EXTENDED, yscrollcommand=recipeListScroll.set)
        self.recipeList.pack(side=LEFT, fill=BOTH, expand=1)
        recipeListScroll.config(command=self.recipeList.yview)
        recipeListScroll.pack(side=RIGHT, fill=Y)
        
        self.getReciepList()
        self.populateRecipeList(self.recipes)
        
        
        # Spacer
        frameSpacer1 = Frame(self, borderwidth=1, width=10)
        frameSpacer1.pack_propagate(0)
        frameSpacer1.pack(side=LEFT, fill=Y)
        
        # Recipe info section
        frameRecipeInfo = Frame(self, borderwidth=1, width=200)
        frameRecipeInfo.pack_propagate(0)
        frameRecipeInfo.pack(side=LEFT, fill=Y)
        # Recipe name
        Label(frameRecipeInfo, text="Recipe Name:", anchor=E, justify=LEFT).pack()
        self.recipeName = Entry(frameRecipeInfo)
        self.recipeName.pack(side=TOP, fill=X)
        # Prep Time
        framePrepTime = Frame(frameRecipeInfo)
        framePrepTime.pack(side=TOP, fill=X)
        Label(framePrepTime, text="Prep Time:", anchor=E, justify=LEFT).pack()
        self.prepTime = Entry(framePrepTime)
        self.prepTime.pack(side=LEFT, fill=X)
        default = StringVar(framePrepTime)
        default.set("----")
        self.prepTimeUnit = OptionMenu(framePrepTime, default,"----","Min","Hr")
        self.prepTimeUnit.pack(side=RIGHT, fill=X)
        # Cook Time
        frameCookTime = Frame(frameRecipeInfo)
        frameCookTime.pack(side=TOP, fill=X)
        Label(frameCookTime, text="Cook Time:", anchor=E, justify=LEFT).pack()
        self.cookTime = Entry(frameCookTime)
        self.cookTime.pack(side=LEFT, fill=X)
        default = StringVar(frameCookTime)
        default.set("----")
        self.cookTimeUnit = OptionMenu(frameCookTime, default,"----","Min","Hr")
        self.cookTimeUnit.pack(side=RIGHT, fill=X)
        
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
        self.ingredientName = Entry(frameIngredients)
        self.ingredientName.pack(side=TOP, fill=X)
        # Ingredient info
        frameIngredientQuantity = Frame(frameIngredients)
        frameIngredientQuantity.pack(side=TOP, fill=X)
        Label(frameIngredientQuantity, text="Ingredient Quantity (value, unit):", anchor=E, justify=LEFT).pack()
        self.ingredientQuantity = Entry(frameIngredientQuantity)
        self.ingredientQuantity.pack(side=LEFT, fill=X, expand=1)
        self.ingredientUnit = Entry(frameIngredientQuantity, width=20)
        self.ingredientUnit.pack_propagate(0)
        self.ingredientUnit.pack(side=RIGHT, fill=X)
        # Spacer
        frameSpacer3 = Frame(frameIngredients, height=10)
        frameSpacer3.pack_propagate(0)
        frameSpacer3.pack(side=TOP, fill=X)
        # Ingredient List buttons
        frameIngredientButtons = Frame(frameIngredients)
        frameIngredientButtons.pack(side=TOP, fill=X)
        ingredientAdd = Button(frameIngredientButtons, text="+", command=self.ingredientAdd, width=3)
        ingredientAdd.pack(side=LEFT)
        ingredientDel = Button(frameIngredientButtons, text="-", command=self.ingredientDelete, width=3)
        ingredientDel.pack(side=LEFT)
        ingredientUp = Button(frameIngredientButtons, text=u"\u25B2", command=self.ingredientMoveUp, width=3)
        ingredientUp.pack(side=LEFT)
        ingredientDwn = Button(frameIngredientButtons, text=u"\u25BC", command=self.ingredientMoveDown, width=3)
        ingredientDwn.pack(side=LEFT)
        ingredientLoad = Button(frameIngredientButtons, text="Load", command=self.ingredientLoadInfo)
        ingredientLoad.pack(side=LEFT)
        ingredientSave = Button(frameIngredientButtons, text="Save", command=self.ingredientSaveInfo)
        ingredientSave.pack(side=LEFT)
        # Ingredient List Box Frame
        frameIngredientList = Frame(frameIngredients, relief=RAISED, borderwidth=1)
        frameIngredientList.pack(side=TOP, fill=BOTH, expand=1)
        # Ingredient List box
        ingredientListScroll = Scrollbar(frameIngredientList, orient=VERTICAL)
        self.ingredientList = Listbox(frameIngredientList, selectmode=SINGLE, yscrollcommand=ingredientListScroll.set) #Set selectmode=SINGLE????
        self.ingredientList.pack(side=LEFT, fill=BOTH, expand=1)
        ingredientListScroll.config(command=self.ingredientList.yview)
        ingredientListScroll.pack(side=RIGHT, fill=Y)
        
        # Spacer
        frameSpacer4 = Frame(self, borderwidth=1, width=10)
        frameSpacer4.pack_propagate(0)
        frameSpacer4.pack(side=LEFT, fill=Y)
        
        
        # Recipe Procedure
        frameProcedure = Frame(self, borderwidth=1)
        frameProcedure.pack(side=LEFT, fill=BOTH, expand=1)
        Label(frameProcedure, text="Procedure", anchor=E, justify=LEFT).pack(side=TOP)
        procedureScroll = Scrollbar(frameProcedure, orient=VERTICAL)
        self.procedure = Text(frameProcedure, maxundo=30, undo=1, wrap=WORD, yscrollcommand=procedureScroll.set)
        self.procedure.pack(side=LEFT, fill=BOTH, expand=1)
        procedureScroll.config(command=self.procedure.yview)
        procedureScroll.pack(side=LEFT, fill=Y)
        
    
    # placeholder function for unimplemented UI elements
    def placeholder(self):
        print("Coming soon!")
        
        


def main():
  
    root = Tk()
    root.geometry("1400x680+300+300")
    root.minsize(1400,350)
    app = windowFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()  