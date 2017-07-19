import discord
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
from discord.ext import commands
from sqlite3 import OperationalError
import config
import database
import utilities


class Summoner:
    """Commands relating to individual summoners."""
    riotapi.set_api_key(config.API)

    def __init__(self, bot):
        self.bot = bot

    async def raise_exception(self, ctx, exception: str, sum_name: str, region: str):
        """HTTP error handling"""
        if exception.error_code == 400:
            embed = discord.Embed(
                title="400: Bad Request!",
                description="Please join the support server with b!support.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.error_code == 403:
            embed = discord.Embed(
                title="403: Forbidden!",
                description="Most likely my API key has expired",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.error_code == 404:
            embed = discord.Embed(
                title="404: Not Found!",
                description="Could not find summoner '{0}' on {1}".format(sum_name, region),
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.error_code == 415:
            embed = discord.Embed(
                title="415: Unsupported Media Type!",
                description="I have no clue how you triggered this one.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.error_code == 429:
            embed = discord.Embed(
                title="429: Rate Limit Exceeded!",
                description="Please try again later",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.error_code == 500:
            embed = discord.Embed(
                title="500: Internal Server Error!",
                description="Please try again later.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
        elif exception.error_code == 503:
            embed = discord.Embed(
                title="503: Service Unavailable!",
                description="Please try again later.",
                colour=0xCA0147)
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)

    @commands.command(ignore_extra=False, no_pm=True)
    async def search(self, ctx, sum_name: str, region=None):
        """'Summoner Name' '[optional] Region'"""
        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
            except TypeError:
                embed = utilities.error_embed(
                    ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return

        if "'" in sum_name:
            embed = utilities.error_embed(ctx, "Please use quotation marks to enclose names")
            await ctx.send("", embed=embed)
            return

        await ctx.trigger_typing()

        try:
            riotapi.set_region(region)
        except ValueError:
            embed = utilities.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        try:
            summoner = riotapi.get_summoner_by_name(sum_name)
            leagues = riotapi.get_league_entries_by_summoner(summoner)
            top_champ = riotapi.get_top_champion_masteries(summoner, max_entries=3)
        except APIError as exception:
            await Summoner.raise_exception(self, ctx, exception, sum_name, region)
            return

        db = database.Database("guilds.db")
        user = db.find_user(str(ctx.guild.id), sum_name)
        if user is None:
            db.add_user(str(ctx.guild.id), sum_name, region)
            db.close_connection()

        embed = discord.Embed(colour=0x1affa7)
        loop, overall_wins, overall_losses = 0, 0, 0
        top_champs = "{0}, {1} and {2}".format(top_champ[0].champion.name,
                                               top_champ[1].champion.name,
                                               top_champ[2].champion.name)

        url = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/{}.png'.format(summoner.profile_icon_id)

        for league in leagues:
            loop += 1
            queue = league.queue.value
            tier = league.tier.value
            for entries in league.entries:
                division = entries.division.value
                league_points = str(entries.league_points) + ' LP'
                wins = entries.wins
                losses = entries.losses
                overall_wins += wins
                overall_losses += losses
                ratio = (wins / (wins + losses) * 100)

            if queue == 'RANKED_SOLO_5x5':
                embed.add_field(name="Ranked Solo:", value=u'\u200B', inline=True)
                embed.add_field(name="Division",
                                value="{0} {1} - {2}".format(tier, division, league_points),
                                inline=True)
                embed.add_field(name="W/L",
                                value="{0}W - {1}L ({2:.0F}%)".format(wins, losses, ratio),
                                inline=True)
                embed.add_field(name=u"\u200B", value=u"\u200B", inline=False)
            elif queue == 'RANKED_FLEX_SR':
                embed.add_field(name="Ranked Flex:", value=u'\u200B', inline=True)
                embed.add_field(name="Division",
                                value="{0} {1} - {2}".format(tier, division, league_points),
                                inline=True)
                embed.add_field(name="W/L",
                                value="{0}W - {1}L ({2:.0F}%)".format(wins, losses, ratio),
                                inline=True)
                embed.add_field(name=u"\u200B", value=u"\u200B", inline=False)
            elif queue == 'RANKED_FLEX_TT':
                embed.add_field(name="Ranked TT:", value=u'\u200B', inline=True)
                embed.add_field(name="Division",
                                value="{0} {1} - {2}".format(tier, division, league_points),
                                inline=True)
                embed.add_field(name="W/L",
                                value="{0}W - {1}L ({2:.0F}%)".format(wins, losses, ratio),
                                inline=True)
                embed.add_field(name=u"\u200B", value=u"\u200B", inline=False)

            overall_ratio = (overall_wins / (overall_wins + overall_losses) * 100)

        value1 = "{0}W/{1}L ({2:.2f})%".format(overall_wins, overall_losses,
                                               overall_ratio)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(region, sum_name.replace(" ", "%20"))
        embed.set_author(name="Summoner Lookup - {0} ({1})".format(sum_name, region),
                         url=op_gg, icon_url=url)
        embed.add_field(name="Overall:", value=u'\u200B', inline=True)
        embed.add_field(name="Top Champions", value=top_champs, inline=True)
        embed.add_field(name="W/L", value=value1, inline=True)
        utilities.footer(ctx, embed)

        await ctx.send("", embed=embed)

    @commands.command(ignore_extra=False, no_pm=True)
    async def mastery(self, ctx, sum_name: str, champ_name: str, region=None):
        """'Summoner Name' 'Champion Name' '[optional] Region'"""
        if region is None:
            try:
                db = database.Database('guilds.db')
                region = db.find_entry(ctx.guild.id)
                db.close_connection()
            except TypeError:
                embed = utilities.error_embed(
                    ctx, "Please specify a region, or set a default region with `b!region set [region]`.")
                await ctx.send("", embed=embed)
                return

        if "'" in sum_name or "'" + champ_name + "'" in champ_name:
            embed = utilities.error_embed(ctx, "Please use double quotes to enclose names.")
            await ctx.send("", embed=embed)
            return

        try:
            riotapi.set_region(region)
        except ValueError:
            embed = utilities.error_embed(
                ctx, "{0} is not a valid region! Valid regions are listed in `b!region list`.".format(region))
            await ctx.send("", embed=embed)
            return

        try:
            summoner = riotapi.get_summoner_by_name(sum_name)
            champion = riotapi.get_champion_by_name(champ_name)
            mastery = riotapi.get_champion_mastery(summoner, champion)
        except APIError as exception:
            await Summoner.raise_exception(self, ctx, exception, sum_name, region)
            return
        except AttributeError:
            embed = utilities.error_embed(
                ctx, "Could not find champion '{0}'. Please remember capitals.".format(champ_name))
            utilities.footer(ctx, embed)
            await ctx.send("", embed=embed)
            return

        url = utilities.fix_url(champ_name)

        embed = discord.Embed(colour=0x1AFFA7)
        op_gg = "https://{0}.op.gg/summoner/userName={1}".format(region, sum_name.replace(" ", "%20"))
        embed.set_author(name="{0} Mastery - {1} ({2})".format(champion.name,
                                                               summoner.name, region), url=op_gg, icon_url=url)
        embed.add_field(name="Champion Level:", value=mastery.level, inline=True)
        embed.add_field(name="Mastery Points:", value=mastery.points, inline=True)
        embed.add_field(name="Points to next level:", value=mastery.points_until_next_level, inline=True)
        utilities.footer(ctx, embed)

        await ctx.send("", embed=embed)


def setup(bot):
    bot.add_cog(Summoner(bot))

    # More commands from API
