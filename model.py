import xml.etree.ElementTree as ET
import os.path as path
import sqlite3 as sql

class Model:
    
    def __init__(self):
        dbname = path.join(path.dirname(path.abspath(__file__)),'recipes.db')
        
        nodb = True
        if not path.isfile(dbname):
            print("warning: Recipe database not found, creating new database at " + str(dbname))
            nodb = True
        
        try:
            self.dbConnection = sql.connect(dbname)
        except:
            print("error: Problem creating or connecting to the database " + str(dbname))
            quit()
            
        self.dbCursor = self.dbConnection.cursor()
        if nodb == True:
            self.dbCursor.executescript("""
                DROP TABLE IF EXISTS Recipes;
                CREATE TABLE Recipes (id INTEGER PRIMARY KEY, Name TEXT, Servings INTEGER, PrepTime INTEGER, PrepTimeUnit TEXT, CookTime INTEGER, CookTimeUnit TEXT, CookTemp INTEGER, CookTempUnit TEXT);
                INSERT INTO Recipes VALUES(1, 'Baked Ziti', 10, 0, '??', 35, 'min', 175, 'C');
                INSERT INTO Recipes VALUES(2, 'Banana Bread', 12, 0, '??', 1, 'hr', 350, 'F');
                """)
            
    
    # check if "filename" is an XML file
    def isXML(self, filename):
        try:
            ET.parse(filename)
            return 1
        except:
            return -1
            
    # add recipe to the database
    def dbAddRecipe(recipe):
        name = recipe['name']
        servings = recipe['servings']
        prepTime, prepTimeUnit = recipe['prep']
        cookTime, cookTimeUnit, cookTemp, cookTempUnit = recipe['cook']
        #procedure = recipe['procedure']
        
        self.dbCursor.execute("INSERT INTO RECIPES VALUES(?,?,?,?,?,?,?,?,?)", (ID, name, servings, prepTime, prepTimeUnit, cookTime, cookTimeUnit, cookTemp, cookTempUnit))
        
        
    
    # imports XML file, "filename", and returns a nested dictionary containing all recipes found in the XML file
    def xmlImport(self,filename):
        if self.isXML(filename) < 1:
            print("error: provided file is not and XML file!")
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
    
filename = "E:\\Dropbox\\Documents\\Programming\\Cookbook Maker Py\\recipes\\several.xml"
#filename = "E:\\Dropbox\\Documents\\Programming\\Cookbook Maker Py\\recipes\\Baked Ziti.xml"

model = Model()

recipes = model.xmlImport(filename)
if recipes != -1:
    for recipe in recipes:
        #print(recipe + ":\n" + str(sorted(recipes[recipe].items())))
        print(recipe + ":\n" + str(recipes[recipe]))

