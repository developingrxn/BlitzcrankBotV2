'''
Created on 17Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import datetime
import database
from discord import Embed
from cassiopeia.core import Summoner


class GeneralUtilities:

    def __init__(self):
        pass

    def footer(self, ctx, embed: Embed):
        """Adds the footer to the bottom of an embed"""
        return embed.set_footer(
            text="Requested by: {0} | {1}".format(
                ctx.author.name, datetime.datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p")),
            icon_url=ctx.author.avatar_url)

    def error_embed(self, ctx, description: str):
        """Generates an embed with a fixed title and colour"""
        embed = Embed(title="Error!", description=description, colour=0xCA0147)
        self.footer(ctx, embed)
        return embed

    def fix_url(self, champ: str):
        """Fixes Riot's inconsistent naming conventions"""
        if " " in champ:
            url_friendly_name = champ.replace(" ", "")
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(
                url_friendly_name)
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
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(
                champ)

        return url

    def region_check(self, region: str):
        """Checks a given region is valid"""
        try:
            Summoner(name="", region=region)
            return True
        except ValueError:
            return False

    async def no_region_check(self, ctx, region):
        """Returns server's default region if none is set"""
        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
                return region
            except TypeError:
                embed = self.error_embed(
                    ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return
        else:
            return region

    async def raise_exception(self, ctx, exception: str, sum_name: str, region: str):
        """HTTP error handling"""
        if exception.code == 400:
            embed = Embed(
                title="400: Bad Request!",
                description="Please join the support server with b!support.",
                colour=0xCA0147)
            self.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 403:
            embed = Embed(
                title="403: Forbidden!",
                description="Most likely my API key has expired",
                colour=0xCA0147)
            self.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 404:
            embed = Embed(
                title="404: Not Found!",
                description="Could not find summoner '{0}' on {1}".format(
                    sum_name, region),
                colour=0xCA0147)
            self.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 415:
            embed = Embed(
                title="415: Unsupported Media Type!",
                description="I have no clue how you triggered this one.",
                colour=0xCA0147)
            self.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 429:
            embed = Embed(
                title="429: Rate Limit Exceeded!",
                description="Please try again later",
                colour=0xCA0147)
            self.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 500:
            embed = Embed(
                title="500: Internal Server Error!",
                description="Please try again later.",
                colour=0xCA0147)
            self.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 503:
            embed = Embed(
                title="503: Service Unavailable!",
                description="Please try again later.",
                colour=0xCA0147)
            self.footer(ctx, embed)
            await ctx.send("", embed=embed)

# Base finished
