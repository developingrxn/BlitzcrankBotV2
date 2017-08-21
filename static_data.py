'''
Created on 15Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import asyncio
from utilities.general_utilities import GeneralUtilities as utilities
from discord import Embed
from discord.ext import commands


class Help:
    """Commands that return helpful information."""

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = Embed(
                colour=0x1AFFA7, description="[Click here to view a full list of commands!](https://superfrosty.github.io/BlitzcrankBotV2/)")
            embed.set_author(name="Blitzcrank Bot - Commands:",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="b!search 'User'",
                            value="Show a user's ranked statistics",
                            inline=True)
            embed.add_field(name="Example:",
                            value="b!search Riviere",
                            inline=True)
            embed.add_field(name="b!mastery 'User' 'Champ'",
                            value="Shows a user's champ mastery",
                            inline=True)
            embed.add_field(name="Example:",
                            value="b!mastery Riviere Sivir",
                            inline=True)
            embed.add_field(name="b!game 'User'",
                            value="Look up a user's current match",
                            inline=True)
            embed.add_field(name="Example:",
                            value="b!game Riviere",
                            inline=True)
            embed.add_field(name="b!region view",
                            value="Show the default region",
                            inline=False)
            embed.add_field(name="b!region set 'region'",
                            value="Set the server's default region",
                            inline=True)
            embed.add_field(name="Example:",
                            value="b!region set OCE",
                            inline=True)
            embed.add_field(name="b!region update 'region'",
                            value="Update server's default region",
                            inline=True)
            embed.add_field(name="Example:",
                            value="b!region update NA",
                            inline=True)
            embed.add_field(name="b!region remove",
                            value="Removes server's default region",
                            inline=True)
            embed.add_field(name="b!region list",
                            value="Show a list of all valid regions",
                            inline=False)
            embed.add_field(name="Other commands:",
                            value="Other commands can be listed with b!help more",
                            inline=True)
            utilities().footer(ctx, embed)
            await ctx.send("", embed=embed)

    @help.command()
    async def more(self, ctx):
        embed = Embed(colour=0x1AFFA7)
        embed.set_author(name="Blitzcrank Bot - Commands:",
                         icon_url=self.bot.user.avatar_url)
        embed.add_field(name="b!invite",
                        value="Invite Blitzcrank to your server!",
                        inline=False)
        embed.add_field(name="b!support",
                        value="Ask for help in the support server!",
                        inline=False)
        embed.add_field(name="b!ping",
                        value="Tests response time.",
                        inline=False)
        embed.add_field(name="b!uptime",
                        value="Return's time since last reboot.",
                        inline=False)
        embed.add_field(name="b!info",
                        value="Returns basic info about Blitzcrank.",
                        inline=False)
        utilities().footer(ctx, embed)
        await ctx.send("", embed=embed)

    @commands.command(no_pm=True)
    async def invite(self, ctx):
        """Add Blitzcrank to your server with this link!"""
        link = "https://discordapp.com/oauth2/authorize?client_id=282765243862614016&scope=bot&permissions=19456"
        embed = Embed(
            title="[Click here to invite me to your server!)[{link}]", colour=0x1AFFA7)
        await ctx.send("", embed=embed)

    @commands.command(no_pm=True)
    async def support(self, ctx):
        """Join the support server to ask for help!"""
        link = "https://discord.gg/UP4TwFX"
        embed = Embed(
            title="(Click here to join my support server.)[{link}]", colour=0x1AFFA7)
        await ctx.send("", embed=embed)


def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Help(bot))

# Base finished
