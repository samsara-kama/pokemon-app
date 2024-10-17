import requests
import streamlit as st
import concurrent.futures

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'
POKE_TYPE_API_URL='https://pokeapi.co/api/v2/type/'

def fetch_pokemon_data(pokemon_name):
    try:
        response = requests.get(f"{POKE_API_URL}{pokemon['pokemon']['name']}")
        pokemon_data = response.json()
        life_point = pokemon_data['stats'][0]['base_stat']
        return life_point
    except:
        print(f"failed to fetch for{pokemon_name}")
        return 0


def get_pokemon_type_data(pokemon_type):
    response = requests.get(f"{POKE_TYPE_API_URL}{pokemon_type.lower()}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


st.title("Pokemon type info ")

st.page_link("main.py",label="Home",icon="🏠")

pokemon_type = st.text_input("Enter the pokemon type:","")

if pokemon_type:
    pokemon_type_data = get_pokemon_type_data(pokemon_type)
    if pokemon_type_data:
        st.subheader(f"Type name: {pokemon_type_data['name'].capitalize()}")
        st.write("Damage relationships of this type:")
        st.write(f"{pokemon_type_data['name'].capitalize()} type takes double damage from: "
                 f"{','.join([double_damage['name'] for double_damage in pokemon_type_data['damage_relations']['double_damage_from']])}")
        st.write(f"{pokemon_type_data['name'].capitalize()} type deals double damage to: "
                 f"{','.join([double_damage['name'] for double_damage in pokemon_type_data['damage_relations']['double_damage_to']])}")
        st.write(f"{pokemon_type_data['name'].capitalize()} type takes half damage from: "
                 f"{','.join([double_damage['name'] for double_damage in pokemon_type_data['damage_relations']['half_damage_from']])}")
        st.write(f"{pokemon_type_data['name'].capitalize()} type deals half damage to: "
                 f"{','.join([double_damage['name'] for double_damage in pokemon_type_data['damage_relations']['half_damage_to']])}")
        st.subheader(f"There are {len(pokemon_type_data['pokemon'])} pokemons in this type.")
        total_lifepoints = 0
        pokemons = pokemon_type_data['pokemon']
        futures=[]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for pokemon in pokemons:
                futures.append(executor.submit(fetch_pokemon_data, pokemon['pokemon']['name']))
            for future in concurrent.futures.as_completed(futures):
                total_lifepoints += future.result()

        average_ligepoints = total_lifepoints/len(pokemon_type_data['pokemon'])
        st.write(f"The average life point of this type is: {average_ligepoints}")




        st.write(pokemon_type_data)

    else:
        st.error("This is not a valid pokemon type! Please try another.")