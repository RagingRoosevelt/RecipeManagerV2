import xml.etree.ElementTree as ET
import os.path as path
import sqlite3 as sql
import random 

class Model:
    
    
    # Initialize database if it doesn't exist.
    def __init__(self):
        dbname = path.join(path.dirname(path.abspath(__file__)),'recipes.db')
        
        nodb = True
        if not path.isfile(dbname):
            print("warning: Recipe database not found, creating new database at %s\n" % str(dbname))
            nodb = True
        
        try:
            self.dbConnection = sql.connect(dbname)
        except:
            print("error: Problem creating or connecting to the database %s\n" % str(dbname))
            quit()
            
        self.dbCursor = self.dbConnection.cursor()
        if nodb == True:
            self.dbCursor.executescript("""
                DROP TABLE IF EXISTS Recipes;
                CREATE TABLE Recipes (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Servings INTEGER, PrepTime INTEGER, PrepTimeUnit TEXT, CookTime INTEGER, CookTimeUnit TEXT, CookTemp INTEGER, CookTempUnit TEXT);
                """)
    
    # check if "filename" is an XML file
    def isXML(self, filename):
        try:
            ET.parse(filename)
            return 1
        except:
            return -1
            
    # add recipe to the database
    def dbAddRecipe(self, recipe):
        #print(recipe)
        name = recipe['name']
        servings = recipe['servings']
        prepTime, prepTimeUnit = recipe['prep']
        cookTime, cookTimeUnit, cookTemp, cookTempUnit = recipe['cook']
        #procedure = recipe['procedure']
        
        print("Adding recipe %s" % name)
        self.dbCursor.execute("INSERT INTO Recipes VALUES(?,?,?,?,?,?,?,?,?);", (None, name, servings, prepTime, prepTimeUnit, cookTime, cookTimeUnit, cookTemp, cookTempUnit))
        self.dbConnection.commit()
        
    # gets recipe by name
    def dbGetRecipe(self, recipeName):
        for row in self.dbCursor.execute("SELECT * FROM Recipes WHERE Name =:recipeName", {"recipeName": recipeName}):
            print(row)
    
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

#recipes = model.xmlImport(path.join(dir,"several.xml"))
recipes = model.xmlImport(path.join(dir,"Baked Ziti.xml"))
recipes = model.xmlImport(path.join(dir,"Banana Bread.xml"))
recipes = model.xmlImport(path.join(dir,"Chocolate-Candy Cane Cake.xml"))

if recipes != -1:
    for recipe in recipes:
        print()
        #print(recipe + ":\n" + str(sorted(recipes[recipe].items())))
        #print(recipe + ":\n" + str(recipes[recipe]))
        
model.dbGetRecipe("Baked Ziti")

