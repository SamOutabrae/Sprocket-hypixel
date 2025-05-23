import os
import requests
from datetime import datetime
import json
import sys

def main():
  # Have to go up one directory becuase this is in tracking, not root
  PATH = os.getcwd() + "/.."
  
  if(len(sys.argv) > 0):
      PATH = sys.argv[len(sys.argv) - 1]

  players = open(PATH + "/data/trackedplayers.txt").readlines()
  PATH = PATH + "/dat/"
  DATE = datetime.now().strftime("%d-%m-%y")
  
  for player in players:
    player = player.replace("\n", "")

    url = 'https://api.hypixel.net/player?key=e31fa63d-7a49-4b76-ad1e-7c0d312c0a13&uuid=' + player
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
    print("Wrote data for " + player)
    f.close()
    continue

main()