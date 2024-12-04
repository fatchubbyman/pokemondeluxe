from bs4 import BeautifulSoup
import requests
import random as rd

pokemon_logged = []
class Pokemon:
    def __init__(self, hp: int, moves: dict,weakness:list,type1:str, spatk: int ,spdef: int,speed: int,evolution:dict,name: str,attack: int,defense: int,evolution_level:int,type2 = None, level = 5,moveset={}):

        self.hp = hp
        self.type1 = type1
        self.type2 = type2
        self.weakness = weakness
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

    def __repr__(self):
        if self.level > 


def evolution_log_error(poki,pokemon_logged = pokemon_logged):
    span_tag = poki.find('span', class_ = 'infocard-lg-data text-muted')
    name = span_tag.find('a', class_ = 'ent-name').text.strip()
    if name in pokemon_logged:
        return True
    return False

def weakness_logger(type1,type2 = None):
    pass

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
    hp = int(numbers[0].text)
    attack = int(numbers[3].text)
    defense = int(numbers[6].text)
    spatk = int(numbers[9].text)
    spdef = int(numbers[12].text)
    speed = int(numbers[15].text)
    [type1,type2] = type_logger(rsoup)
    evolution_line_logger(poki = rsoup,name=name)



    









        


        



        
        
        