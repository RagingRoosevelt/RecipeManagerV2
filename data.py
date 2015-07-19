import xml.etree.ElementTree as ET
import os.path as path
import sqlite3 as sql
import random 

class Model:
    # Initialize database if it doesn't exist.
    def __init__(self):
        dbname = path.join(path.dirname(path.abspath(__file__)),'recipes.db')
        
        # If the db file doesn't exist, we'll have to create a db
        if not path.isfile(dbname):
            print("warning: Recipe database not found, creating new database file at %s..." % str(dbname))
            nodb = True
        else:
            nodb = True
        
        # check if we can connect to the db (is it corrupt?)
        try:
            self.dbConnection = sql.connect(dbname)
        except:
            print("error: Problem creating or connecting to the database %s\n" % str(dbname))
            quit()
            
        # establish the db cursor
        self.dbCursor = self.dbConnection.cursor()
        
        # If we're creating the db from scratch, we'll need to initialize the necessary tables and fields
        if nodb == True:
            print("Initializing recipe database...")
            self.dbCursor.executescript("""
                DROP TABLE IF EXISTS Recipes;
                CREATE TABLE Recipes (
                    RecipeID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Name TEXT, 
                    Servings INTEGER, 
                    PrepTime INTEGER, 
                    PrepTimeUnit TEXT, 
                    CookTime TEXT, 
                    CookTimeUnit TEXT, 
                    CookTemp TEXT, 
                    CookTempUnit TEXT);
                """)
            print("Initializing ingredient database...")
            self.dbCursor.executescript("""
                DROP TABLE IF EXISTS Ingredients;
                CREATE TABLE Ingredients (
                    IngredientID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    RecipeID INT, 
                    Name TEXT, 
                    Quantity TEXT, 
                    Unit TEXT,
                    FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID));
                """)
            print()
            

    # check if "filename" is an XML file
    def isXML(self, filename):
        try:
            ET.parse(filename)
            return 1
        except:
            return -1


    # get user input
    def getUserChoice(self,message,choices=("Y","N")):
        
        usrInput = input(message)
        while usrInput.upper() not in choices:
            print("error: Input is not one of the accepted inputs: " + str(choices))
            usrInput = input(message)
        return usrInput


    # add recipe to the database
    def dbAddRecipe(self, recipe):
        canwrite = True
    
        # Assemble recipe metadata
        name = recipe['name']
        servings = recipe['servings']
        prepTime, prepTimeUnit = recipe['prep']
        cookTime, cookTimeUnit, cookTemp, cookTempUnit = recipe['cook']
        # Assemble ingredient info
        ingredients = []
        for ingredient in recipe['ingredients']:
            ingredients.append(recipe['ingredients'][ingredient])
        '''procedure = recipe['procedure']'''
        
        # check for the existence of entry to be updated
        self.dbCursor.execute("SELECT RecipeID FROM Recipes WHERE Name =:name", {"name": name})
        entry = self.dbCursor.fetchone()
        if entry is not None:
            print("\nwarning: A recipe already exists under that name.  Please either rename the recipe you are trying to import or delete the recipe that is already in the database.\n")
            canwrite = False
            
        
        # Insert the recipe
        if canwrite == True:
            print("\nAdding recipe %s..." % name)
            # Insert recipe metadata
            self.dbCursor.execute("INSERT INTO Recipes VALUES(?,?,?,?,?,?,?,?,?);", (None, name, servings, prepTime, prepTimeUnit, cookTime, cookTimeUnit, cookTemp, cookTempUnit))
            # Insert ingredients
            recipeID = self.dbCursor.lastrowid
            for ingredient in ingredients:
                self.dbCursor.execute("INSERT INTO Ingredients VALUES (?,?,?,?,?);", (None, recipeID) + ingredient)
            self.dbConnection.commit()
        

    # gets recipe by name
    def dbGetRecipe(self, recipeName):
        self.dbCursor.execute("SELECT * FROM Recipes WHERE Name =:recipeName", {"recipeName": recipeName})
        return self.dbCursor.fetchone()


    # reads XML file, "filename", and returns a nested dictionary containing all recipes found in the XML file
    def xmlRead(self,filename):
        if self.isXML(filename) < 1:
            print("error: provided file is not and XML file!\n")
            quit()
            return -1
        else:
            recipes = {}
            tree = ET.parse(filename)
            root = tree.getroot()

            for recipe in root.findall('recipe'):
                #print(recipe.attrib)
                
                attributes = {}
                attributes['name'] = recipe.attrib['name']
                
                for attrib in recipe:
                    if attrib.tag == "prep":
                        attributes["prep"] = (attrib.attrib['time'], attrib.attrib['unit'])
                    elif attrib.tag == "cook":
                        attributes["cook"] = (attrib.attrib['time'], attrib.attrib['timeUnit'], attrib.attrib['temp'], attrib.attrib['tempUnit'])
                    elif attrib.tag == "ingredients":
                        ingredients = {}
                        for ingredient in attrib:
                            ingredients[len(ingredients)] = (ingredient.get("name"), ingredient.get("quantity"), ingredient.get("unit"))
                        attributes["ingredients"] = ingredients
                    else:
                        attributes[attrib.tag] = attrib.text
                        #print(part.tag + " " + str(part.text))
                    
                        
                #print(sorted(attributes.items()))
                recipes[recipe.attrib["name"]] = attributes

            #for recipe in recipes:
            #    print(recipe + ":\n" + str(sorted(recipes[recipe].items())))
                
            return recipes


    # for a given XML file, imports the recipes from the file into the database (using xmlRead to parse the file)
    def xmlImport(self,filename):
        recipes = self.xmlRead(filename)
        
        #print(recipes)
        
        for name, recipe in recipes.items():
            self.dbAddRecipe(recipe)
        return recipes
    
dir = "E:\\Dropbox\\Documents\\Programming\\Cookbook Maker V2\\recipes"

model = Model()

recipes = model.xmlImport(path.join(dir,"Baked Ziti.xml"))
recipes = model.xmlImport(path.join(dir,"Banana Bread.xml"))
recipes = model.xmlImport(path.join(dir,"Chocolate-Candy Cane Cake.xml"))
recipes = model.xmlImport(path.join(dir,"Chocolate-Candy Cane Cake.xml"))
        
#print("\n" + str(model.dbGetRecipe("Baked Ziti")))

recipe = model.xmlRead(path.join(dir,"Salmon Chowder.xml"))['Salmon Chowder']
#recipe['name'] = "Chocolate-Candy Cane Cake"
model.dbAddRecipe(recipe)
