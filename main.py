from pokemondeluxe import Pokemon
import time 
import random as rd
import requests as rq
import pandas as pd
#https://github.com/lgreski/pokemonData
import numpy

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


def time():
    for i in range (3):
        print('.')
        time.sleep(0.5)
        
        
print('Welcome to the world of pokémon!')
time.sleep(0.5)
print('My name is Oak! People call me the pokémon Prof!')
time.sleep(0.5)
print('This world is inhabited by creatures called pokémon!')
time.sleep(0.5)
print('You are born in the region of kjhsu(pronounced kuh-jh-soo), the nexus and recently prospering region between the regions')
time.sleep(1.5)
print('Kanto, Johto, Hoenn, Sinnoh, Unova')
time.sleep(1)
print("After years of research I have collected numerous pokemon and taken immense care of them")
time()
print("I would like you to have one of these well-sought Pokemon, who would you choose to keep with you for this journey?")
time()
print("The grass-type")
time()
print("The fire-type")
time()
print("The water-type")




    
    


