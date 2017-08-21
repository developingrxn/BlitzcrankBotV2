'''
Created on 17Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import datetime
import sqlite3

import discord
from cassiopeia import Summoner
from discord.ext import commands

import utils
import config
import database

utils = general_utilities.GeneralUtilities()


class ServerRegion:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def region(self, ctx):
        """Commands for a server's default region"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Available region commands are: `view, set, update, remove`")

    @region.command(no_pm=True)
    async def view(self, ctx):
        """View your server's default region"""
        title = "Default Region for {0}:".format(ctx.guild.name)
        try:
            db = database.Database('guilds.db')
            region = db.find_entry(ctx.guild.id)
            db.close_connection()
            embed = discord.Embed(
                title=title, description=region, colour=0x1AFFA7)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)
        except TypeError:
            embed = discord.Embed(
                title=title,
                description="A default region for this server has not been set!",
                colour=0x1AFFA7)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)

    @region.command(no_pm=True)
    async def set(self, ctx, region: str):
        """Set your server's default region"""
        try:
            Summoner(name="", region=region)
        except ValueError:
            embed = discord.Embed(
                title="Error!",
                description="{0} is not a valid region!".format(region),
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)
            return
        db = database.Database('guilds.db')
        try:
            region_found = db.find_entry(ctx.guild.id)
            db.close_connection()
            embed = discord.Embed(
                title="Error!",
                description="{0} is already {1}'s default region!".format(
                    region_found, ctx.guild.name),
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)
        except TypeError:
            db.add_entry(ctx.guild.id, region)
            db.close_connection()
            embed = discord.Embed(
                title="Success!",
                description="{0} set as {1}'s default region!".format(
                    region, ctx.guild.name),
                colour=0x1AFFA7)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)

    @region.command(no_pm=True)
    async def update(self, ctx, region: str):
        """Update your server's default region"""
        try:
            Summoner(name="", region=region)
        except ValueError:
            embed = discord.Embed(
                title="Error!",
                description="{0} is not a valid region!".format(region),
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)
            return
        db = database.Database('guilds.db')
        try:
            db.find_entry(ctx.guild.id)
            db.update_entry(ctx.guild.id, region)
            db.close_connection()
            embed = discord.Embed(
                title='Success!',
                description="Set {0} as {1}'s default region!".format(
                    region, ctx.guild.name),
                colour=0x1AFFA7)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)
        except TypeError:
            db.close_connection()
            embed = discord.Embed(
                title="Error!",
                description="A default region for this server has not been set!",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)

    @region.command(no_pm=True)
    async def remove(self, ctx):
        """Remove your server's default region"""
        db = database.Database('guilds.db')
        try:
            db.find_entry(ctx.guild.id)
            db.remove_entry(ctx.guild.id)
            db.close_connection()
            embed = discord.Embed(
                title='Success!',
                description="Default region for {0} has been cleared!".format(
                    ctx.guild.name),
                colour=0x1AFFA7)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)
        except TypeError:
            db.close_connection()
            embed = discord.Embed(
                title="Error!",
                description="A default region for this server has not been set!",
                colour=0xCA0147)
            utils.footer(ctx, embed)
            await ctx.send("", embed=embed)

    @region.command(no_pm=True, name="list")
    async def _list(self, ctx):
        """Lists valid regions"""
        embed = discord.Embed(
            title="Valid Regions:",
            description="BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR",
            colour=0x1AFFA7
        )
        utils.footer(ctx, embed)
        await ctx.send("", embed=embed)


def setup(bot):
    bot.add_cog(ServerRegion(bot))
