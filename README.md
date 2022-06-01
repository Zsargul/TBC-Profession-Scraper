# TBC-Profession-Scraper
Python web-scraper for getting data about crafting difficulty regarding trade-skills from [tbc.wowhead.com](https://tbc.wowhead.com/), and exporting it to CSV. I
made this as a supporting tool for a profession-related WoW add-on I am making. This was heavily inspired by a
[script by Ravendwyr](https://github.com/Ravendwyr/TradeSkillInfo_DataMiner), one of the makers of the TradeSkillInfo Add-on.

## About
The scraper uses Selenium with geckodriver, BeautifulSoup and Pandas to visit [The Burning Crusade WoWhead](https://tbc.wowhead.com/), and iterate over
every trade-skill in the game (with the exception of trade-skills which do not have craftable items, like herbalism), and uses a list of 'spell IDs'
(craftable item IDs) to parse and collect data about the when each item's difficulty turns orange/yellow/green/gray. It then finally exports them as CSV. 
The script takes a good while to run as Selenium isn't the fastest web-scraping tool around, but I needed to use it as the data related to the item difficulty
was generated using JavaScript, which faster tools such as the requests library didn't support.

## Dependencies

- BeatifulSoup4
- Pandas
- Selenium

All of these can be installed with ```pip install```

## CSV Exporting
The data is exported to CSV in the ```spells-csv/``` folder. The directory to which the files are exported can be changed on the line:

```spellDF.to_csv('spells-csv/%s.csv' % (profNames[i]), header=True, index=False, sep='\t')```
