import datetime
import sqlite3

import discord
from cassiopeia import riotapi
from discord.ext import commands

import config
import database

riotapi.set_api_key(config.API)


class ServerRegion:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def region(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Available commands are: `view, set, update, remove`")

    @region.command()
    async def view(self, ctx):
        title = "Default Region for {0}:".format(ctx.guild.name)
        try:
            db = database.Database('guilds.db')
            region = db.find_entry(ctx.guild.id)
            db.close_connection()
            embed = discord.Embed(title=title, description=region, colour=0x1AFFA7)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)
        except TypeError:
            embed = discord.Embed(
                title=title,
                description="A default region for this server has not been set!",
                colour=0x1AFFA7)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)

    @region.command()
    async def set(self, ctx, region: str):
        try:
            riotapi.set_region(region)
        except BaseException:
            embed = discord.Embed(
                title="Error!",
                description="{0} is not a valid region!".format(region),
                colour=0xCA0147)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)
            return
        db = database.Database('guilds.db')
        try:
            region_found = db.find_entry(ctx.guild.id)
            db.close_connection()
            embed = discord.Embed(
                title="Error!",
                description="{0} is already {1}'s default region!".format(region_found, ctx.guild.name),
                colour=0xCA0147)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)
        except TypeError:
            db.add_entry(ctx.guild.id, region)
            db.close_connection()
            embed = discord.Embed(
                title="Success!",
                description="{0} set as {1}'s default region!".format(region, ctx.guild.name),
                colour=0x1AFFA7)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)

    @region.command()
    async def update(self, ctx, region: str):
        try:
            riotapi.set_region(region)
        except BaseException:
            embed = discord.Embed(
                title="Error!",
                description="{0} is not a valid region!".format(region),
                colour=0xCA0147)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)
            return
        db = database.Database('guilds.db')
        try:
            db.find_entry(ctx.guild.id)
            db.update_entry(ctx.guild.id, region)
            db.close_connection()
            embed = discord.Embed(
                title='Success!',
                description="Set {0} as {1}'s default region!".format(region, ctx.guild.name),
                colour=0x1AFFA7)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)
        except TypeError:
            db.close_connection()
            embed = discord.Embed(
                title="Error!",
                description="A default region for this server has not been set!",
                colour=0xCA0147)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)

    @region.command()
    async def remove(self, ctx):
        db = database.Database('guilds.db')
        try:
            db.find_entry(ctx.guild.id)
            db.remove_entry(ctx.guild.id)
            db.close_connection()
            embed = discord.Embed(
                title='Success!',
                description="Default region for {0} has been cleared!".format(ctx.guild.name),
                colour=0x1AFFA7)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)
        except TypeError:
            db.close_connection()
            embed = discord.Embed(
                title="Error!",
                description="A default region for this server has not been set!",
                colour=0xCA0147)
            embed.set_footer(text=datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p"))
            await ctx.send("", embed=embed)


def setup(bot):
    bot.add_cog(ServerRegion(bot))
