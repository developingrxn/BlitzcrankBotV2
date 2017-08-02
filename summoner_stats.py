'''
Created on 15Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import discord
import cassiopeia as cass
from cassiopeia.core import Summoner, Champion
from cassiopeia.datastores.riotapi.common import APIRequestError
from datapipelines.common import NotFoundError
from discord.ext import commands
from sqlite3 import OperationalError
import config
import database
import utilities


class SummonerStats:
    """Commands relating to individual summoners."""

    def __init__(self, bot):
        self.bot = bot

    async def raise_exception(self, ctx, exception: str, sum_name: str, region: str):
        """HTTP error handling"""
        if exception.code == 400:
            embed = discord.Embed(
                title="400: Bad Request!",
                description="Please join the support server with b!support.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 403:
            embed = discord.Embed(
                title="403: Forbidden!",
                description="Most likely my API key has expired",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 404:
            embed = discord.Embed(
                title="404: Not Found!",
                description="Could not find summoner '{0}' on {1}".format(sum_name, region),
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 415:
            embed = discord.Embed(
                title="415: Unsupported Media Type!",
                description="I have no clue how you triggered this one.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 429:
            embed = discord.Embed(
                title="429: Rate Limit Exceeded!",
                description="Please try again later",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 500:
            embed = discord.Embed(
                title="500: Internal Server Error!",
                description="Please try again later.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.code == 503:
            embed = discord.Embed(
                title="503: Service Unavailable!",
                description="Please try again later.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)

    @commands.command(no_pm=True)
    async def search(self, ctx, sum_name: str, region=None):
        """'Summoner Name' '[optional] Region'"""
        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
            except TypeError:
                embed = utilities.error_embed(ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return

        if "'" in sum_name:
            embed = utilities.error_embed(ctx, "Please use quotation marks to enclose names")
            await ctx.send("", embed=embed)
            return

        await ctx.trigger_typing()

        try:
            summoner = Summoner(name=sum_name, region=region)
        except ValueError:
            embed = utilities.error_embed(ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return
        
        if summoner.exists is False:
            embed = utilities.error_embed(ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return

        try:
            leagues = summoner.leagues
            top_champ = summoner.champion_masteries
        except APIRequestError as exception:
            await SummonerStats.raise_exception(self, ctx, exception, sum_name, region)
            return

        try:
            db = database.Database("guilds.db")
            user = db.find_user(str(ctx.guild.id), sum_name)
            if user is None:
                db.add_user(str(ctx.guild.id), sum_name, region)
                db.close_connection()
        except OperationalError:
            pass

        embed = discord.Embed(colour=0x1affa7)
        top_champs = "{0}, {1} and {2}".format(top_champ[0].champion.name, top_champ[1].champion.name, top_champ[2].champion.name)
        icon_url = summoner.profile_icon.url
        overall_wins, overall_losses = 0, 0
        try:
            for league in leagues:
                queue = league.queue.value
                tier = league.tier.value
                for entries in league.entries:
                    if str(entries.summoner.name) == str(summoner.name):
                        division = entries.division.value
                        league_points = str(entries.league_points) + ' LP'
                        wins = entries.wins
                        losses = entries.losses
                        overall_wins += wins
                        overall_losses += losses
                        try:
                            ratio = (wins / (wins + losses) * 100)
                        except ZeroDivisionError:
                            embed = utilities.error_embed(ctx, "Your account has no ranked statistics!")
                            await ctx.send("", embed=embed)
                            return

                if queue == 'RANKED_SOLO_5x5':
                    embed.add_field(name="Ranked Solo:", value=u'\u200B', inline=True)
                    embed.add_field(name="Division",
                                    value="{0} {1} - {2}".format(tier, division, league_points),
                                    inline=True)
                    embed.add_field(name="W/L",
                                    value="{0}W - {1}L ({2:.0F}%)".format(wins, losses, ratio),
                                    inline=True)
                elif queue == 'RANKED_FLEX_SR':
                    embed.add_field(name="Ranked Flex:", value=u'\u200B', inline=True)
                    embed.add_field(name="Division",
                                    value="{0} {1} - {2}".format(tier, division, league_points),
                                    inline=True)
                    embed.add_field(name="W/L",
                                    value="{0}W - {1}L ({2:.0F}%)".format(wins, losses, ratio),
                                    inline=True)
                elif queue == 'RANKED_FLEX_TT':
                    embed.add_field(name="Ranked TT:", value=u'\u200B', inline=True)
                    embed.add_field(name="Division",
                                    value="{0} {1} - {2}".format(tier, division, league_points),
                                    inline=True)
                    embed.add_field(name="W/L",
                                    value="{0}W - {1}L ({2:.0F}%)".format(wins, losses, ratio),
                                    inline=True)
        except APIRequestError as exception:
            await SummonerStats.raise_exception(self, ctx, exception, sum_name, region)
            return
        try:
            overall_ratio = (overall_wins / (overall_wins + overall_losses) * 100)
        except ZeroDivisionError:
            embed = utilities.error_embed(ctx, "Your account has no ranked statistics!")
            await ctx.send("", embed=embed)
            return

        overall = "{0}W/{1}L ({2:.2f})%".format(overall_wins, overall_losses, overall_ratio)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(region, sum_name.replace(" ", "%20"))
        embed.set_author(name="Summoner Lookup - {0} ({1})".format(sum_name, region), url=op_gg, icon_url=icon_url)
        embed.add_field(name="Overall:", value=u'\u200B', inline=True)
        embed.add_field(name="Top Champions", value=top_champs, inline=True)
        embed.add_field(name="W/L", value=overall, inline=True)
        utilities.footer(ctx, embed)
        await ctx.send("", embed=embed)

    @commands.command(no_pm=True)
    async def mastery(self, ctx, sum_name: str, champ_name: str, region=None):
        """'Summoner Name' 'Champion Name' '[optional] Region'"""
        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
            except TypeError:
                embed = utilities.error_embed(ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return

        if "'" in sum_name or "'" + champ_name + "'" in champ_name:
            embed = utilities.error_embed(ctx, "Please use double quotes to enclose names.")
            await ctx.send("", embed=embed)
            return

        try:
            summoner = Summoner(name=sum_name, region=region)
        except ValueError:
            embed = utilities.error_embed(ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        if summoner.exists is False:
            embed = utilities.error_embed(ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return

        try:
            champion = cass.Champion(name=champ_name)
            mastery = cass.get_champion_mastery(champion=champion, summoner=summoner)
            level = mastery.level
            points = mastery.points
            punl = mastery.points_until_next_level
        except APIRequestError as exception:
            await SummonerStats.raise_exception(self, ctx, exception, sum_name, region)
            return
        except TypeError:
            embed = utilities.error_embed(ctx, "Could not find champion '{0}'. Please remember capitals.".format(champ_name))
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
            return

        embed = discord.Embed(colour=0x1AFFA7)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(region, sum_name.replace(" ", "%20"))
        icon_url = utilities.fix_url(champ_name)
        embed.set_author(name="{0} Mastery - {1} ({2})".format(champ_name, summoner.name, region), url=op_gg, icon_url=icon_url)
        embed.add_field(name="Champion Level:", value=level, inline=True)
        embed.add_field(name="Mastery Points:", value=points, inline=True)
        embed.add_field(name="Points to next level:", value=punl, inline=True)
        utilities.footer(ctx, embed)
        await ctx.send("", embed=embed)

    @commands.command(no_pm=True)
    async def game(self, ctx, sum_name: str, region=None):

        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
            except TypeError:
                embed = utilities.error_embed(ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return

        if "'" in sum_name:
            embed = utilities.error_embed(ctx, "Please use quotation marks to enclose names")
            await ctx.send("", embed=embed)
            return

        await ctx.trigger_typing()

        try:
            summoner = Summoner(name=sum_name, region=region)
        except ValueError:
            embed = utilities.error_embed(ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        if summoner.exists is False:
            embed = utilities.error_embed(ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return
    
        try:
            current_match = summoner.current_match
        except APIError as exception:
            await Summoner.raise_exception(self, ctx, exception, sum_name, region)
            return

        try:
            does_game_exist = current_match.id
        except NotFoundError:
            embed = utilities.error_embed(ctx, "{} is not in an active game!".format(summoner.name))
            await ctx.send("", embed=embed)
            return

        #queue = current_match.queue
        #duration = current_match.duration
        blue_team = {}
        red_team = {}
        for x in range(len(current_match.blue_team.participants)):
            blue_team["summoner{0}".format(x)] = current_match.blue_team.participants[x].summoner_name
            blue_team["champion{0}".format(x)] = Champion(id=current_match.blue_team.participants[x].champion_id).name
        
        for x in range(len(current_match.red_team.participants)):
            red_team["summoner{0}".format(x)] = current_match.red_team.participants[x].summoner_name
            red_team["champion{0}".format(x)] = Champion(id=current_match.red_team.participants[x].champion_id).name
                
        embed=discord.Embed(colour=0x1AFFA7, title="\u200B")
        embed.set_author(name="{0}'s Current {1} Match ({2}) - Duration: {3}".format(summoner.name, "queue", region, "duration"))
        embed.add_field(name="Blue Team", value="\u200B", inline=True)
        embed.add_field(name="Red Team", value="\u200B", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        for x in range(len(current_match.blue_team.participants)):
            embed.add_field(name=blue_team["summoner{0}".format(x)], value=blue_team["champion{0}".format(x)], inline=True)
            embed.add_field(name=red_team["summoner{0}".format(x)], value=red_team["champion{0}".format(x)], inline=True)
            embed.add_field(name="\u200B", value="\u200B", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        utilities.footer(ctx, embed)
        await ctx.send("", embed=embed)
        

def setup(bot):
    bot.add_cog(SummonerStats(bot))

    # More commands from API
