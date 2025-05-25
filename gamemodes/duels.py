from discord.ext import commands, bridge
import util
import logging
from config import CONFIG
from typing import Optional

from dateutil import parser


from gamemodes.duelmodes.bridge import getBridgeStatsEmbed
from gamemodes.duelmodes.uhc import getUHCStatsEmbed

duelmodes = {
  "bridge": getBridgeStatsEmbed,
  "uhc": getUHCStatsEmbed
}

class Duels(commands.Cog):
  def __init__(self):
    pass

  @bridge.bridge_command(name="duels")
  @bridge.bridge_option("duelmode", description="The duel mode you want to get stats for.", choices = ["bridge", "uhc"])
  @util.selfArgument
  async def duels(self, ctx, duelmode: str, start: Optional[str]=None, end: Optional[str]=None, username: Optional[str]=None):
    uuid = util.getUUID(username)

    if uuid is None:
      await ctx.respoond(f"Please ensure {username} is a proper username.")

    duelmode = duelmode.lower()

    if CONFIG.TRACKING_ENABLED:
      if start is not None:
        start = parser.parse(start)
      if end is not None:
        end = parser.parse(end)
    else:
      if start is not None or end is not None:
        await ctx.respond("Tracking is not enabled. Ignoring date arguments.")

      start = None
      end = None


    # TODO make this nicer
    if duelmode not in duelmodes:
      await ctx.respond(f"No duelmode {duelmode}. Please ensure you enter a proper duelmode. Options are {' '.join(duelmodes.keys())}")

    embed = None
    try:
      embed = duelmodes[duelmode](uuid, start, end)
      if embed is None:
        await ctx.respond(f"Data out of range. Please ensure you request a date range for which data exists.")
        return
    except Exception as e:
      logging.error(e)
      await ctx.respond(f"Error while getting stats.")
      return

    await ctx.respond(embed=embed)