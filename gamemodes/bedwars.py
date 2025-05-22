import discord
from discord.ext import commands, bridge

import logging
import requests

import util 

from typing import Optional

def parseFromJSON(json):
  """Creates a BedwarsStats object from a JSON response from the Hypixel API."""

  winstreak = "N/A"
  
  try:
      winstreak = json["player"]["stats"]["Bedwars"]["winstreak"]
  except:
      pass

  kills        = json["player"]["stats"]["Bedwars"]["kills_bedwars"]
  deaths       = json["player"]["stats"]["Bedwars"]["deaths_bedwars"]
  voidDeaths   = json["player"]["stats"]["Bedwars"]["void_deaths_bedwars"]
  finalDeaths  = json["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
  finalKills   = json["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
  bedwarsLevel = json["player"]["achievements"]["bedwars_level"]
  displayname  = json["player"]["displayname"]
  gamesplayed  = json["player"]["stats"]["Bedwars"]["games_played_bedwars"]
  wins         = json["player"]["stats"]["Bedwars"]["wins_bedwars"]
  losses       = json["player"]["stats"]["Bedwars"]["losses_bedwars"]
  kdr          = finalKills/finalDeaths

  stats = BedwarsStats(winstreak, kills, deaths, voidDeaths, finalDeaths, finalKills, bedwarsLevel, gamesplayed, wins, losses, kdr, displayname)
  return stats


class BedwarsStats():
  def __init__(self, winstreak, kills, deaths, voidDeaths, finalDeaths, finalKills, bedwarsLevel, gamesplayed, wins, losses, kdr, displayname):
    self.winstreak    = winstreak
    self.kills        = kills
    self.deaths       = deaths 
    self.voidDeaths   = voidDeaths
    self.finalKills   = finalKills
    self.finalDeaths  = finalDeaths
    self.bedwarsLevel = bedwarsLevel
    self.gamesplayed  = gamesplayed
    self.wins         = wins
    self.losses       = losses
    self.kdr          = kdr
    self.displayname  = displayname

    self.lastResponse = None
  
  @staticmethod
  def get(key: str, uuid=None, username=None):
    if uuid is None and username is not None:
      uuid = util.getUUID(username)
    
    response = None
    url = f'https://api.hypixel.net/player?key={key}&uuid={uuid}'
    try:
      logging.debug(f"Making web request to {url}")
      response = requests.get(url)

      return parseFromJSON(response.json())
    except Exception as e:
      logging.error(f"Error while making request to {url}. Response code: {response.status_code}.")
      raise e

  def __add__(self, other):
    killsfinal        = self.kills + other.kills
    deathsfinal       = self.deaths + other.deaths
    voidDeathsfinal   = self.voidDeaths + other.voidDeaths
    finalDeathsfinal  = self.finalDeaths + other.finalDeaths
    finalKillsfinal   = self.finalKills + other.finalKills
    bedwarsLevelfinal = self.bedwarsLevel + other.bedwarsLevel
    gamesplayedfinal  = self.gamesplayed + other.gamesplayed
    winsfinal         = self.wins + other.wins
    lossesfinal       = self.losses + other.losses
    kdrfinal          = self.kdr + other.kdr

    return BedwarsStats(self.winstreak, killsfinal, deathsfinal, voidDeathsfinal, finalDeathsfinal, finalKillsfinal, bedwarsLevelfinal, gamesplayedfinal, winsfinal, lossesfinal, kdrfinal, self.displayname)

  def __sub__(self, other):
    killsfinal        = self.kills - other.kills
    deathsfinal       = self.deaths - other.deaths
    voidDeathsfinal   = self.voidDeaths - other.voidDeaths
    finalDeathsfinal  = self.finalDeaths - other.finalDeaths
    finalKillsfinal   = self.finalKills - other.finalKills
    bedwarsLevelfinal = self.bedwarsLevel - other.bedwarsLevel
    gamesplayedfinal  = self.gamesplayed - other.gamesplayed
    winsfinal         = self.wins - other.wins
    lossesfinal       = self.losses - other.losses

    kdrfinal = 0
    try:
        kdrfinal = finalKillsfinal/finalDeathsfinal
    except:
        pass

    return BedwarsStats(self.winstreak, killsfinal, deathsfinal, voidDeathsfinal, finalDeathsfinal, finalKillsfinal, bedwarsLevelfinal, gamesplayedfinal, winsfinal, lossesfinal, kdrfinal, self.displayname)

  def toEmbedDict(self):
    winloss = 0
    if self.losses + self.wins != 0:
      winloss = self.wins/(self.wins + self.losses)
      pass

    embed_dict = {
      "Level": f"{self.bedwarsLevel}",
      "Winstreak": f"{self.winstreak}",
      "Games played": f"{self.gamesplayed}",
      "Wins": f"{self.wins}",
      "Losses": f"{self.losses}",
      "Win Rate": f"{round(winloss*100)}%",
      "Kills": f"{self.kills}",
      "Deaths": f"{self.deaths}",
      "Void Deaths": f"{self.voidDeaths}",
      "Final Kills": f"{self.finalKills}",
      "Final K/D Ratio": f"{round(self.kdr, 2)}"
    }

    return embed_dict
  
  def toEmbed(self, embed=None):
    if embed is None:
      embed = discord.Embed(title = self.displayname, description = "Bedwars stats for " + self.displayname, color=0x00ff00 )

    d = self.toEmbedDict()
    for key in d.keys():
      value = d[key]
      embed.add_field(name = key, value = value, inline = False)

    embed.from_dict(self.toEmbedDict())
    return embed

class Bedwars(commands.Cog):
  key = None

  def __init__(self, client, hypixel_api_key):
    self.client = client
    self.key = hypixel_api_key

  @bridge.bridge_command(name="bw", aliases=["bedwars", "bwstats", "statsBW"])
  @util.selfArgument
  async def bw(self, ctx, username: Optional[str]):
    if username is None:
      await ctx.send("Please provide a username or UUID.")
      return

    uuid = util.getUUID(username)
    
    try:
      await ctx.respond(embed = BedwarsStats.get(self.key, uuid=uuid).toEmbed())
    except Exception as e:
      await ctx.respond(f"Error while getting stats. Are you sure `{username}` is correct?")