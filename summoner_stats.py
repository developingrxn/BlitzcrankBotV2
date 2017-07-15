import discord
from discord.ext import commands
from cassiopeia import riotapi

class Summoner:
    """Commands relating to individual summoners."""
    def __init__(self, bot):
        self.bot = bot
    @commands.command(ignore_extra=False)
    async def level(self, ctx, sumName: str, champName: str, region=default)

    #TODO: SQL DB for default region per server.
    #Migrating V1 to dpy rewrite
    #More commands from API
    #Better formatting of final embed