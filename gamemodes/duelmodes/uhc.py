import discord, requests

from util import getPrestige, winsToPrestige

from dataclasses import dataclass

from tracking.databases import getJSON

from config import CONFIG
from typing import Optional 

@dataclass
class UHCStats():
  username: str
  wins: int
  losses: int
  kills: int
  deaths: int
  gamesPlayed: int
  goldenApplesEaten: int
  damageDealt: int
  blocksPlaced: int
  highestWinstreak: Optional[int]
  winstreak: Optional[int]
  bow_hits: int
  bow_shots: int

  @classmethod
  def from_json(cls, json_data: dict):
    if not json_data.get("success", False):
      return None

    try:
      stats    = json_data["player"]["stats"]["Duels"]
      username = json_data["player"]["displayname"]

      return cls(
        username          = username,
        wins              = stats.get("uhc_duel_wins", 0),
        losses            = stats.get("uhc_duel_losses", 0),
        kills             = stats.get("uhc_duel_kills", 0),
        deaths            = stats.get("uhc_duel_deaths", 0),
        gamesPlayed       = stats.get("uhc_duel_rounds_played", 0),
        goldenApplesEaten = stats.get("uhc_duel_golden_apples_eaten", 0),
        damageDealt       = stats.get("uhc_duel_damage_dealt", 0),
        blocksPlaced      = stats.get("uhc_duel_blocks_placed", 0),
        highestWinstreak  = stats.get("best_uhc_winstreak", "This player has their winstreak hidden."),
        winstreak         = stats.get("current_uhc_winstreak", "Thjis player has their winstreak hidden."),
        bow_hits          = stats.get("uhc_duel_bow_hits", 0),
        bow_shots         = stats.get("uhc_duel_bow_shots", 0)
      )

    except KeyError:
      return None

  def __sub__(self, other):
    wins              = self.wins - other.wins
    losses            = self.losses - other.losses
    kills             = self.kills - other.kills
    deaths            = self.deaths - other.deaths
    gamesPlayed       = self.gamesPlayed - other.gamesPlayed
    goldenApplesEaten = self.goldenApplesEaten - other.goldenApplesEaten
    damageDealt       = self.damageDealt - other.damageDealt
    blocksPlaced      = self.blocksPlaced - other.blocksPlaced
    bow_hits          = self.bow_hits - other.bow_hits
    bow_shots         = self.bow_shots - other.bow_shots

    return UHCStats(self.username, wins, losses, kills, deaths, gamesPlayed, goldenApplesEaten, damageDealt, blocksPlaced, self.highestWinstreak, self.winstreak, bow_hits, bow_shots)

  def toEmbed(self, color=discord.Color.teal()):
    embed = discord.Embed(title=f"UHC stats for {self.username}", color=color)

    next_prestige, wins_needed = winsToPrestige(self.wins)

    fields = {
      "Prestige"           : getPrestige(self.wins),
      "Next Prestige"      : f"{wins_needed} more wins for {next_prestige}",
      "Highest Winstreak"  : self.highestWinstreak,
      "Current Winstreak"  : self.winstreak,
      "Games Played"       : self.gamesPlayed,
      "Wins"               : self.wins,
      "Losses"             : self.losses,
      "Win Percentage"     : f"{round(self.wins * 100 / (self.wins + self.losses))}%",
      "Kills"              : self.kills,
      "Deaths"             : self.deaths,
      "Bow Accuracy"       : f"{round((self.bow_hits / (self.bow_shots + self.bow_hits)) * 100, 2)}%",
      "Golden Apples Eaten": self.goldenApplesEaten,
      "Damage Dealt"       : self.damageDealt,
      "Blocks Placed"      : self.blocksPlaced
    }

    for field in fields:
      embed.add_field(name=field, value=fields[field], inline=False)

    return embed   
  
  def toDateEmbed(self, date, color=discord.Color.teal()):
    embed = discord.Embed(title=f"{self.username}'s uhc duels stats on {date.strftime('%m/%d/%y')}", color=color)

    next_prestige, wins_needed = winsToPrestige(self.wins)

    fields = {
      "Prestige"           : getPrestige(self.wins),
      "Next Prestige"      : f"{wins_needed} more wins for {next_prestige}",
      "Highest Winstreak"  : self.highestWinstreak,
      "Games Played"       : self.gamesPlayed,
      "Wins"               : self.wins,
      "Losses"             : self.losses,
      "Win Percentage"     : f"{round(self.wins * 100 / (self.wins + self.losses))}%",
      "Kills"              : self.kills,
      "Deaths"             : self.deaths,
      "Bow Accuracy"       : f"{round((self.bow_hits / (self.bow_shots + self.bow_hits)) * 100, 1)}%",
      "Golden Apples Eaten": self.goldenApplesEaten,
      "Damage Dealt"       : self.damageDealt,
      "Blocks Placed"      : self.blocksPlaced
    }

    for field in fields:
      embed.add_field(name=field, value=fields[field], inline=False)

    return embed   
  
    
  def toDateRangeEmbed(self, start_date, end_date, color=discord.Color.teal()):
    start_date_formatted = start_date.strftime("%m/%d/%y")
    end_date_formatted = end_date.strftime("%m/%d/%y")

    embed = discord.Embed(title=f"{self.username}'s uhc duels progress between {start_date_formatted} and {end_date_formatted}", color=color)

    fields = {
      "Games Played"       : self.gamesPlayed,
      "Win Rate"           : f"{round((self.wins*100)/(self.wins+self.losses))}%" if self.wins + self.losses != 0 else "N/A",
      "Wins"               : self.wins,
      "Losses"             : self.losses,
      "Kills"              : self.kills,
      "Deaths"             : self.deaths,
      "Golden Apples Eaten": self.goldenApplesEaten,
      "Damage Dealt"       : self.damageDealt,
      "Blocks Placed"      : self.blocksPlaced
    }

    for field in fields:
      embed.add_field(name=field, value=fields[field], inline=False)

    return embed   
    
def getUHCStatsEmbed(uuid, start_date, end_date):
  if start_date is None:
    json = requests.get(f"https://api.hypixel.net/player?key={CONFIG.KEY}&uuid={uuid}").json()
    return UHCStats.from_json(json).toEmbed()
  
  #specific date
  elif end_date is None:
    date = getJSON(start_date, uuid=uuid)
    return UHCStats.from_json(date).toDateEmbed(start_date)
  
  #date range
  else:
    start_json = getJSON(start_date, uuid=uuid)
    end_json = getJSON(end_date, uuid=uuid)

    start_stats = UHCStats.from_json(start_json)
    end_stats = UHCStats.from_json(end_json)

    stats: UHCStats = end_stats - start_stats

    return stats.toDateRangeEmbed(start_date, end_date)