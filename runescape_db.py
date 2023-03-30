
# Import required modules
import logging
import sqlite3
import json
from osrsbox import monsters_api
from pprint import pprint

# Load all monsters
all_db_monsters = monsters_api.load()
# print("Loaded", len(all_db_monsters), "monsters")

# Define lists to hold monster names, descriptions, and drops
monster_names = []
monster_descriptions = []
monster_drops = []

# Loop over monsters and append names, descriptions, and drops to their respective lists
for monster in all_db_monsters:
    monster_names.append(monster.name)
    monster_descriptions.append(monster.examine)
    monster_drops.append(monster.drops)

# Create a dictionary to hold all monsters
monster_dict = {}

# Loop over monsters and create nested dictionaries for each monster
for i in range(len(monster_names)):
    # Create a nested dictionary for each monster with description and drops
    nested_dict = {'description': monster_descriptions[i]}
    drop_dict = {}
    for drop in monster_drops[i]:
        drop_dict[drop.name] = drop.quantity
    nested_dict['drops'] = drop_dict

    # Add the nested dictionary to the monster dictionary with the monster name as the key
    monster_dict[monster_names[i]] = nested_dict

# Connect to the database and insert the monsters
runescape_db = sqlite3.connect("runescape.db")
runescape_db.execute("CREATE TABLE IF NOT EXISTS monsters (name TEXT, examine TEXT, drops TEXT)")

for name, data in monster_dict.items():
    examine = data['description']
    drops = json.dumps(data['drops'])
    runescape_db.execute("INSERT INTO monsters VALUES (?, ?, ?)", (name, examine, drops))

runescape_db.commit()   
runescape_db.close()


# Convert database to dictionary
runescape_db = sqlite3.connect("runescape.db")
runescape_db.row_factory = sqlite3.Row
cursor = runescape_db.cursor()
cursor.execute("SELECT * FROM monsters")
rows = cursor.fetchall()
runescape_db.close()

# Create a dictionary to hold all monsters
monster_dict = {}

# Loop over monsters and create nested dictionaries for each monster
for row in rows:
    # Create a nested dictionary for each monster with description and drops
    nested_dict = {'description': row['examine']}
    drop_dict = json.loads(row['drops'])
    nested_dict['drops'] = drop_dict

    # Add the nested dictionary to the monster dictionary with the monster name as the key
    monster_dict[row['name']] = nested_dict 
    

# Save to .txt file
with open('data/monster_dict.txt', 'w') as file:
    file.write(json.dumps(monster_dict))
    file.close()
    






