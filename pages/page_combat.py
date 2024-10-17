import requests
import streamlit as st
import random

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

# Function to get data from PokéAPI
def get_pokemon_data(pokemon_name):
    response = requests.get(f"{POKE_API_URL}{pokemon_name.lower()}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to calculate damage
def calculate_damage(attacker_attack, defender_defense):
    # Simple formula for calculating damage
    damage = max(1, attacker_attack - (defender_defense // 2))  # Avoid negative damage
    return damage

# Function to simulate the combat
def simulate_combat(pokemon_1, pokemon_2):
    # Extract relevant stats for combat
    pokemon_1_name = pokemon_1['name'].capitalize()
    pokemon_2_name = pokemon_2['name'].capitalize()

    pokemon_1_hp = pokemon_1['stats'][0]['base_stat']
    pokemon_1_attack = pokemon_1['stats'][1]['base_stat']
    pokemon_1_defense = pokemon_1['stats'][2]['base_stat']

    pokemon_2_hp = pokemon_2['stats'][0]['base_stat']
    pokemon_2_attack = pokemon_2['stats'][1]['base_stat']
    pokemon_2_defense = pokemon_2['stats'][2]['base_stat']

    # Determine turn order randomly
    turn = random.choice([1, 2])
    st.write(f"Turn order is randomly decided: {'First' if turn == 1 else 'Second'} Pokémon attacks first!")

    # Simulate combat
    while pokemon_1_hp > 0 and pokemon_2_hp > 0:
        if turn == 1:
            # First Pokémon attacks second Pokémon
            damage = calculate_damage(pokemon_1_attack, pokemon_2_defense)
            pokemon_2_hp -= damage
            st.write(f"{pokemon_1_name} attacks {pokemon_2_name} and deals {damage} damage!")
            st.write(f"{pokemon_2_name} has {max(0, pokemon_2_hp)} HP left.")
            turn = 2  # Switch turn
        else:
            # Second Pokémon attacks first Pokémon
            damage = calculate_damage(pokemon_2_attack, pokemon_1_defense)
            pokemon_1_hp -= damage
            st.write(f"{pokemon_2_name} attacks {pokemon_1_name} and deals {damage} damage!")
            st.write(f"{pokemon_1_name} has {max(0, pokemon_1_hp)} HP left.")
            turn = 1  # Switch turn

    # Determine winner
    if pokemon_1_hp > 0:
        st.success(f"{pokemon_1_name} wins the battle!")
    else:
        st.success(f"{pokemon_2_name} wins the battle!")


# Streamlit app layout
st.title("The Pokémon Combat Simulator")

# Input for the first Pokémon name
pokemon_name_1 = st.text_input("Enter First Pokémon Name:", "")

# Input for the second Pokémon name
pokemon_name_2 = st.text_input("Enter Second Pokémon Name:", "")

# When user submits both Pokémon names
if pokemon_name_1 and pokemon_name_2:
    pokemon_data_1 = get_pokemon_data(pokemon_name_1)
    pokemon_data_2 = get_pokemon_data(pokemon_name_2)

    if pokemon_data_1 and pokemon_data_2:
        # Display both Pokémon's basic information
        st.subheader(f"First Pokémon: {pokemon_data_1['name'].capitalize()}")
        st.image(pokemon_data_1['sprites']['front_default'], width=150)

        st.subheader(f"Second Pokémon: {pokemon_data_2['name'].capitalize()}")
        st.image(pokemon_data_2['sprites']['front_default'], width=150)

        # Simulate the Pokémon combat
        st.header("Combat Simulation:")
        simulate_combat(pokemon_data_1, pokemon_data_2)

    else:
        st.error("One or both Pokémon not found! Please check the spelling or try another Pokémon.")
