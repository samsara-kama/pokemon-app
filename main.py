import requests
import streamlit as st

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'


# Function to get data from PokéAPI


def get_pokemon_data(pokemon_name):
    response = requests.get(f"{POKE_API_URL}{pokemon_name.lower()}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


st.title("The Pokémon App")
st.page_link("pages/page_type.py",label="type",icon="📚")
st.page_link('pages/page_combat.py',label="combat",icon='💥')

# Input for Pokémon name
pokemon_name = st.text_input("Enter Pokémon Name:", "")

# When user submits a Pokémon name
if pokemon_name:
    pokemon_data = get_pokemon_data(pokemon_name)

    if pokemon_data:
        # Display Pokémon basic information
        st.subheader(f"Name: {pokemon_data['name'].capitalize()}")
        st.image(pokemon_data['sprites']['front_default'], width=150)

        # Display stats like HP, Attack, Defense, etc.
        st.subheader("Stats:")
        stats = pokemon_data['stats']
        for stat in stats:
            st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")

        # Display Pokémon types
        st.subheader("Types:")
        types = pokemon_data['types']
        for poke_type in types:
            st.write(f"- {poke_type['type']['name'].capitalize()}")

        # Display height and weight
        st.subheader("Physical Characteristics:")
        st.write(f"Height: {pokemon_data['height'] / 10} meters")
        st.write(f"Weight: {pokemon_data['weight'] / 10} kg")
        st.write(pokemon_data)

    else:
        st.error("Pokémon not found! Please check the spelling or try another Pokémon.")