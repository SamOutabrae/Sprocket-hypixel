import discord

from discord.ext import commands
import sys, os

import tracking.databases as databases

import gamemodes.bedwars as bedwars
import util

def get_tracking_enabled(dir) -> bool:
  return False

def get_intents() -> discord.Intents:
  intents = discord.Intents.default()
  intents.message_content = True

  return intents

def get_cogs(client: commands.Bot, dir: str) -> list:
  tracking_enabled = get_tracking_enabled(dir)

  return [
    bedwars.Bedwars(client, api_token(dir), dir, get_tracking_enabled(dir)),
    util.Util(dir)
  ]

def api_token(directory: str) -> str:
  with open(f"{directory}/hypixel_token.txt", "r") as f:
    return f.read().strip()