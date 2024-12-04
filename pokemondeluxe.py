from bs4 import BeautifulSoup
import requests

pokemon_logged = []
class Pokemon:
    def __init__(self, hp: int, moves: dict,weakness:list,type1:str, spatk: int ,spdef: int,speed: int,evolution:dict,name: str,attack: int,defense: int,evolution_level,type2 = None, level = 5,moveset={}):

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

    #need a repr like function to check if the pokemon needs to evolve or not according to level

def evolution_log_error(poki,pokemon_logged = pokemon_logged):
    span_tag = poki.find('span', class_ = 'infocard-lg-data text-muted')
    name = span_tag.find('a', class_ = 'ent-name').text.strip()
    if name in pokemon_logged:
        return True
    return False

def weakness_logger(type1,type2 = None):
    pass

def evolution_line_logger():
    pass

def evolving_checker()

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
    types = rsoup.find_all()








        


        



        
        
        