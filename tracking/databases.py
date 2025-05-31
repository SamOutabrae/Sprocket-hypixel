import asyncio, os, json, logging
import datetime
import pandas as pd

from ..config import CONFIG
from .. import util

databases = {}


def getJSON(date: datetime.datetime, uuid=None, username=None):
    PATH = CONFIG.PATH

    # Determine UUID
    if uuid is not None:
        real_uuid = uuid
    elif username is not None:
        real_uuid = util.getUUID(username)
        if real_uuid == 1:
            return None
    else:
        return None

    wkdir = os.path.join(PATH, "data", "trackedplayers", real_uuid)
    date_str = date.strftime("%d-%m-%y")
    filepath = os.path.join(wkdir, f"{date_str}.json")

    # If exact file doesn't exist, try mapping.json
    if not os.path.exists(filepath):
        mapping_path = os.path.join(wkdir, "mapping.json")
        if not os.path.exists(mapping_path):
            logging.error(f"Mapping file not found: {mapping_path}")
            return None

        with open(mapping_path, "r") as f:
            mapping = json.load(f)

        if date_str not in mapping:
            logging.error(f"No mapping for date {date_str}")
            return None

        mapped_date = mapping[date_str]
        if mapped_date is None:
            logging.error(f"No valid fallback for date {date_str}")
            return None

        filepath = os.path.join(wkdir, f"{mapped_date}.json")
        if not os.path.exists(filepath):
            logging.error(f"Mapped file {filepath} does not exist.")
            return None

    # Load and return JSON
    with open(filepath, "r") as f:
        return json.load(f)

def normalizeJSON(json):
  kills = json["player"]["stats"]["Bedwars"]["kills_bedwars"]
  deaths = json["player"]["stats"]["Bedwars"]["deaths_bedwars"]
  voidDeaths = json["player"]["stats"]["Bedwars"]["void_deaths_bedwars"]
  finalDeaths = json["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
  finalKills = json["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
  bedwarsLevel = json["player"]["achievements"]["bedwars_level"]
  bedsBroken = json["player"]["stats"]["Bedwars"]["beds_broken_bedwars"]
  displayname = json["player"]["displayname"]
  gamesplayed = json["player"]["stats"]["Bedwars"]["games_played_bedwars"]
  wins = json["player"]["stats"]["Bedwars"]["wins_bedwars"]
  losses = json["player"]["stats"]["Bedwars"]["losses_bedwars"]
  #winstreak = json["player"]["stats"]["Bedwars"]["winstreak"]
  kdr = kills / deaths
  finalkdr = finalKills / finalDeaths
  
  return {
    "Date": json["date"],
    "Kills": kills,
    "Deaths": deaths,
    "Void Deaths": voidDeaths,
    "Final Deaths": finalDeaths,
    "Final Kills": finalKills,
    "Beds Broken": bedsBroken,
    "Bedwars Level": bedwarsLevel,
    "Games Played": gamesplayed,
    "Wins": wins,
    "Losses": losses,
    #"Win Streak": winstreak,
    "K/D Ratio": kdr,
    "Final K/D Ratio": finalkdr
  }

def rebuild_database_worker(player, PATH):
  path = PATH + "/data/"

  PLAYERPATH = f"{path}/trackedplayers/{player}"
  json_files = [f.replace(".json", "") for f in os.listdir(PLAYERPATH) if f.endswith(".json")]
  json_files.sort(key=lambda x : datetime.strptime(x, "%d-%m-%y"))
  json_files = [f + ".json" for f in json_files]

  data = []
  failed = 0
  for filename in json_files:
    with open(os.path.join(PLAYERPATH, filename), "r") as file:
      json_data = json.load(file)
      json_data["date"] = filename.removesuffix(".json")

      if json_data["success"] != True:
        failed += 1
        continue
      
      df = normalizeJSON(json_data)
      data.append(df)
  
  df = pd.DataFrame(data)

  df.to_hdf(PATH + f"/data/databases/{player}/data.h5", key=player)
  return pd.DataFrame(data)


async def rebuild_db(player):
  result = await asyncio.to_thread(rebuild_database_worker, player)
  databases[player] = result

  logging.info(f"Sucessfully rebuilt database for {player}")

async def rebuild_dbs(PATH):
  logging.info("Rebuilding databeses.")
  players = [player.removesuffix("\n") for player in open(PATH + "/data/trackedplayers.txt").readlines()]
  PATH = PATH + "/data/trackedplayers"
  DATE = datetime.datetime.now().strftime("%d-%m-%y")

  tasks = [asyncio.create_task(rebuild_db(player)) for player in players]

  await asyncio.gather(*tasks)

def time_until_next_run(target_hour=0, target_minute=0):
  now = datetime.datetime.now()
  next_run = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

  if next_run <= now:  # If the target time today has already passed, schedule for tomorrow
    next_run += datetime.timedelta(days=1)

  return (next_run - now).total_seconds()

async def daily_scheduler():
  while True:
    seconds_until_next_run = time_until_next_run(target_hour=6, target_minute=0)  # Adjust time as needed
    await asyncio.sleep(seconds_until_next_run)  
    await initialize_dbs() 

async def initialize_dbs(directory):
  PATH = f"{directory}/data/"
  players = [player.strip() for player in open(PATH + "trackedplayers.txt").readlines()]

  now = datetime.datetime.now().strftime('%d-%m-%y')

  for player in players:
    player_dir = PATH + f"/databases/{player}"
    datapath = f"{player_dir}/data.h5"

    if not os.path.exists(player_dir):
      os.mkdir(player_dir)

    if not os.path.isfile(datapath):
      asyncio.create_task(rebuild_db(player))
      continue

    df = pd.read_hdf(datapath)

    if df["Date"].iloc[-1] != now:
      json_path = f"{player_dir}/{now}.json"

      if os.path.isfile(json_path):
        with open(json_path, "r") as file:
          json_data = json.load(file)
          json_data["date"] = json_path.removesuffix(".json")

          if json_data.get("success") is True:
            dat = dat.normalizeJSON(json_data)
            df = pd.concat([df, dat], ignore_index=True)

            df.to_hdf(datapath)

    databases[player] = df
    logging.info(f"Loaded database for {player}")