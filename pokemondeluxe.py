from bs4 import BeautifulSoup
import requests

pokemon_logged = []
class Pokemon:
    def __init__(self, hp, moves: dict,weakness,type1,type2 = None, level = 5, defense ,spatk,spdef,speed,evolution:dict,name,attack):

        self.hp = hp
        self.type1 = type1
        self.weakness = weakness
        self.moves = moves
        self.level = level
        self.evolution = evolution
        self.attack = attack
        self.defense = defense
        self.spatk = spatk
        self.spdef = spdef
        self.speed = speed
        self.name = name
        self

    #need a repr like function to check if the pokemon needs to evolve or not according to level

def evolution_log_error(poki,pokemon_logged = pokemon_logged):
    span_tag = poki.find('span', class_ = 'infocard-lg-data text-muted')
    name = span_tag.find('a', class_ = 'ent-name').text.strip()
    if name in pokemon_logged:
        return True
    return False


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
    





        


        



        
        
        