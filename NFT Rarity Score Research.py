# imports

import os
import sys
import matplotlib.pyplot as plt

# functions

def get_data(nft_data: list) -> list:
    """
    Get new data from API
    Example call:
    get_data(nft_data)
    """
    traits = []
    token_ids = []
    for dictionary in nft_data:
        if dictionary['nft']['traits'] is None:
            print("x")
        else:
            traits.append(dictionary['nft']['traits'])
            token_ids.append(dictionary['nft']['identifier'])
    return traits, token_ids

def read_data() -> list:
    """
    Read data from text file
    Example call:
    read_data()
    """    
    import json
    traits = []
    token_ids = []
    data = {}
    filename = input("Please enter the filename you would like to read from: (add .txt at the end of the filename) - ")
    if os.path.exists(filename):
        infile = open(filename, "r")
        for line in infile:
            line = json.loads(line)
            if line['nft']['traits'] is None:
                print("x")
            else:
                traits.append(line['nft']['traits'])
                token_ids.append(line['nft']['identifier'])
                data[line['nft']['identifier']] = line['nft']['contract']
        return traits, token_ids, data            
    else:
        print("This file does not exist. Please rerun the program")
        sys.exit()

def sort_data(traits: list) -> dict:
    """
    Sorts data to determine counts of traits and trait_vales
    Example call:
    sort_data(traits)
    """    
    trait_data = {}
    trez = {}
    for lis in traits:
        for dic in lis: 
            trez[dic['trait_type']] = trez.get(dic['trait_type'], 0) +1
            if trait_data.get(dic['trait_type'])==None:
                trait_data[dic['trait_type']] = {}
            k = trait_data.get(dic['trait_type'])
            if k.get(dic['value'])==None:
                k[dic['value']] = 1
            else:            
                k[dic['value']] = k.get(dic['value'])+1
    return trait_data, trez

def missing_traits(traits: list, trez:dict) -> dict:
    """
    Finds missing traits and makes dictionary
    Example call:
    missing_traits(traits)
    """
    no_trez = {}    
    for lis in traits:
        x = []
        for dic in lis:
            
            x += [dic["trait_type"]]

        for key in trez:
            if key not in x:
                lis.append({'trait_type': "No " + key})
                
                no_trez["No " + key] = no_trez.get("No " + key, 0)+1
                         
    return no_trez

def trait_freq(traits: list, trez: dict, no_trez: dict) -> list: 
    """
    Calculates individual frequencies of traits based on if they exist or not
    Example call:
    trait_freq(traits, trez, no_trez)
    """
    freq = []
    for lis in traits:
        frequ = []
        for dic in lis:
            if dic["trait_type"] not in trez:
                frequ.append(no_trez[dic["trait_type"]]/len(traits))
            else:
                frequ.append(trez[dic["trait_type"]]/len(traits))
            freq.append(frequ)
    return freq

def trait_val_freq(traits: list, trait_data: dict, no_trez: dict) -> list:
    """
    Calculates individual frequencies of traits based on trait values
    Example call:
    trait_val_freq(traita, trez, no_trez)
    """  
    freq = []
    for lis in traits:
        frequ = []
        for dic in lis:
            if dic["trait_type"] not in trait_data:
                frequ.append(no_trez[dic["trait_type"]]/len(traits))
            else:
                frequ.append(trait_data[dic["trait_type"]][dic["value"]]/len(traits))
            freq+= [frequ]
    return freq
    
def harmonic(freq: list) -> list:
    """
    Calculates harmonic mean
    Example call:
    harmonic(freq)
    """
    harmonic_rar = []
    for lis in freq:
        sm = 0
        for f in lis:
            sm += 1/f
        harmonic_rar += [len(lis)/sm]
    return harmonic_rar

def geometric(freq: list) -> list:
    """
    Calculates geometric mean
    Example call:
    geometric(freq)
    """    
    geometric_rar = []
    for lis in freq:
        sm = 1
        for f in lis:
            sm *= f
        geometric_rar += [sm**(1/len(lis))]
    return geometric_rar

def arithmetic(freq: list) -> list:
    """
    Calculates arithmetic mean
    Rxample call:
    arithemtric(freq)
    """
    arithmetic_rar = []
    for lis in freq:
        sm = 0
        for f in lis:
            sm += f
        arithmetic_rar += [sm/len(lis)]
    return arithmetic_rar

def rarity (harmonic_rar: list) -> dict:
    """
    Calculates rarity scores
    Example call:
    rarity(harmonic_rar)
    """
    fre = {}
    for item in harmonic_rar:
        fre[item] = fre.get(item, 0) + 1/len(traits)
    fre = dict(sorted(fre.items()))
    return fre

def plot(fre_h: dict, fre_g: dict, fre_a: dict): 
    """
    Plots graph
    Example call:
    plot(fre)
    """
    fig2 = plt.figure()
    plt.title("Rarity scores vs freq")
    plt.ylabel("frequency")
    plt.xlabel("rarity scores")
    plt.plot(list(fre_h.keys()),list(fre_h.values()), label = "harmonic", color = "blue")
    plt.plot(list(fre_g.keys()),list(fre_g.values()), label = "geometric", color = "green")
    plt.plot(list(fre_a.keys()),list(fre_a.values()), label = "arithmetic", color = "red")
    plt.legend()
    plt.show()
    
# Script
data_choice = input("Would you like to generate new data or read previous data? Options: New/Read - ")

if data_choice == "Read":
    traits, token_ids, data = read_data()
else:
    import Opensea_API_saan
    slug = input("Slug:")
    data = Opensea_API_saan.load_data(slug)
    while data == {}:
        data = Opensea_API_saan.load_data()
    chain = input("Chain:")
    nft_data = Opensea_API_saan.nft_data(data, chain)
    price = Opensea_API_saan.price(data)    
    traits, token_ids = get_data(nft_data)

trait_data, trez = sort_data(traits)
no_trez = missing_traits(traits, trez)
    
calc = input("Would you like to do the calculations using the trait types or trait values? Options: Trait types/ Trait values - ") 
    
if calc == "Trait types":
    freq = trait_freq(traits, trez, no_trez)       
else:
    freq = trait_val_freq(traits, trait_data, no_trez)
    
harmonic_rar = harmonic(freq)
geometric_rar = geometric(freq)
arithmetic_rar = arithmetic(freq)
fre_h = rarity(harmonic_rar)
fre_g = rarity(geometric_rar)
fre_a = rarity(arithmetic_rar)
plot(fre_h, fre_g, fre_a)
    

print("Getting token ids with rarity scores")
id_rar = {}
for i in range(0, len(token_ids)): 
    id_rar[token_ids[i]] = [harmonic_rar[i], geometric_rar[i], arithmetic_rar[i]]
print("{token id: [harmonic, geometric, arithmetic]}")
print(id_rar)

print("Getting token ids with price")
if data_choice == "New":
    print(price)
else:
    from Opensea_API_saan import price
    price = price(data)
    print(price)
       

    


