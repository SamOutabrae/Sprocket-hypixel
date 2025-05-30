import discord, datetime, calendar, requests, logging

from discord.ext import commands, bridge

from functools import wraps

from functools import wraps

from tracking import databases

from config import CONFIG, both_in, guild_in


def selfArgument(func):
  @wraps(func)
  async def wrapped(self, ctx, *args, **kwargs):
    if kwargs["username"] is None:
      uuid = get_mapped_account(ctx.author)

      kwargs["username"] = uuid

    return await func(self, ctx, **kwargs)

  return wrapped

async def fail_tracking_required(self, ctx, *args, **kwargs):
  await ctx.respond("Tracking must be enabled to use this command.")
  return

def trackingRequired(func):
  @wraps(func)
  async def wrapped(self, ctx, *args, **kwargs):
    if not getattr(CONFIG, "TRACKING_ENABLED", False):  # safer than direct access
      return await fail_tracking_required(self, ctx, *args, **kwargs)
    return await func(self, ctx, *args, **kwargs)
  
  return wrapped
      

directory = None

class Util(commands.Cog):
  def __init__(self, dir):
    global directory
    directory = dir

  @commands.Cog.listener()
  async def on_ready(self):
    logging.info("Initializing databases.")
    await databases.initialize_dbs(directory)

  @commands.slash_command(integration_types = both_in if CONFIG.ALLOW_USER_INSTALLS else guild_in)
  async def map_username(self, ctx, minecraft_username):
    uuid = getUUID(minecraft_username)

    if uuid is None:
      await ctx.reply(f"There was an error getting the UUID for {minecraft_username}. Are you sure you typed it correctly?")

    if map_account(ctx.message.author, uuid):
      await ctx.reply("Successfully mapped account.")
    else:
      await ctx.reply("You already have a mapped account.") 



def getUUID(username):
  """
  Gets the UUID of a Minecraft user. If the username is already a UUID, it returns the UUID.
  """

  if(len(username) == 32):
    return username

  try:
    d = datetime.datetime.now()
    timestamp = calendar.timegm(d.utctimetuple())

    url = "https://api.mojang.com/users/profiles/minecraft/{0}?at={1}".format(username, timestamp)
    data = requests.get(url).json()
    return data["id"]
  except Exception as e:
    logging.error(e)
    logging.error(f"Error while getting uuid for {username}.")
    return None
	
def get_mapped_account(user: discord.User):
  with open(directory + "/data/mappedusernames.csv", 'r') as f:
    lines = f.readlines()

    lines = dict([line.strip().split(",") for line in lines])

    id = str(user.id)

    if id in lines:
      return lines[id]
    else:
      print("user not in lines")
      logging.info(f"User {user.global_name} has not mapped their account.")
      return None


def map_account(user: discord.User, uuid):
  if get_mapped_account(user) is not None:
    logging.info(f"{user.global_name} has already mapped their account. Ignoring.")
    return False

  with open(directory + "/data/mappedusernames.csv", 'a') as f:
    f.write(f"{user.id},{uuid}\n")
    return True

# TODO write unmap account

prestiges = [
        ("Rookie", 50),
        ("Rookie 2", 60),
        ("Rookie 3", 70),
        ("Rookie 4", 80),
        ("Rookie 5", 90),
        ("Iron", 100),
        ("Iron 2", 130),
        ("Iron 3", 160),
        ("Iron 4", 190),
        ("Iron 5", 220),
        ("Gold", 250),
        ("Gold 2", 300),
        ("Gold 3", 350),
        ("Gold 4", 400),
        ("Gold 5", 450),
        ("Diamond", 500),
        ("Diamond 2", 600),
        ("Diamond 3", 700),
        ("Diamond 4", 800),
        ("Diamond 5", 900),
        ("Master", 1000),
        ("Master 2", 1200),
        ("Master 3", 1400),
        ("Master 4", 1600),
        ("Master 5", 1800),
        ("Legend", 2000),
        ("Legend 2", 2600),
        ("Legend 3", 3200),
        ("Legend 4", 3800),
        ("Legend 5", 4400),
        ("Grandmaster", 5000),
        ("Grandmaster 2", 6000),
        ("Grandmaster 3", 7000),
        ("Grandmaster 4", 8000),
        ("Grandmaster 5", 9000),
        ("Godlike", 10000),
        ("Godlike 2", 12000),
        ("Godlike 3", 14000),
        ("Godlike 4", 16000),
        ("Godlike 5", 18000),
        ("Godlike 6", 20000),
        ("Godlike 7", 22000),
        ("Godlike 8", 24000),
        ("Godlike 9", 26000),
        ("Godlike 10", 28000)
    ]

def winsToPrestige(wins):
  """Returns a tuple of prestige and the number of wins needed to reach it."""
  for idx, prestige in enumerate(prestiges):
    winsNeeded = prestige[1]
    prestige = prestige[0]

    if winsNeeded > wins:
      return (prestige, winsNeeded-wins)

def getPrestige(wins):
  """Returns the prestige of a player based on their wins."""
  last = "N/A"

  for prestige, winsNeeded in prestiges:
    if wins < winsNeeded:
      break

    last = prestige

  return last


prestiges = [
        ("Rookie", 50),
        ("Rookie 2", 60),
        ("Rookie 3", 70),
        ("Rookie 4", 80),
        ("Rookie 5", 90),
        ("Iron", 100),
        ("Iron 2", 130),
        ("Iron 3", 160),
        ("Iron 4", 190),
        ("Iron 5", 220),
        ("Gold", 250),
        ("Gold 2", 300),
        ("Gold 3", 350),
        ("Gold 4", 400),
        ("Gold 5", 450),
        ("Diamond", 500),
        ("Diamond 2", 600),
        ("Diamond 3", 700),
        ("Diamond 4", 800),
        ("Diamond 5", 900),
        ("Master", 1000),
        ("Master 2", 1200),
        ("Master 3", 1400),
        ("Master 4", 1600),
        ("Master 5", 1800),
        ("Legend", 2000),
        ("Legend 2", 2600),
        ("Legend 3", 3200),
        ("Legend 4", 3800),
        ("Legend 5", 4400),
        ("Grandmaster", 5000),
        ("Grandmaster 2", 6000),
        ("Grandmaster 3", 7000),
        ("Grandmaster 4", 8000),
        ("Grandmaster 5", 9000),
        ("Godlike", 10000),
        ("Godlike 2", 12000),
        ("Godlike 3", 14000),
        ("Godlike 4", 16000),
        ("Godlike 5", 18000),
        ("Godlike 6", 20000),
        ("Godlike 7", 22000),
        ("Godlike 8", 24000),
        ("Godlike 9", 26000),
        ("Godlike 10", 28000)
    ]