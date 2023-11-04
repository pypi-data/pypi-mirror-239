"""
I believe this is the source for the CSV file: https://www.kaggle.com/datasets/rounakbanik/pokemon/data
"""

import pandas as pd
import os

directory = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(directory, "pokemon.csv"))

def get_pokemon_name(id: int) -> str: 
    """
    Returns the name of the Pokemon with the given ID
    """
    return df[df["pokedex_number"] == id]["name"].iloc[0]

def get_pokemon_attack(name: str) -> int:
    """
    Returns the attack of the Pokemon with the given name
    """
    return int(df[df["name"] == name]["attack"].iloc[0])

def get_pokemon_defense(name: str) -> int:
    """
    Returns the defense of the Pokemon with the given name
    """
    return int(df[df["name"] == name]["defense"].iloc[0])

def get_pokemon_height(name: str) -> int:
    """
    Returns the height of the Pokemon with the given name in centimetres
    """
    return int(df[df["name"] == name]["height_m"].iloc[0] * 100)

def get_pokemon_weight(name: str) -> int:
    """
    Returns the weight of the Pokemon with the given name in kilograms
    """
    return round(df[df["name"] == name]["weight_kg"].iloc[0])

def get_pokemon_num_types(name: str) -> int:
    """
    Returns the number of types that the Pokemon with the given name has.
    If the name is invalid, 0 is returned.
    """
    if df[df["name"] == name]["type1"].any():
        if df[df["name"] == name]["type2"].any():
            return 2
        return 1
    return 0

def get_pokemon_type1(name: str) -> str:
    """
    Returns the first type of the Pokemon with the given name.
    """
    if df[df["name"] == name]["type1"].any():
        return df[df["name"] == name]["type1"].iloc[0]
    else: 
        return None

def get_pokemon_type2(name: str) -> str:
    """
    Returns the second type of the Pokemon with the given name.
    If the Pokemon does not have a second type, None is returned.
    """
    if df[df["name"] == name]["type2"].any():
        return df[df["name"] == name]["type2"].iloc[0]
    else: 
        return None
    

__all__ = [
    'get_pokemon_name',
    'get_pokemon_attack',
    'get_pokemon_defense',
    'get_pokemon_height',
    'get_pokemon_weight',
    'get_pokemon_num_types',
    'get_pokemon_type1',
    'get_pokemon_type2'
]