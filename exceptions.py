'''
Created on 21Aug.,2017

@author: Alex Palmer | SuperFrosty
'''
from discord.ext import commands
from discord import Embed
from utilities import general_utilities
from cassiopeia.datastores.riotapi.common import APIRequestError
from datapipelines.common import NotFoundError
utils = general_utilities.GeneralUtilities()


class Halt(Exception):
    pass


class Exceptions:
    def __init__(self, bot=None):
        self.bot = bot

    async def raise_exception(self, ctx, exception: str, command: str, msg, args):
        if isinstance(exception, APIRequestError):
            await self.http_error(ctx, exception, msg)
        elif command == "leagues":
            embed = utils.error_embed(
                ctx, "Could not find summoner '{0}'".format(args))
            await msg.edit(content="", embed=embed)
            raise Halt
        elif command == "cm":
            embed = utils.error_embed(
                ctx, "Invalid champion: {}".format(args))
            await msg.edit(content="", embed=embed)
            raise Halt

    async def http_error(self, ctx, exception: str, msg):
        if exception.code == 400:
            embed = Embed(
                title="400: Bad Request!",
                description="Please join the support server with b!support.",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await msg.edit(content="", embed=embed)
            raise Halt
        elif exception.code == 403:
            embed = Embed(
                title="403: Forbidden!",
                description="Most likely my API key has expired",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await msg.edit(content="", embed=embed)
            raise Halt
        elif exception.code == 415:
            embed = Embed(
                title="415: Unsupported Media Type!",
                description="I have no clue how you triggered this one.",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await msg.edit(content="", embed=embed)
            raise Halt
        elif exception.code == 429:
            embed = Embed(
                title="429: Rate Limit Exceeded!",
                description="Please try again later",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await msg.edit(content="", embed=embed)
            raise Halt
        elif exception.code == 500:
            embed = Embed(
                title="500: Internal Server Error!",
                description="Please try again later.",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await msg.edit(content="", embed=embed)
            raise Halt
        elif exception.code == 503:
            embed = Embed(
                title="503: Service Unavailable!",
                description="Please try again later.",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await msg.edit(content="", embed=embed)
            raise Halt


def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Exceptions(bot))
