from bs4 import BeautifulSoup
import requests
import random as rd
import matplotlib          # for showing hp of every pokemon after every battle????
import numpy as np

pokemon_logged = []
class Pokemon:
    def __init__(self, base_hp: int,weaknesses:list,type1:str, spatk: int ,spdef: int,speed: int,
                 exp_cap:int,exp_type:str,evolution:dict,name: str,iv:int,attack: int,defense: int,evolution_level:int,
                 type2 = None, level = 5,moveset={},exp = 0):

        self.base_hp = base_hp
        self.type1 = type1
        self.type2 = type2
        self.weaknesses = weaknesses
        self.moveset = moveset
        self.level = level
        self.evolution = evolution
        self.evolution_level = evolution_level
        self.attack = attack
        self.defense = defense
        self.spatk = spatk
        self.spdef = spdef
        self.speed = speed
        self.name = name
        self.exp = exp 
        self.exp_type = exp_type
        self.exp_cap = exp_cap_changer(level = self.level,typee = self.exp_type)
        self.iv = iv
    

    def level_up(self):
        if self.exp >= self.exp_cap:  # Check if experience is enough to level up
            self.level += 1
            self.exp = 0              # Reset experience after leveling up

class Moves:
    def __init__(self,typex,damage,accuracy,power,effectiveness = 1):
        self.typex = typex
        self.damage = damage
        self.effectiveness = effectiveness
        self.accuracy = accuracy
        self.power = power
    


def evolution_log_error(poki,pokemon_logged = pokemon_logged):
    span_tag = poki.find('span', class_ = 'infocard-lg-data text-muted')
    name = span_tag.find('a', class_ = 'ent-name').text.strip()
    if name in pokemon_logged:
        return True
    return False

def exp_cap_changer(level,typee):
    if typee == 'Erratic':
        if level < 50:
            exp_cap = ((level+1)**3)*(100 - (level+1))/50 - ((level**3)*(100 - level)/50)
        elif 68 > level >= 50:
            exp_cap = ((level+1)**3)*(150 - (level+1))/100 - ((level**3)*(150 - level)/100)
        elif 68 <= level < 98:
            exp_cap = ((level+1)**3)*((1911 - 10*(level+1))/3)/500 - ((level**3)*((1911 - 10*level)/3)/500)
        elif 100 > level >= 98:
            exp_cap = ((level+1)**3)*(160 - (level+1))/100 - ((level**3)*(160 - level)/100)
    elif typee == 'Fast':
        exp_cap = 4*((level+1)**3)/5 - 4*(level**3)/5
    elif typee == 'Medium Fast':
        exp_cap = (level+1)**3 - level**3
    elif typee == 'Medium Slow':
        exp_cap = 6/5*(level+1)**3 - 15*(level+1)**2 + 100*(level+1) - 140 - (6/5*(level)**3 - 15*(level)**2 + 100*(level) - 140)
    elif typee == 'Slow':
        exp_cap = 5*(((level+1)**3)/4) - (5*((level**3)/4))
    elif typee == 'Fluctuating':
        if level < 15:
            exp_cap = (((level+1)**3)*((level+1)+1/3) + 24)/50 - ((((level)**3)*((level)+1/3) + 24)/50)
        elif 36 > level >= 15:
            exp_cap = ((level+1)**3)*((level+1)+14)/50 - ((level**3)*(level+14)/50)
        elif 36 <= level < 100:
            exp_cap = ((level+1)**3)*(((level+1)/2)+32)/50 - (((level)**3)*(((level)/2)+32)/50)
    return exp_cap

def ellect_multiplier(move_type, type1, type2=None):
    type_chart = {
        'Normal': {'Rock': 0.5, 'Steel': 0.5, 'Ghost': 0},
        'Fighting': {'Normal': 2, 'Rock': 2, 'Steel': 2, 'Ice': 2, 'Dark': 2, 'Ghost': 0,
                     'Flying': 0.5, 'Poison': 0.5, 'Bug': 0.5, 'Psychic': 0.5, 'Fairy': 0.5},
        'Flying': {'Fighting': 2, 'Bug': 2, 'Grass': 2, 'Rock': 0.5, 'Steel': 0.5, 'Electric': 0.5},
        'Poison': {'Grass': 2, 'Fairy': 2, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0},
        'Ground': {'Poison': 2, 'Rock': 2, 'Steel': 2, 'Fire': 2, 'Electric': 2, 'Grass': 0.5, 'Bug': 0.5,
                   'Flying': 0},
        'Rock': {'Flying': 2, 'Bug': 2, 'Fire': 2, 'Ice': 2, 'Fighting': 0.5, 'Ground': 0.5, 'Steel': 0.5},
        'Bug': {'Grass': 2, 'Psychic': 2, 'Dark': 2, 'Fighting': 0.5, 'Flying': 0.5, 'Poison': 0.5,
                'Ghost': 0.5, 'Steel': 0.5, 'Fire': 0.5, 'Fairy': 0.5},
        'Ghost': {'Ghost': 2, 'Psychic': 2, 'Dark': 0.5, 'Normal': 0},
        'Steel': {'Rock': 2, 'Ice': 2, 'Fairy': 2, 'Steel': 0.5, 'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5},
        'Fire': {'Bug': 2, 'Steel': 2, 'Grass': 2, 'Ice': 2, 'Rock': 0.5, 'Fire': 0.5, 'Water': 0.5,
                 'Dragon': 0.5},
        'Water': {'Ground': 2, 'Rock': 2, 'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Dragon': 0.5},
        'Grass': {'Ground': 2, 'Rock': 2, 'Water': 2, 'Flying': 0.5, 'Poison': 0.5, 'Bug': 0.5,
                  'Steel': 0.5, 'Fire': 0.5, 'Grass': 0.5, 'Dragon': 0.5},
        'Electric': {'Flying': 2, 'Water': 2, 'Ground': 0, 'Grass': 0.5, 'Electric': 0.5, 'Dragon': 0.5},
        'Psychic': {'Fighting': 2, 'Poison': 2, 'Steel': 0.5, 'Psychic': 0.5, 'Dark': 0},
        'Ice': {'Flying': 2, 'Ground': 2, 'Grass': 2, 'Dragon': 2, 'Steel': 0.5, 'Fire': 0.5, 'Water': 0.5,
                'Ice': 0.5},
        'Dragon': {'Dragon': 2, 'Steel': 0.5, 'Fairy': 0},
        'Dark': {'Ghost': 2, 'Psychic': 2, 'Fighting': 0.5, 'Dark': 0.5, 'Fairy': 0.5},
        'Fairy': {'Fighting': 2, 'Dragon': 2, 'Dark': 2, 'Poison': 0.5, 'Steel': 0.5, 'Fire': 0.5},
    }

    # Default effectiveness
    effectiveness = 1

    # Check defender's primary type
    if move_type in type_chart and type1 in type_chart[move_type]:
        effectiveness *= type_chart[move_type][type1]

    # Check defender's secondary type (if applicable)
    if type2 and move_type in type_chart and type2 in type_chart[move_type]:
        effectiveness *= type_chart[move_type][type2]

    return effectiveness

def default_moves_logger(soup,moveset):
    move_table = soup.find('table' , class_ = 'data-table')
    trs = move_table.find_all('tr')
    for tr in trs[:4]:
        name = tr.find('td' , class_ = 'cell-name').text.strip()
        typee = tr.find('td' , class_ = 'cell-icon').text.strip()
        power = tr.find_all_next('td', class_ = 'cell-num')[0].text.strip()
        accuracy = tr.find_all_next('td', class_ = 'cell-num')[1].text.strip()
        effectiveness = effect_multiplier()   #this parameter will contain the object of the pokemon the player uses
        moveset[name] = Moves(typex=typee,accuracy = accuracy,power=power,effectiveness=effectiveness)

        

    

def evolution_line_logger(poki,name):
    evolutions = poki.find('div', class_ = 'infocard-list-evo') 
    names = evolutions.find_all('a', class_ = 'ent-name')
    for naam in names:
        if naam.text.strip() == name:
            continue
        link = 'https://pokemondb.net/pokedex/' + naam.text.strip()
        rqsts = requests.get(link)
        soup = BeautifulSoup(rqsts.content,'lxml')
        name = soup.find('h1')
        stats_table = soup.find('div' class_ = 'grid-col span-md-12 span-lg-8')
        numbers = stats_table.find_all('td', class_ = 'cell-num')
        hp = int(numbers[0].text)
        attack = int(numbers[3].text)
        defense = int(numbers[6].text)
        spatk = int(numbers[9].text)
        spdef = int(numbers[12].text)
        speed = int(numbers[15].text)
        [type1,type2] = type_logger(rsoup)
        pass

def evolving_checker():
    pass

def win():
    pass

def loss():
    pass

def battle(your_pokemon:dict,opponent_pokemon):       #get trainer data from https://www.serebii.net/pokearth/
    print(' '.join(your_pokemon.keys()) + ' /n Which Pokemon would you like to pick? ')

def type_logger(soup):
    pokedex_data = soup.find('div' , class_ = 'grid-col span-md-6 span-lg-4')
    types = pokedex_data.find_all('a')
    if len(types) > 1:
        type2 = types[1].text.strip()
        type1 = types[0].text.strip()
    else:
        type1 = types[0].text.strip()
        type2 = None
    return [type1,type2]

games = {'kanto':'firered-leafgreen','unova':'black-white','sinnoh':'platinum','hoenn':'ruby-sapphire-emerald','alola':'sun-moon','kalos':'x-y','johto':'heartgold-soulsilver','galar':'sword-shield'}
game_choice = input('Which game would you like to play? (kanto,johto,hoenn,sinnoh,unova,kalos,alola,galar) ')
game_choice = game_choice.title()
url = 'https://pokemondb.net/pokedex/game/' + games[game_choice.lower()]
rqsts = requests.get(url)
soup = BeautifulSoup(rqsts.content,'lxml')
pokemon_stats_filler = soup.find('div' , class_ = 'infocard-list infocard-list-pkmn-lg')
pokemon_stats_filler = pokemon_stats_filler.find_all('div', class_ = 'infocard ')
for poki in pokemon_stats_filler:
    if evolution_log_error(poki= poki) is True:
        continue
    span_tag = poki.find('span', class_ = 'infocard-lg-data text-muted')
    name = span_tag.find('a', class_ = 'ent-name').text.strip()
    href = name.get('href')
    name = name.text.strip()
    link = 'https://pokemondb.net/' + href
    rqsts = requests.get(link)
    rsoup = BeautifulSoup(rqsts.content,'lxml')
    stats_table = rsoup.find('div' class_ = 'grid-col span-md-12 span-lg-8')
    numbers = stats_table.find_all('td', class_ = 'cell-num')
    base_hp = int(numbers[0].text)
    attack = int(numbers[3].text)
    defense = int(numbers[6].text)
    spatk = int(numbers[9].text)
    spdef = int(numbers[12].text)
    speed = int(numbers[15].text)
    [type1,type2] = type_logger(rsoup)
    evolution_line_logger(poki = rsoup,name=name)
    trs = rsoup.find_all('tr')
    for tr in trs:
        if tr:
            th = tr.find('th')
            if th.text.strip() == 'Growth Rate':
                growth_rate = tr.find('td').text.strip()
                break
    exp_type = growth_rate
    weaknesses = weakness_logger(type1=type1,type2=type2)     #not USING THIS!!!!
    iv = rd.randrange(20,32)
    default_moves_logger(moveset = {},soup=rsoup)
    





location_site = 'https://www.serebii.net/pokearth/'
reachingout = requests.get(location_site)
region_soup = BeautifulSoup(reachingout.content,'lxml')
select_element = region_soup.find_all('select', {'name': 'SelectURL'})
for element in select_element:
    onchange_value = element.get('onchange')
    if game_choice.lower() in onchange_value:
        break
select_element = region_soup.find('select', onchange = onchange_value)
routes = select_element.find_all('option')
for route in routes[1:]:
    route()



def route(location = route):
    print(location.text + ':')
    location_site = location.get('value')
    location_site = 'https://www.serebii.net' + location_site
    if 'kanto' in location_site:
        location_site.replace('/kanto','/kanto/4th')
    elif 'sinnoh' in location_site:
        location_site.replace('/sinnoh','/sinnoh/4th')
    rqsts = requests.get(location_site)
    soup = BeautifulSoup(rqsts.content,'lxml')
    # you can either get a trainer or find wild pokemon(use while loops)
    #wild pokemon
    rd.randrange()

