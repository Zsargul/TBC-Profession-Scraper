import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs

# Get difficulties. If none exists, default to 0.
# r1 = orange
# r2 = yellow
# r3 = green
# r4 = gray
def getDiff(string):
    color = soup.find("span", class_=string)

    if (color is None):
        return 0
    else:
        return color.get_text()

profNames = [
        'first-aid',        # 0
        'blacksmithing',    # 1
        'engineering',      # 2
        'enchanting',       # 3
        'jewelcrafting',    # 4
        'leatherworking',   # 5
        'tailoring',        # 6
        'mining',           # 7
        'cooking',          # 8
        'alchemy'           # 9
]

# Get list of spell IDs for all professions
profSpellList = []

for prof in profNames:
    fileName = 'spell-ids/' + prof + '.txt'
    file = open(fileName, "r")

    # Read each spell ID into list
    spellList = file.read().splitlines()
    profSpellList.append(spellList)

# Scrape wowhead for remaining data
i = 0
for prof in profSpellList:
    print("* Getting %s spells... (%d out of %d professions)" % (profNames[i], i+1, len(profSpellList)))
    print("-----------------------------------------------------------")
    profSpells = []
    j = 0
    for spellID in prof:

        URL = 'https://tbc.wowhead.com/spell=' + spellID

        options = Options()
        options.headless = True
        s = Service(executable_path='geckodriver', log_path='/dev/null') # Prevent geckodriver logging
        browser = webdriver.Firefox(options=options, service=s)
        browser.get(URL)
        html = browser.page_source

        soup = bs(html, 'lxml')

        # Get data related to the tradeSkill spell
        spell = []
        
        spellName = soup.find_all('h1', class_='heading-size-1')[0].get_text()

        orange = getDiff("r1")
        yellow = getDiff("r2")
        green = getDiff("r3")
        gray = getDiff("r4")

        spell.extend((spellID, orange, yellow, green, gray, spellName))
        profSpells.append(spell) # Store in main spell list

        print("Scraped %s \t(%d/%d)" % (URL, j+1, len(prof)))

        browser.quit()
        j+=1

        spellDF = pd.DataFrame(profSpells, columns = ['spellID', 'orange', 'yellow', 'green', 'gray', 'spellName'])

    # Export profession to CSV
    spellDF.to_csv('spells-csv/%s.csv' % (profNames[i]), header=True, index=False, sep='\t')
    print("Exported %s.csv" % (profNames[i]))
    i += 1

print("Done")
