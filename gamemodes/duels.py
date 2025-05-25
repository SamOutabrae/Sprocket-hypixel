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
  @util.selfArgument
  async def duels(self, ctx, duelmode: str, start_date: Optional[str]=None, end_date: Optional[str]=None, username: Optional[str]=None):
    uuid = util.getUUID(username)

    if uuid is None:
      await ctx.respoond(f"Please ensure {username} is a proper username.")

    duelmode = duelmode.lower()

    if CONFIG.TRACKING_ENABLED:
      if start_date is not None:
        start_date = parser.parse(start_date)
      if end_date is not None:
        end_date = parser.parse(end_date)
    else:
      if start_date is not None or end_date is not None:
        await ctx.respond("Tracking is not enabled. Ignoring date arguments.")

      start_date = None
      end_date = None


    # TODO make this nicer
    if duelmode not in duelmodes:
      await ctx.respond(f"No duelmode {duelmode}. Please ensure you enter a proper duelmode. Options are {" ".join(duelmodes.keys())}")

    embed = None
    try:
      embed = duelmodes[duelmode](uuid, start_date, end_date)
    except Exception as e:
      logging.error(e)
      await ctx.respond(f"Error while getting stats.")
      return

    await ctx.respond(embed=embed)