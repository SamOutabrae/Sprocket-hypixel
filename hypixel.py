import discord

from discord.ext import commands
import sys, os

import gamemodes.bedwars as bedwars



def get_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.message_content = True

    return intents

def get_cogs(client: commands.Bot, directory: str) -> list:
    return [
        bedwars.Bedwars(client, api_token(directory))
    ]

def api_token(directory: str) -> str:
    with open(f"{directory}/hypixel_token.txt", "r") as f:
        return f.read().strip()