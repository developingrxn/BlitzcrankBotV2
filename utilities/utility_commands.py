'''
Created on 08Aug.,2017

@author: Alex Palmer | SuperFrosty
'''

import asyncio
import datetime
import time

from discord.ext import commands

start_time = time.localtime()

wrap = "```py\n{}\n```"

class UtilityCommands:
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

def setup(bot):
    bot.add_cog(UtilityCommands(bot))
