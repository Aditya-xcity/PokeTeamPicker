# Problem: Fetch Pokémon data, compute profit using stats + synergy, and store in JSON

"""
Name - ADITYA BHARDWAJ
Section - D2
Roll No - 07
Course – B TECH
Branch – CSE
"""

import pokebase as pb
import json

# 🔥 Enable caching (VERY IMPORTANT for speed)
pb.APIResource.CACHE = True


def getSynergyBonus(types):
    type_set = set(types)

    if "fire" in type_set and "flying" in type_set:
        return 20
    elif "water" in type_set and "electric" in type_set:
        return 15
    else:
        return 0


def calculateProfit(attack, defense, speed, bonus):
    return attack + defense + speed + bonus


def fetchPokemonData(limit=151):
    pokemon_list = []

    for i in range(1, limit + 1):
        try:
            p = pb.pokemon(i)

            name = p.name

            stats = {stat.stat.name: stat.base_stat for stat in p.stats}

            attack = stats.get("attack", 0)
            defense = stats.get("defense", 0)
            speed = stats.get("speed", 0)

            types = [t.type.name for t in p.types]

            bonus = getSynergyBonus(types)

            profit = calculateProfit(attack, defense, speed, bonus)

            pokemon_data = {
                "id": i,
                "name": name,
                "types": types,
                "attack": attack,
                "defense": defense,
                "speed": speed,
                "synergyBonus": bonus,
                "profit": profit
            }

            pokemon_list.append(pokemon_data)

            print(f"[DONE] {i}/151 - {name} | Profit: {profit}")

        except Exception as e:
            print(f"[FAILED] {i}/151 | Error: {e}")

    return pokemon_list


def saveToJson(data, filename="pokemonData.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("\n✅ All Pokémon successfully saved to JSON file")
    except Exception as e:
        print(f"\n❌ Error saving JSON file: {e}")


def main():
    print("========== Pokémon Data Generator ==========")
    print("Press 1 to Start")
    print("Press 0 to Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n🚀 Starting data fetch...\n")
        data = fetchPokemonData(151)
        saveToJson(data)
    elif choice == "0":
        print("👋 Exiting program...")
    else:
        print("⚠️ Invalid input. Please restart and press 1 or 0.")


if __name__ == "__main__":
    main()