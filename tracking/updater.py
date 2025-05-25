import os
import requests
from datetime import datetime
import json
import sys
import toml

from pathlib import Path

def getKey(path):
  with open(path + "/config.toml", "r") as f:
    data = toml.load(f)
    return data["api_key"].strip()
  

def main():
  # Have to go up one directory becuase this is in tracking, not root
  PATH = str(Path(__file__).parents[1].absolute())
  key = getKey(PATH)

  players = None
  with open(PATH + "/data/trackedplayers.txt", "r") as f:
    players = [player.strip() for player in f.readlines()]

  players = open(PATH + "/data/trackedplayers.txt").readlines()
  PATH = PATH + "/data/"
  DATE = datetime.now().strftime("%d-%m-%y")
  
  for player in players:
    player = player.replace("\n", "")

    url = f'https://api.hypixel.net/player?key={key}&uuid=' + player
    data = requests.get(url).json()

    FILEPATH = PATH + "/trackedplayers/" + player + "/" + DATE + ".json"
    
    if(os.path.exists(PATH + "trackedplayers/" + player)):
      f = open(FILEPATH, "w")
      f.write(json.dumps(data))
      f.close()
      print("Wrote data for " + player)
      continue

    os.makedirs(PATH + "trackedplayers/" + player)
    f = open(FILEPATH, "w")
    f.write(json.dumps(data))
    print(f"Wrote data for {player} at {FILEPATH}.")
    f.close()
    continue

main()