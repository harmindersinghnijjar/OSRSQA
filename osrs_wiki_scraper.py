import requests
from bs4 import BeautifulSoup
import os
import sqlite3

# Create the data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Loop through the first row of the runescape.db database and retrieve the names of the monsters
def get_monster_names():
    monster_names = []
    runescape_db = sqlite3.connect("runescape.db")
    runescape_db.row_factory = sqlite3.Row
    cursor = runescape_db.cursor()
    cursor.execute("SELECT * FROM monsters")
    rows = cursor.fetchall()
    runescape_db.close()
    for row in rows:
        monster_names.append(row['name'])
    return monster_names

# Get the list of URLs to scrape
def get_urls():
    urls = []
    for name in get_monster_names():
        urls.append(f'https://oldschool.runescape.wiki/w/{name}')
    return urls


    
    

# Scrape the monster pages
def scrape_monsters(urls):
    # Loop through each URL
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving {url}: {e}")
            continue
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            soup = soup.find('div', {'id': 'content'})
        except:
            pass
        # Find the NPC name
        try:
            npc_name = soup.find('h1', {'class': 'firstHeading'}).text
        except AttributeError:
            try:
                npc_name = soup.find('h1', {'id': 'firstHeading'}).text
            except AttributeError:
                print(f"Error finding NPC name in {url}")
                continue
       
        
        # Save the content to a file in the data directory
        with open(f'data/{npc_name}.md', 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"Saved {npc_name} to file")
        
if __name__ == '__main__':
    scrape_monsters(get_urls())