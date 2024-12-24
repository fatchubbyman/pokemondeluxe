#                                things left to do
# checkpoints
# clean_up_crew
# exp ups depending on pokemon defeated
# play the route again after losing
# starter pokemon choice
# bill's PC
# sequences of routes
# pokemart?

from bs4 import BeautifulSoup
import requests
import random as rd
import matplotlib.pyplot as plt                  # for showing hp of every pokemon after every battle
import time
import datetime                  #for day care center
your_pokemon = {}
global money
money = 10000
global pokeballs
pokeballs = 6

class MyPokemon:
    def __init__(self, base_hp: int,type1:str,
                 exp_type:str,evolution:dict,name: str,iv:int,hp :int,evolution_level:int,base_speed : int,base_atk:int,base_defense:int,base_spatk:int
                 ,base_spdef:int,type2 = None, level = 5,moveset={},exp = 0):

        self.base_hp = base_hp
        self.max_hp = max_hp(base = base_hp,level = level,iv = iv)
        self.hp = hp
        self.type1 = type1
        self.type2 = type2
        self.moveset = moveset
        self.level = level
        self.evolution = evolution
        self.evolution_level = evolution_level
        self.base_atk = base_atk
        self.attack = attack_finder(base = base_atk,level = level,iv = iv)
        self.base_defense = base_defense
        self.defense = defense_finder(base = base_defense)
        self.base_spatk = base_spatk
        self.spatk = spatk_finder(base = base_spatk,level = level, iv = iv)
        self.base_spdef = base_spdef
        self.spdef = spdef_finder(base = base_spdef)
        self.base_speed = base_speed
        self.speed = speed_finder(base = base_speed)
        self.name = name
        self.exp = exp 
        self.exp_type = exp_type
        self.exp_cap = exp_cap_changer(level = level,typee = exp_type)
        self.iv = rd.randrange(20,32)
        self.fainted = fainted_check(hp = hp)
    

    def level_up(self):
        if self.exp >= self.exp_cap:  # Check if experience is enough to level up
            self.level += 1
            self.exp = (self.exp_cap-self.exp)              # Reset experience after leveling up


    def evolve(self):
        url = 'https://pokemondb.net/evolution'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        evolution_blocks = soup.find_all('div', class_='infocard-list-evo')
        for block in evolution_blocks:
            pokemons = block.find_all('div', class_='infocard')
            for i, pokemon in enumerate(pokemons):
                name_tag = pokemon.find('a', class_='ent-name')
                if name_tag and name_tag.text.strip() == self.name:
                    evolution_arrow = block.find('span', class_='infocard-arrow')
                    if evolution_arrow:
                        level_tag = evolution_arrow.find('small')
                        if level_tag and 'Level' in level_tag.text:
                            required_level = int(level_tag.text.replace('(Level ', '').replace(')', ''))
                            if self.level >= required_level and i + 1 < len(pokemons):
                                next_pokemon = pokemons[i + 1].find('a', class_='ent-name').text.strip()
                                print(f'Congratulations your {self.name} has evolved!')
                                wait()
                                del your_pokemon[self.name]
                                self.name = next_pokemon
                                print(f'It is now a {self.name}!')
                                your_pokemon[self.name] = pokemon_caught(name = self.name,level = self.level)
                                return
                            return

            

class Moves:
    def __init__(self, typex, accuracy, power):
        self.typex = typex
        self.accuracy = accuracy
        self.power = power

    def damage(self, pokemon):
        effectiveness = effect_multiplier(move_type=self.typex, type1=pokemon.type1, type2=pokemon.type2)
        damage = self.power * effectiveness
        return damage

class Pokemon(MyPokemon):
    def __init__(self, base_hp, type1, exp_type, evolution, name, iv, hp, evolution_level, base_speed, base_atk, base_defense, base_spatk, base_spdef, type2=None, level=5, moveset={}, exp=0):
        super().__init__(base_hp, type1, exp_type, evolution, name, iv, hp, evolution_level, base_speed, base_atk, base_defense, base_spatk, base_spdef, type2, level, moveset, exp)
        del self.evolution 
        del self.iv
        del self.evolution_level
        del self.exp
        del self.exp_cap
        del self.exp_type
        del self.weaknesses
    

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

def fainted_check(pokemon):
    if pokemon.hp <= 0:
        return True
    return False

def max_hp(level,base_hp,iv):
    max_hp = ((2 * base_hp + iv) * level) // 100 + level + 10
    return max_hp

def attack_finder(level,iv,base_atk):
    attack = ((2 * base_atk + iv) * level) // 100 + 5
    return attack

def defense_finder(level,iv,base_defense):
    defense = ((2 * base_defense + iv) * level) // 100 + 5
    return defense

def spatk_finder(level, base_sp_attack, iv,):
    spatk = ((2 * base_sp_attack + iv) * level) // 100 + 5
    return spatk

def spdef_finder(level, base_sp_defense, iv):
    sp_def = ((2 * base_sp_defense + iv) * level) // 100 + 5
    return sp_def
    
def speed_finder(level, base_speed, iv):
    speed = ((2 * base_speed + iv) * level) // 100 + 5
    return speed

def effect_multiplier(move_type, type1, type2=None):
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

    effectiveness = 1

    if move_type in type_chart and type1 in type_chart[move_type]:
        effectiveness *= type_chart[move_type][type1]

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
        moveset[name] = Moves(typex=typee,accuracy = accuracy,power=power)

def hp_bar(current_hp, max_hp, bar_length=20):
    current_hp = max(0, min(current_hp, max_hp))
    hp_ratio = current_hp / max_hp
    filled_length = int(bar_length * hp_ratio)
    empty_length = bar_length - filled_length
    bar = "█" * filled_length + "-" * empty_length
    print(f"HP: [{bar}] {current_hp}/{max_hp}")

def your_pokemon_display(your_pokemon = your_pokemon):
    i = 1
    pokemon_alive = []
    for pokemon in your_pokemon.values():
        if pokemon.status is True:
            print(f'{i}. {pokemon.name}')
            hp_bar(current_hp=pokemon.hp,max_hp=pokemon.max_hp)
            print('')
            i += 1
            pokemon_alive.append(pokemon)
    return pokemon_alive

def pokemon_battling(pokemon,opp_pokemon):
    print(pokemon.name)
    hp_bar(max_hp=pokemon.max_hp,current_hp=pokemon.hp)
    print('.')
    print(opp_pokemon.name)
    hp_bar(max_hp=opp_pokemon.max_hp,current_hp=opp_pokemon.hp)


def clean_up_crew():      #impletments all the functions that need to be used after battling, like money,evolving_checker, plots the hp of pokemon
    evolving_checker(your_pokemon)
    pass

def evolving_checker(your_pokemon=your_pokemon):
    for keys,values in your_pokemon.items():
        if values.exp > values.exp_cap:
            values.level_up()
    for keys,values in your_pokemon.items():
        if values.level >= values.evolution_level:
            values.evolve()

def pokemon_logger(level, pokemon,moveset = {}):
    url = 'https://pokemondb.net/pokedex/' + pokemon.lower()
    rqsts = requests.get(url)
    soup = BeautifulSoup(rqsts.content,'lxml')
    stats_table = soup.find('div',class_ = 'grid-col span-md-12 span-lg-8')
    numbers = stats_table.find_all('td', class_ = 'cell-num')
    base_hp = int(numbers[0].text)
    base_attack = int(numbers[3].text)
    base_defense = int(numbers[6].text)
    base_spatk = int(numbers[9].text)
    base_spdef = int(numbers[12].text)
    base_speed = int(numbers[15].text)
    [type1,type2] = type_logger(soup)
    if moveset == {}:
        default_moves_logger(soup=soup,moveset=moveset) 
    opp_pokemon = Pokemon(name=pokemon,level=level,type1=type1,type2=type2,moveset=moveset,base_speed=base_speed,base_attack=base_attack,
                          base_defense=base_defense,base_hp = base_hp,base_spatk=base_spatk,base_spdef=base_spdef)
    return opp_pokemon 

def pokemon_caught(level, pokemon):
    url = 'https://pokemondb.net/pokedex/' + pokemon.lower()
    rqsts = requests.get(url)
    soup = BeautifulSoup(rqsts.content,'lxml')
    stats_table = soup.find('div' ,class_ = 'grid-col span-md-12 span-lg-8')
    numbers = stats_table.find_all('td', class_ = 'cell-num')
    base_hp = int(numbers[0].text)
    base_atk = int(numbers[3].text)
    base_defense = int(numbers[6].text)
    base_spatk = int(numbers[9].text)
    base_spdef = int(numbers[12].text)
    base_speed = int(numbers[15].text)
    [type1,type2] = type_logger(soup)
    iv = rd.randrange(20,32)
    trs = soup.find_all('tr')
    for tr in trs:
        if tr:
            th = tr.find('th')
            if th.text.strip() == 'Growth Rate':
                growth_rate = tr.find('td').text.strip()
                break
    exp_type = growth_rate
    return MyPokemon(level=level,base_hp=base_hp,type1=type1,type2=type2,spatk=base_spatk,spdef=base_spdef,speed=base_speed,atk=base_atk,defense=base_defense,iv=iv,exp_type=exp_type)


def plot_pokemon_hp(your_pokemon=your_pokemon):
    names = [pokemon.name for pokemon in your_pokemon.values()]
    hp_values = [pokemon.hp for pokemon in your_pokemon.values()]
    plt.figure(figsize=(10, 6))
    plt.bar(names, hp_values, color='lightgreen')
    plt.title('Pokemon HP Stats')
    plt.xlabel('Pokemon')
    plt.ylabel('HP')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def pokemon_center(your_pokemon=your_pokemon):
    print('Welcome to the Pokémon Center! ')
    for value in your_pokemon.values():
        value.hp = value.max_hp
    plot_pokemon_hp()

def pokeball_prompt(opp_pokemon,pokeballs = pokeballs):   
    prompt = input('Press Enter to throw a pokeball! ')
    if prompt == '' and pokeballs > 0:
        pokeballs -= 1
        for i in range(1, 4):
            print(i * '*')
            time.sleep(1)
        options = [True, False]
        probabilities = [0.9, 0.1]
        caught_or_not = rd.choices(options, probabilities)[0]
        if caught_or_not is True:
            print(f'Congratulations! You caught {opp_pokemon.name}.')
            your_pokemon[opp_pokemon.name] = pokemon_caught(pokemon=opp_pokemon.name,level=opp_pokemon.level)
        else:
            pokeball_prompt()
    else:
        print(f'{opp_pokemon.name} got away!')
        return 'quit'

def wild_battle(level,opponent_pokemon,your_pokemon = your_pokemon):
    opp_pokemon = pokemon_logger(opponent_pokemon=opponent_pokemon,level = level)
    print(f'A wild lvl. {opp_pokemon.level} {opp_pokemon.name} has appeared!')
    pokemon_alive = your_pokemon_display(your_pokemon)
    prompt = input('Which Pokemon would you like to pick? (Type the number of the pokemon/ type p for pokeball) ')
    if prompt.lower() == 'p':
        pass
    else:
        pokemon = pokemon_alive[int(prompt)-1]                              # the pokemon you selected
        print(f'Go out {pokemon.name}!')
        while True:
            status = pokemon_in_battle(pokemon= pokemon,opp_pokemon= opp_pokemon)
            if status == 'win':
                if pokeball_prompt(opp_pokemon=opp_pokemon) == 'quit':
                    return 'done'
                    

def move_stat_finder(href):
    url = 'https://www.serebii.net' + href
    rqsts = requests.get(url)
    soup = BeautifulSoup(rqsts.content,'lxml')
    dex_table = soup.find('table',class_ = 'dextable')
    type_tr = dex_table.find_all('tr')[1]
    typex = type_tr.find_all('td', class_ = 'cen')[1]
    a_tag = typex.find('a')
    typex = a_tag.get('href').replace('/attackdex-bw/','')
    typex = typex.replace('.shtml','').title()
    power_tr = dex_table.find_all('tr')[3]
    power = int(power_tr.find_all('td',class_ = 'cen')[1].text.strip())
    accuracy = int(power_tr.find_all('td',class_ = 'cen')[2].text.strip())
    return [typex,accuracy,power]
    
def trainer_battle(trainer,your_pokemon=your_pokemon):
    names_tr = trainer.find_all('tr')[1]
    levels_tr = trainer.find_all('tr')[2]
    moveset_tr = trainer.find_all('tr')[4]
    trainer_name = names_tr.find('td')
    print(f'{trainer_name.text.strip()} wants to battle!')
    pokemn = names_tr.find_all('td', align = 'center')
    trainer_pokemon = {}
    moveset = {}
    for i in range(len(pokemn)):
        name = pokemn[i].text.strip()
        level = int(levels_tr.find_all('td', class_ = 'level')[i])
        moveset = {}
        move_table = moveset_tr.find_all('td',class_ = 'bor')[i]
        attacks = move_table.find_all('a')
        for attack in attacks:
            name = attack.text.strip()
            href = attack.get('href')
            [typex,accuracy,power] = move_stat_finder(href)
            moveset[name] = Moves(typex=typex,accuracy=accuracy,power=power)
        trainer_pokemon[pokemon_logger(pokemon=name,level = level,moveset = moveset)]
    for value in trainer_pokemon.values():
        print(f'{trainer_name} sent out {value.name}!')
        pokemon_alive = your_pokemon_display(your_pokemon)
        prompt = int(input('Which Pokemon would you like to pick? (Type the number of the pokemon)'))
        pokemon = pokemon_alive[int(prompt)-1]  
        while True:
            status = pokemon_in_battle(pokemon=pokemon,opp_pokemon=value,wild=False)
            if status == 'fainted':
                pokemon_alive = your_pokemon_display(your_pokemon)
                prompt = int(input('Which Pokemon would you like to pick? (Type the number of the pokemon)'))
                pokemon = pokemon_alive[int(prompt)-1]
                continue
            elif status == 'win':
                del trainer_pokemon[value.name]
                break
        continue
    return 'won'

def pokemon_in_battle(pokemon, opp_pokemon, wild=True):
    if fainted_check(pokemon):
        print(f"Your {pokemon} fainted!")
        plot_pokemon_hp()
        return 'fainted'
    if fainted_check(opp_pokemon):
        print(f"{opp_pokemon} fainted!")
        plot_pokemon_hp()
        return 'win'
    if pokemon.speed >= opp_pokemon.speed:
        move = move_display(pokemon=pokemon)
        key_at_position = list(pokemon.moveset.keys())[move - 1]
        attack = pokemon.moveset[key_at_position]
        opp_pokemon.hp -= attack.damage(typex=attack.typex, pokemon=pokemon)
        pokemon_battling(pokemon=pokemon, opp_pokemon=opp_pokemon)
    else:
        opp_move = rd.choice(list(opp_pokemon.moveset.keys()))
        opp_move = opp_pokemon.moveset[opp_move]
        pokemon.hp -= opp_move.damage
        pokemon_battling(pokemon=pokemon, opp_pokemon=opp_pokemon)
    pokemon_in_battle(pokemon, opp_pokemon, wild)

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

def move_display(pokemon):
    for i in len(list(pokemon.moveset.keys())):
        print(list(pokemon.moveset.keys())[i])
    move = int(input('Which move do you want to choose? (Select the move no.) '))
    return move

def wait():
    for i in range(3):
        print('.')
        time.sleep(0.3)


games = {'kanto':'firered-leafgreen','unova':'black-white','sinnoh':'platinum','hoenn':'ruby-sapphire-emerald','alola':'sun-moon','kalos':'x-y','johto':'heartgold-soulsilver','galar':'sword-shield'}
game_choice = input('Which game would you like to play? (kanto,johto,hoenn,sinnoh,unova,kalos,alola,galar) ')
game_choice = game_choice.title()

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
for route in routes[1:]:         # need to get a sequence of routes which help the player to play smoothly
    route(route)

def route(location):
    print(location.text + ':')
    location_site = location.get('value')
    location_site = 'https://www.serebii.net' + location_site
    if 'kanto' in location_site:
        location_site.replace('/kanto','/kanto/3rd')
    elif 'sinnoh' in location_site:
        location_site.replace('/sinnoh','/sinnoh/4th')
    rqsts = requests.get(location_site)
    soup = BeautifulSoup(rqsts.content,'lxml')
    #wild pokemon
    while True:       # while loop keeps on asking if you want to battle against a pokemon and when youre done battling wild pokemon(another while loop should be in place for catching the pokemon) then starts a battle with a trainer's pokemon
        prompt = input('"Do you want to search for a Pokémon? The area around you seems full of potential hiding spots. (Yes/No)"')
        if prompt.lower() != 'yes':
            break
        anctab = location.find('table', class_ = 'anctab')
        wild_pokemon_table = anctab.find_all_next('table',class_ =['extradextable', 'dextable'])
        wild_pokemon_table = wild_pokemon_table[1:]
        wild_pokemon = {}
        for table in wild_pokemon_table:
            names = table.find_all('td' , class_ = 'name')
            finding_rates = table.find_all('td', class_ = 'rate')
            levels = table.find_all('td', class_ = 'level')
            for name,finding_rate,level in zip(names,finding_rates,levels):
                level = level.strip("() ")
                x,y = map(int, level.split(' - '))
                wild_pokemon[name.text.strip()] = [int(((finding_rate.text.strip()).replace('%',''))),[x,y]]    #pidgey: 20%,5  #finding rate and level
        total_rate = sum(data[0] for data in wild_pokemon.values())
        normalized_rates = {name: (data[0] / total_rate) * 100 for name, data in wild_pokemon.items()}
        choices = list(normalized_rates.keys())
        weights = list(normalized_rates.values())
        while True:
            selected_pokemon = rd.choices(choices, weights=weights, k=1)[0]
            level = rd.randrange(wild_pokemon[selected_pokemon][1][0],wild_pokemon[selected_pokemon][1][1]+1)
            new_prompt = input(f"A wild level {level} {selected_pokemon} has appeared! Would you like to battle? (yes/no/out)")
            if new_prompt == 'out':
                break
            elif new_prompt != 'yes':
                continue
            done = wild_battle(opponent_pokemon=selected_pokemon,level= level)
            if done == 'done':
                break
        break
    #trainer battle 
    wait()
    trainers = location.find_all('table', class_ = 'trainer')
    if trainers is not None:
            for trainer in trainers:
                trainer = trainers.find('td', class_ = 'trainer')
                wait()
                trainer_battle(trainer=trainer)
                if trainer_battle == 'won':
                    trainers.remove(trainer)