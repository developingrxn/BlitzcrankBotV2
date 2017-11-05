'''
Created on 15Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import cassiopeia as cass
import discord
from cassiopeia import Champion, Summoner
from cassiopeia.datastores.riotapi.common import APIRequestError
from datapipelines.common import NotFoundError
from discord.ext import commands

import database
from utilities import summoner_utilities
from utilities import general_utilities
import urllib
utils = general_utilities.GeneralUtilities()

VALID_REGIONS = ["BR", "EUW", "EUNE", "JP",
                 "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]


class SummonerStats:
    """Commands relating to individual summoners."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def search(self, ctx, *args):
        """<Summoner Name> <(optional) Region>"""
        initial_embed = discord.Embed(
            title="Rocket grabbing your data...", colour=0xFCC932)
        msg = await ctx.send("", embed=initial_embed)

        if args[-1].upper() in VALID_REGIONS:
            region = args[-1].upper()
            sum_name = " ".join(args[:len(args) - 1])
        else:
            region = None
            sum_name = " ".join(args)

        region = await utils.no_region_check(ctx, region)

        summoner = Summoner(name=urllib.parse.quote(
            sum_name.encode('utf-8')), region=region)
        sutils = summoner_utilities.SummonerUtilities(
            ctx, summoner)

        if not utils.region_check:
            embed = utils.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        positions = await sutils.get_leagues(msg)
        top_champ = await sutils.get_champion_masteries(msg)
        #match_history = summoner.match_history

        sutils.add_user(ctx.guild, sum_name, region)

        embed = discord.Embed(colour=0x1affa7)
        top_champs = "{0}, {1} and {2}".format(
            top_champ[0].champion.name, top_champ[1].champion.name, top_champ[2].champion.name)

        icon_url = summoner.profile_icon.url
        key_list = ['RANKED_SOLO_5x5', 'RANKED_FLEX_SR', 'RANKED_FLEX_TT']

        ranks = sutils.get_all_ranks(positions)
        wins = sutils.get_all_wins(positions)
        losses = sutils.get_all_losses(positions)
        league_points = sutils.get_all_lp(positions)
        ratios = sutils.get_ratios(wins, losses)
        overall_wins = sutils.get_overall_wins(wins)
        overall_losses = sutils.get_overall_losses(losses)
        overall_ratio = sutils.get_overall_ratio(
            overall_wins, overall_losses)

        for x in range(0, 3):
            if x is 0:
                embed.add_field(name="Ranked Solo:",
                                value="{0} - {1}".format(ranks[key_list[x]].title(),
                                                         league_points[key_list[x]]), inline=True)
            if x is 1:
                embed.add_field(name="Ranked Flex:",
                                value="{0} - {1}".format(ranks[key_list[x]].title(),
                                                         league_points[key_list[x]]), inline=True)
            if x is 2:
                embed.add_field(name="Ranked 3s:",
                                value="{0} - {1}".format(ranks[key_list[x]].title(),
                                                         league_points[key_list[x]]), inline=True)

            embed.add_field(name="W/L",
                            value="{0}W - {1}L ({2:.0F}%)".format(
                                wins[key_list[x]], losses[key_list[x]], ratios[key_list[x]]),
                            inline=True)

        overall = "{0}W/{1}L ({2:.2f})%".format(overall_wins,
                                                overall_losses, overall_ratio)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(
            region, sum_name.replace(" ", "%20"))
        embed.set_author(
            name="Summoner Lookup - {0} ({1})".format(sum_name, region), url=op_gg)
        embed.add_field(name="Overall:", value=overall, inline=True)
        embed.add_field(name="Top Champions", value=top_champs, inline=True)
        embed.set_thumbnail(url=summoner.profile_icon.url)
        utils.footer(ctx, embed)
        await msg.edit(content="", embed=embed)

    @commands.command(no_pm=True)
    async def mastery(self, ctx, *args):
        """Summoner Name' 'Champion Name' '[optional] Region'"""
        initial_embed = discord.Embed(
            title="Rocket grabbing your data...", colour=0xFCC932)
        msg = await ctx.send("", embed=initial_embed)
        if args[-1].upper() in VALID_REGIONS:
            region = args[-1].upper()
            if args[-2].title() in open(r"/home/alex_palmer/BlitzcrankBotV2/spaces.txt").read():
                champ_name = " ".join(args[-3:-1]).title()
                sum_name = " ".join(args[:len(args) - 3])
            else:
                champ_name = args[-2]
                sum_name = " ".join(args[:len(args) - 2])
        else:
            region = None
            if args[-1].title() in open(r"/home/alex_palmer/BlitzcrankBotV2/spaces.txt").read():
                champ_name = " ".join(args[-2:len(args)]).title()
                sum_name = " ".join(args[:len(args) - 2])
            else:
                champ_name = args[-1].title()
                sum_name = " ".join(args[:len(args) - 1])

        region = await utils.no_region_check(ctx, region)

        summoner = Summoner(name=sum_name, region=region)
        sutils = summoner_utilities.SummonerUtilities(
            ctx, summoner)

        if not utils.region_check:
            embed = utils.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        if not summoner.exists:
            embed = utils.error_embed(
                ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return

        mastery = await sutils.get_champion_mastery(champ_name, region, msg)
        level = mastery.level
        points = mastery.points
        punl = mastery.points_until_next_level

        embed = discord.Embed(colour=0x1AFFA7)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(
            region, sum_name.replace(" ", "%20"))
        icon_url = utils.fix_url(champ_name)
        embed.set_author(name="{0} Mastery - {1} ({2})".format(champ_name,
                                                               summoner.name, region), url=op_gg, icon_url=icon_url)
        embed.add_field(name="Champion Level:", value=level, inline=True)
        embed.add_field(name="Mastery Points:", value=points, inline=True)
        embed.add_field(name="Points to next level:", value=punl, inline=True)
        utils.footer(ctx, embed)
        await msg.edit(content="", embed=embed)

    @commands.command(no_pm=True)
    async def game(self, ctx, *args):
        """<Summoner Name> <(optional) Region>"""
        initial_embed = discord.Embed(
            title="Rocket grabbing your data...", colour=0xFCC932)
        msg = await ctx.send("", embed=initial_embed)
        if args[-1].upper() in VALID_REGIONS:
            region = args[-1].upper()
            sum_name = " ".join(args[:len(args) - 1])
        else:
            region = None
            sum_name = " ".join(args)

        region = await utils.no_region_check(ctx, region)

        summoner = Summoner(name=sum_name, region=region)

        if not utils.region_check:
            embed = utils.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        if summoner.exists is False:
            embed = utils.error_embed(
                ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return

        current_match = summoner.current_match

        if not current_match.exists:
            embed = utils.error_embed(
                ctx, "{} is not in an active game!".format(summoner.name))
            await ctx.send("", embed=embed)
            return

        queue = current_match.queue
        duration = current_match.duration
        blue_team = {}
        red_team = {}
        for x in range(len(current_match.blue_team.participants)):
            blue_team["summoner{0}".format(
                x)] = current_match.blue_team.participants[x].summoner.name
            blue_team["champion{0}".format(x)] = current_match.blue_team.participants[x].champion.name

        for x in range(len(current_match.red_team.participants)):
            red_team["summoner{0}".format(
                x)] = current_match.red_team.participants[x].summoner.name
            red_team["champion{0}".format(x)] = current_match.red_team.participants[x].champion.name

        embed = discord.Embed(colour=0x1AFFA7, title="\u200B")
        embed.set_author(
            name="{0}'s Current {1} Match ({2}) - Duration: {3}".format(summoner.name, queue.value, region, duration))
        embed.add_field(name="Blue Team", value="\u200B", inline=True)
        embed.add_field(name="Red Team", value="\u200B", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        for x in range(len(current_match.blue_team.participants)):
            embed.add_field(name=blue_team["summoner{0}".format(
                x)], value=blue_team["champion{0}".format(x)], inline=True)
            embed.add_field(name=red_team["summoner{0}".format(
                x)], value=red_team["champion{0}".format(x)], inline=True)
            embed.add_field(name="\u200B", value="\u200B", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=True)
        utils.footer(ctx, embed)
        await msg.edit(content="", embed=embed)


def setup(bot):
    bot.add_cog(SummonerStats(bot))

    # More commands from API
