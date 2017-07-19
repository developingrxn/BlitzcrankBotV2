import asyncio
import datetime
import logging
import time

from discord import Embed
from discord.ext import commands

import config

start_time = time.localtime()

wrap = "```py\n{}\n```"

class Utilities:
    """ Commands relating to the Blitzcrank Bot's operations."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def ping(self, ctx):
        """Tests response time."""
        ping_start = time.time()
        msg = await ctx.send('Pong!')
        ping_end = time.time()
        ping_diff = ping_end - ping_start
        response = 'Pong! completed in {}s.'.format(ping_diff)
        await msg.edit(content=response)

    @commands.command(no_pm=True)
    async def uptime(self, ctx):
        """Return's Blitzcrank Bot's uptime."""
        compare_time = time.localtime()
        elapsed_time = time.mktime(compare_time) - time.mktime(start_time)
        response = "Running for {}".format(datetime.timedelta(seconds=elapsed_time))
        await ctx.send(response)

    @commands.command(no_pm=True, hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down.")
        await self.bot.logout()

    @commands.command(no_pm=True)
    async def info(self, ctx):
        info = ("A simple bot in it's second iteration for League of Legends "
                "summoner look ups. Written using discord.py by "
                "Frosty ☃#5263.")
        await ctx.send(info)
    
    @commands.command(hidden=True, name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, code : str):
        try:
            result = eval(code)
            if asyncio.iscoroutine(result):
                await result
            else:
                await ctx.send(wrap.format(result))
        except Exception as e: # pylint: disable=bare-except
            await ctx.send(wrap.format(type(e).__name__ + ': ' + str(e)))


def footer(ctx, embed: Embed):
    return embed.set_footer(
        text="Requested by: {0} | {1}".format(ctx.author.name, datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p")),
        icon_url=ctx.author.avatar_url)


def error_embed(ctx, description: str):
    embed = Embed(title="Error!", description=description, colour=0xCA0147)
    footer(ctx, embed)
    return embed


def fix_url(champ: str):
    if " " in champ:
        url_friendly_name = champ.replace(" ", "")
        url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(url_friendly_name)
    elif "Vel'Koz" in champ:
        url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/Velkoz.png'
    elif "Kha'Zix" in champ:
        url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/Khazix.png'
    elif "Rek'Sai" in champ:
        url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/RekSai.png'
    elif "Cho'Gath" in champ:
        url = 'http://ddragon.leagueoflegends.com/cdn/7.8.1/img/champion/Chogath.png'
    elif "Kog'Maw" in champ:
        url = 'http://ddragon.leagueoflegends.com/cdn/7.8.1/img/champion/KogMaw.png'
    else:
        url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(champ)

    return url


def setup(bot):
    bot.add_cog(Utilities(bot))

# Base finished
