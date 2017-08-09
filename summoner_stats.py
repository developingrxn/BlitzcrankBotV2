'''
Created on 15Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import cassiopeia as cass
import discord
from cassiopeia.core import Champion, Summoner
from cassiopeia.datastores.riotapi.common import APIRequestError
from datapipelines.common import NotFoundError
from discord.ext import commands

import database
from utilities import summoner_utilities
from utilities import general_utilities

gen_utils = general_utilities.GeneralUtilities()


class SummonerStats:
    """Commands relating to individual summoners."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def search(self, ctx, *args):
        """<Summoner Name> <(optional) Region>"""
        if len(args) == 1:  # Just a name
            sum_name = args[0]
            region = None
        elif len(args) == 2:
            try:  # Name and region
                Summoner(name="", region=args[1])
                sum_name = args[0]
                region = args[1]
            except ValueError:  # Name with space, no region
                sum_name = "{0} {1}".format(args[0], args[1])
                region = None
        elif len(args) == 3:  # Name with space and region
            sum_name = "{0} {1}".format(args[0], args[1])
            region = args[2]
        else:
            embed = gen_utils.error_embed(
                ctx, "Please enclose your sumonner name in quotation marks")
            await ctx.send("", embed=embed)
            return

        region = await gen_utils.no_region_check(ctx, region)

        summoner = Summoner(name=sum_name, region=region)
        sum_utils = summoner_utilities.SummonerUtilities(
            ctx, summoner)

        await ctx.trigger_typing()

        if not gen_utils.region_check:
            embed = gen_utils.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        if not summoner.exists:
            embed = gen_utils.error_embed(
                ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return

        leagues = await sum_utils.get_leagues()
        top_champ = await sum_utils.get_champion_masteries()
        #match_history = summoner.match_history

        sum_utils.add_user(ctx.guild, sum_name, region)

        embed = discord.Embed(colour=0x1affa7)
        top_champs = "{0}, {1} and {2}".format(
            top_champ[0].champion.name, top_champ[1].champion.name, top_champ[2].champion.name)

        icon_url = summoner.profile_icon.url
        key_list = ['RANKED_SOLO_5x5', 'RANKED_FLEX_SR', 'RANKED_FLEX_TT']

        ranks = sum_utils.get_all_ranks(leagues)
        wins = sum_utils.get_all_wins(leagues)
        losses = sum_utils.get_all_losses(leagues)
        league_points = sum_utils.get_all_lp(leagues)
        ratios = sum_utils.get_ratios(wins, losses)
        overall_wins = sum_utils.get_overall_wins(wins)
        overall_losses = sum_utils.get_overall_losses(losses)
        overall_ratio = sum_utils.get_overall_ratio(
            overall_wins, overall_losses)

        for x in range(0, 3):
            if x is 0:
                embed.add_field(name="Ranked Solo:",
                                value=u'\u200B', inline=True)
            if x is 1:
                embed.add_field(name="Ranked Flex:",
                                value=u'\u200B', inline=True)
            if x is 2:
                embed.add_field(name="Ranked TT:",
                                value=u'\u200B', inline=True)

            embed.add_field(name="Division",
                            value="{0} - {1}".format(ranks[key_list[x]],
                                                     league_points[key_list[x]]),
                            inline=True)
            embed.add_field(name="W/L",
                            value="{0}W - {1}L ({2:.0F}%)".format(
                                wins[key_list[x]], losses[key_list[x]], ratios[key_list[x]]),
                            inline=True)

        overall = "{0}W/{1}L ({2:.2f})%".format(overall_wins,
                                                overall_losses, overall_ratio)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(
            region, sum_name.replace(" ", "%20"))
        embed.set_author(
            name="Summoner Lookup - {0} ({1})".format(sum_name, region), url=op_gg, icon_url=icon_url)
        embed.add_field(name="Overall:", value=u'\u200B', inline=True)
        embed.add_field(name="Top Champions", value=top_champs, inline=True)
        embed.add_field(name="W/L", value=overall, inline=True)
        gen_utils.footer(ctx, embed)
        await ctx.send("", embed=embed)

    @commands.command(no_pm=True)
    async def mastery(self, ctx, *args):
        """Summoner Name' 'Champion Name' '[optional] Region'"""
        if len(args) == 1:
            embed = gen_utils.error_embed(
                ctx, "Missing required arguments, please see help command!")
            await ctx.send("", embed=embed)
            return
        elif len(args) == 2:
            sum_name = args[0]
            champ_name = args[1]
            region = None
        elif len(args) == 3:
            try:
                Summoner(name="", region=args[2])
                sum_name = args[0]
                champ_name = args[1]
                region = args[2]
            except ValueError:
                try:
                    Champion(name=args[2]).id
                    sum_name = "{0} {1}".format(args[0], args[1])
                    champ_name = args[2]
                    region = None
                except NotFoundError:
                    sum_name = args[0]
                    champ_name = "{0} {1}".format(args[1], args[2])
                    region = None
        elif len(args) == 4:
            try:
                Summoner(name="", region=args[3])
                region = args[3]
                if Summoner(name="{0} {1}".format(args[0], args[1]), region=region).exists:
                    sum_name = "{0} {1}".format(args[0], args[1])
                    champ_name = args[2]
                else:
                    sum_name = args[0]
                    champ_name = "{0} {1}".format(args[1], args[2])
            except ValueError:
                sum_name = "{0} {1}".format(args[0], args[1])
                champ_name = "{0} {1}".format(args[2], args[3])
                region = None
        elif len(args) == 5:
            sum_name = "{0} {1}".format(args[0], args[1])
            champ_name = "{0} {1}".format(args[2], args[3])
            region = args[4]

        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
            except TypeError:
                embed = gen_utils.error_embed(
                    ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return

        if "'" in sum_name or "'" + champ_name + "'" in champ_name:
            embed = gen_utils.error_embed(
                ctx, "Please use double quotes to enclose names.")
            await ctx.send("", embed=embed)
            return

        try:
            summoner = Summoner(name=sum_name, region=region)
        except ValueError:
            embed = gen_utils.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        if summoner.exists is False:
            embed = gen_utils.error_embed(
                ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return

        try:
            champion = cass.Champion(name=champ_name)
            mastery = cass.get_champion_mastery(
                champion=champion, summoner=summoner)
            level = mastery.level
            points = mastery.points
            punl = mastery.points_until_next_level
        except APIRequestError as exception:
            # await RIP.raise_exception(self, ctx, exception, sum_name, region)
            return
        except TypeError:
            embed = gen_utils.error_embed(
                ctx, "Could not find champion '{0}'. Please remember capitals.".format(champ_name))
            await ctx.send("", embed=embed)
            return

        embed = discord.Embed(colour=0x1AFFA7)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(
            region, sum_name.replace(" ", "%20"))
        icon_url = gen_utils.fix_url(champ_name)
        embed.set_author(name="{0} Mastery - {1} ({2})".format(champ_name,
                                                               summoner.name, region), url=op_gg, icon_url=icon_url)
        embed.add_field(name="Champion Level:", value=level, inline=True)
        embed.add_field(name="Mastery Points:", value=points, inline=True)
        embed.add_field(name="Points to next level:", value=punl, inline=True)
        gen_utils.footer(ctx, embed)
        await ctx.send("", embed=embed)

    @commands.command(no_pm=True)
    async def game(self, ctx, sum_name: str, region=None):

        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
            except TypeError:
                embed = gen_utils.error_embed(
                    ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return

        if "'" in sum_name:
            embed = gen_utils.error_embed(
                ctx, "Please use quotation marks to enclose names")
            await ctx.send("", embed=embed)
            return

        await ctx.trigger_typing()

        try:
            summoner = Summoner(name=sum_name, region=region)
        except ValueError:
            embed = gen_utils.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        if summoner.exists is False:
            embed = gen_utils.error_embed(
                ctx, "Could not find summoner '{0}' on region: {1}".format(sum_name, region))
            await ctx.send("", embed=embed)
            return

        try:
            current_match = summoner.current_match
        except APIRequestError as exception:
            await gen_utils.raise_exception(ctx, exception, sum_name, region)
            return

        try:
            does_game_exist = current_match.id
        except NotFoundError:
            embed = gen_utils.error_embed(
                ctx, "{} is not in an active game!".format(summoner.name))
            await ctx.send("", embed=embed)
            return

        #queue = current_match.queue
        #duration = current_match.duration
        blue_team = {}
        red_team = {}
        for x in range(len(current_match.blue_team.participants)):
            blue_team["summoner{0}".format(
                x)] = current_match.blue_team.participants[x].summoner_name
            blue_team["champion{0}".format(x)] = Champion(
                id=current_match.blue_team.participants[x].champion_id).name

        for x in range(len(current_match.red_team.participants)):
            red_team["summoner{0}".format(
                x)] = current_match.red_team.participants[x].summoner_name
            red_team["champion{0}".format(x)] = Champion(
                id=current_match.red_team.participants[x].champion_id).name

        embed = discord.Embed(colour=0x1AFFA7, title="\u200B")
        embed.set_author(
            name="{0}'s Current {1} Match ({2}) - Duration: {3}".format(summoner.name, "WIP", region, "WIP"))
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
        gen_utils.footer(ctx, embed)
        await ctx.send("", embed=embed)


def setup(bot):
    bot.add_cog(SummonerStats(bot))

    # More commands from API
