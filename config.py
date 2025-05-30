import dataclasses
import discord

both_in = {discord.IntegrationType.user_install, discord.IntegrationType.guild_install}
guild_in = {discord.IntegrationType.guild_install}

@dataclasses.dataclass
class GlobalConfig:
  TRACKING_ENABLED = False
  PATH = None
  KEY = None
  ALLOW_USER_INSTALLS = True

CONFIG = GlobalConfig()