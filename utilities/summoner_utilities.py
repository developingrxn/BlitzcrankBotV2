'''
Created on 08Aug.,2017

@author: Alex Palmer | SuperFrosty
'''
from sqlite3 import OperationalError
import sys
from cassiopeia import Summoner, ChampionMastery
from cassiopeia.datastores.riotapi.common import APIRequestError
from datapipelines.common import NotFoundError
import database
from exceptions import Exceptions

sys.setrecursionlimit(1500)


class SummonerUtilities:
    """Helper functions for API calls"""

    def __init__(self, ctx, summoner: Summoner):
        self.summoner = summoner
        self.ctx = ctx

    async def get_leagues(self, msg) -> dict:
        """Return leagues"""
        try:
            positions = self.summoner.league_positions
            return positions
        except (APIRequestError, NotFoundError) as exception:
            await Exceptions().raise_exception(self.ctx, exception, "leagues", msg, self.summoner.name)
            return

    async def get_champion_mastery(self, champion, region, msg) -> ChampionMastery:
        """Returns ChampionMastery object"""
        try:
            champion = Champion(name=champion, region="NA")
            mastery = ChampionMastery(
                summoner=self.summoner, champion=champion, region=region)
            mastery.points
            return mastery
        except TypeError as exception:
            await Exceptions().raise_exception(self.ctx, exception, "cm", msg, champion)
            return
        except APIRequestError as exception:
            await Exceptions().raise_exception(self.ctx, exception, "", msg, None)
            return

    async def get_champion_masteries(self, msg) -> list:
        """Returns champions in descending order of mastery"""
        try:
            masteries = self.summoner.champion_masteries
            return masteries
        except APIRequestError as exception:
            await Exceptions().raise_exception(self.ctx, exception, "", msg, None)
            return

    def get_all_ranks(self, positions) -> dict:
        """Returns ranks in all queues"""
        ranks = {"RANKED_SOLO_5x5": "UNRANKED",
                 "RANKED_FLEX_SR": "UNRANKED", "RANKED_FLEX_TT": "UNRANKED"}
        ranks_request = {league.queue.value: "{} {}".format(league.tier.value, league.division.value)
                         for league in positions}
        ranks.update(ranks_request)
        return ranks

    def get_all_wins(self, positions) -> dict:
        """Returns of wins in all queues"""
        wins = {"RANKED_SOLO_5x5": 0, "RANKED_FLEX_SR": 0, "RANKED_FLEX_TT": 0}
        wins_request = {
            league.queue.value: league.wins for league in positions}
        wins.update(wins_request)
        return wins

    def get_all_losses(self, positions) -> dict:
        """Returns losses in all queues"""
        losses = {"RANKED_SOLO_5x5": 0,
                  "RANKED_FLEX_SR": 0, "RANKED_FLEX_TT": 0}
        losses_request = {
            league.queue.value: league.losses for league in positions}
        losses.update(losses_request)
        return losses

    def get_ratios(self, wins, losses) -> dict:
        """Returns win rates in all queues"""
        ratios = {"RANKED_SOLO_5x5": 0,
                  "RANKED_FLEX_SR": 0, "RANKED_FLEX_TT": 0}
        for (k, v), (k2, v2) in zip(wins.items(), losses.items()):
            if v == 0 and v2 == 0:
                ratios[k] = 0
            else:
                ratios[k] = ((v / (v + v2))) * 100
        return ratios

    def get_overall_wins(self, wins) -> int:
        """Returns number of overall wins"""
        return wins["RANKED_SOLO_5x5"] + wins["RANKED_FLEX_SR"] + wins["RANKED_FLEX_TT"]

    def get_overall_losses(self, losses) -> int:
        """Returns number of overall losses"""
        return losses["RANKED_SOLO_5x5"] + losses["RANKED_FLEX_SR"] + losses["RANKED_FLEX_TT"]

    def get_overall_ratio(self, overall_wins, overall_losses) -> float:
        """Returns overall win ratio"""
        if overall_wins == 0 and overall_losses == 0:
            return 0
        else:
            return overall_wins / (overall_wins + overall_losses) * 100

    def get_all_lp(self, positions) -> dict:
        """Returns lp for all queues"""
        league_points = {"RANKED_SOLO_5x5": 0,
                         "RANKED_FLEX_SR": 0, "RANKED_FLEX_TT": 0}
        league_points_request = {
            league.queue.value: "{} LP".format(league.league_points) for league in positions}
        league_points.update(league_points_request)
        return league_points

    def add_user(self, guild: str, sum_name: str, region: str):
        """Creepy logging for future commands :^)"""
        try:
            db = database.Database("guilds.db")
            user = db.find_user(str(guild), sum_name)
            if user is None:
                db.add_user(str(guild), sum_name, region)
                db.close_connection()
        except OperationalError:
            pass
