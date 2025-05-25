import discord
from discord.ext import commands
import sys, os, util, toml, requests, logging, time

from config import CONFIG

import tracking.databases as databases

import gamemodes.bedwars as bedwars

import gamemodes.duels as duels


def initialize_config(dir):
  """Initializes the config file and sets the API key and tracking enabled status."""
  parsed_toml = None
  # Check if config.toml exists, else read from default
  if not os.path.exists(f"{dir}/config.toml"):
    logging.warning("sprocket-hypixel config.toml not found. Looking for changes in config.toml.default.")
    
    if not os.path.exists(f"{dir}/config.toml.default"):
      logging.error("config.toml.default not found. Please fix your configuration. Cogs will NOT be enabled.")
      return []
    
    with open(f"{dir}/config.toml.default", "r") as f:
      parsed_toml = toml.loads(f.read())
  else:
    with open(f"{dir}/config.toml", "r") as f:
      parsed_toml = toml.loads(f.read())
    
  CONFIG.PATH = dir
  CONFIG.KEY = parsed_toml["api_key"].strip()
  CONFIG.TRACKING_ENABLED = parsed_toml["tracking"]
  

  # Check if API key is valid by requesting stats for Hypixel
  # player with UUID f7c77d99-9f15-4a66-a87d-c4a51ef30d19
  url = f"https://api.hypixel.net/player?key={CONFIG.KEY}&uuid=f7c77d99-9f15-4a66-a87d-c4a51ef30d19"
  response = requests.get(url)
  if response.status_code == 403:
    logging.error("Invalid API key. Please check your config.toml file. Cogs will NOT be enabled.")
    return []
  elif response.status_code == 200 or response.status_code == 429:
    logging.info("API key is valid.")
  else:
    logging.error(f"Unexpected error: {response.status_code}. Cogs will NOT be enabled.")
    return []

def get_intents() -> discord.Intents:
  intents = discord.Intents.default()
  intents.message_content = True

  return intents

def get_cogs(client: commands.Bot, dir: str) -> list:
  initialize_config(dir)

  return [
    bedwars.Bedwars(client),
    util.Util(dir),
    duels.Duels()
  ]

def api_token(directory: str) -> str:
  with open(f"{directory}/hypixel_token.txt", "r") as f:
    return f.read().strip()