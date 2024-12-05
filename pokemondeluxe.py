from bs4 import BeautifulSoup
import requests
import random as rd
import matplotlib    # for showing hp of every pokemon after every battle????

pokemon_logged = []
class Pokemon:
    def __init__(self, hp: int, moves: dict,weakness:list,type1:str, spatk: int ,spdef: int,speed: int,
                 exp_cap:int,exp_type:str,evolution:dict,name: str,attack: int,defense: int,evolution_level:int,
                 type2 = None, level = 5,moveset={},exp = 0):

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
        self.exp = exp 
        self.exp_type = exp_type
        self.exp_cap = exp_cap_changer(level = self.level,typee = self.exp_type)
    

    def level_up(self):
        if self.exp >= self.exp_cap:  # Check if experience is enough to level up
            self.level += 1
            self.exp = 0  # Reset experience after leveling up


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
    trs = rsoup.find_all('tr')
    for tr in trs:
        if tr:
            th = tr.find('th')
            if th.text.strip() == 'Growth Rate':
                growth_rate = tr.find('td').text.strip()
                break
    exp_type = growth_rate




    









        


        



        
        
        