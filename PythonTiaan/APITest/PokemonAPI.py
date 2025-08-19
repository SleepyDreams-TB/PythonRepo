import requests

#url = "https://pokeapi.co/api/v2/pokemon/ditto"
#response = requests.get(url)

#print("Status Code:", response.status_code)


def get_pokemon_info(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon = { #create a dictionary with relevant data[specify fields to extract from the JSON response] Treat JSON as a dictionary
            "name": data["name"].title(),
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]], # "abilities" is a list of dictionaries, so we extract the "name" from each ability
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}  # Extracting stats as a dictionary
        }
        return pokemon

while True:  
    print("Welcome to the Pokémon Info Fetcher!")
    name = input("Enter a Pokémon name: ")
    info = get_pokemon_info(name)

    if info:
        print(f"\nPokémon: {info['name']} (ID: {info['id']})")
        print(f"Height: {info['height']}  Weight: {info['weight']}")
        print(f"Types: {', '.join(info['types'])}")
        print(f"Abilities: {', '.join(info['abilities'])}")
        print(f"Stats: {', '.join(f"{stat}: {value}" for stat, value in info['stats'].items())}") #search for stat field in the JSON response, join each stat and its value with a comma. 

        input("\nPress Enter to continue or type 'exit' to quit: ")
        if input().lower() == 'exit':
            break
    else:
        print("Invalid Pokémon name. Please try again.")
