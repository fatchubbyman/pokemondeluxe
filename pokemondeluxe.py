#                                                                  ideas/scrapped ideas
#make all the areas of the pokemon game we wanna have in the game
#webscrape from https://pokemondb.net/ and get all the data for all the stats of the pokemon
#learn how to use classes and check if we can make more methods(functions) to use in game like the items ability
#this time expand to more regions(maybe contain 4-5 regions in this game!?)
#we are learning to use objects classes web scraping and using a variety of functions to make this game
# get a way to get out an input prompt everytime and ask what to do, we will have the most amount 0f functions ever
# a battle mode, a more normal prompt mode asking you what to do, wild pokemon fight mode, buying mode, starting mode to select pokemon
import pandas as pd




df = pd.read_csv('Pokemon.csv')
class Pokemon:
    def __init__(self,sp_attack: int,sp_defense: int,hp: int,speed : int,name : str,attack : int ,defense : int,exp:int,type1 :str,type2:str,total: int):
        self.name = name
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.hp = hp
        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.type1 = type1
        self.type2 = type2
        self.total = total
        
    def Protein(self):
        self.hp += 10
        print("Your %s has a new base HP of %d" % (self.name,self.attack))
    
    def Calcium(self):
        self.sp_attack += 10
        print("Your %s has a new base Sp.Attack of %d" % (self.name,self.sp_attack))
    
    def HP_Up(self):
        self.hp += 10
        print("Your %s has a new base HP of %d" % (self.name,self.hp))
    
    def Carbos(self):
        self.speed += 10
        print("Your %s has a new base speed of %d" % (self.name,self.speed))
        
    def Zinc(self):
        self.sp_defense += 10
        print("Your %s has a new base SP.Defense of %d" % (self.name,self.sp_defense))
    
    def Iron(self):
        self.defense += 10
        print("Your %s has a new base defense of %d" % (self.name,self.defense))
        



        
        
        