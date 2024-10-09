from pokemondeluxe import Pokemon
import time 
import random as rd
import requests as rq
import pandas
#https://github.com/lgreski/pokemonData
import numpy
import pandas as pd

df = pd.read_csv('Pokemon.csv')

for i in range(0,152):
    name = df.at[i,'Name']
    type1 = df.at[i,'Type1']
    type2 = df.at[i,'Type2']
    Total = df.at[i,'Total']
    hp = df.at[i,'HP']
    attack = df.at[i,'Attack']
    defense = df.at[i,'Defense']
    sp_attack = df.at[i,'Sp. Atk']
    sp_defense = df.at[i,'Sp. Def']
    speed = df.at[i,'Speed']
    exp = 0
    df.at[i,'Name'] = Pokemon(name=name,type1=type1,type2=type2,total=Total,hp=hp,attack=attack,defense=defense,sp_attack=sp_attack,sp_defense=sp_defense,speed=speed,exp=0)

    
    
    


