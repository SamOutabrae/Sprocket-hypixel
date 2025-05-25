import discord
from discord.ext import commands
import sys, os, util

from config import CONFIG

import tracking.databases as databases

import gamemodes.bedwars as bedwars

import gamemodes.duels as duels


def get_tracking_enabled(dir) -> bool:
  return False

def get_intents() -> discord.Intents:
  intents = discord.Intents.default()
  intents.message_content = True

  return intents

def get_cogs(client: commands.Bot, dir: str) -> list:
  CONFIG.KEY = api_token(dir)
  CONFIG.PATH = dir
  CONFIG.TRACKING_ENABLED = get_tracking_enabled
  

  return [
    bedwars.Bedwars(client),
    util.Util(dir),
    duels.Duels()
  ]

def api_token(directory: str) -> str:
  with open(f"{directory}/hypixel_token.txt", "r") as f:
    return f.read().strip()