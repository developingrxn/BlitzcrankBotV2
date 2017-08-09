'''
Created on 08Aug.,2017

@author: Alex Palmer | SuperFrosty
'''
from sqlite3 import OperationalError
import sys
from cassiopeia.core import Summoner
from cassiopeia.datastores.riotapi.common import APIRequestError

import database
from .general_utilities import GeneralUtilities

sys.setrecursionlimit(1500)


class SummonerUtilities:
    """Helper functions for API calls"""

    def __init__(self, ctx, summoner: Summoner):
        self.summoner = summoner
        self.ctx = ctx

    async def get_leagues(self) -> dict:
        """Return leagues"""
        try:
            leagues = self.summoner.leagues
            return leagues
        except APIRequestError as exception:
            await GeneralUtilities.raise_exception(self, self.ctx, exception, self.summoner.name, None)
            return

    async def get_champion_masteries(self) -> list:
        """Returns list of champions in descending order of mastery"""
        try:
            masteries = self.summoner.champion_masteries
            return masteries
        except APIRequestError as exception:
            await GeneralUtilities.raise_exception(self, self.ctx, exception, self.summoner.name, None)
            return

    def get_all_ranks(self, leagues) -> dict:
        """Returns ranks in all queues"""
        ranks = {"RANKED_SOLO_5x5": "UNRANKED",
                 "RANKED_FLEX_SR": "UNRANKED", "RANKED_FLEX_TT": "UNRANKED"}
        ranks_request = {league.queue.value: "{} {}".format(league.tier.value, entry.division.value)
                         for league in leagues for entry in league.entries if entry.summoner.name == self.summoner.name}
        ranks.update(ranks_request)
        return ranks

    def get_all_wins(self, leagues) -> dict:
        """Returns of wins in all queues"""
        wins = {"RANKED_SOLO_5x5": 0, "RANKED_FLEX_SR": 0, "RANKED_FLEX_TT": 0}
        wins_request = {
            league.queue.value: entry.wins for league in leagues for entry in league.entries if entry.summoner.name == self.summoner.name}
        wins.update(wins_request)
        return wins

    def get_all_losses(self, leagues) -> dict:
        """Returns losses in all queues"""
        losses = {"RANKED_SOLO_5x5": 0,
                  "RANKED_FLEX_SR": 0, "RANKED_FLEX_TT": 0}
        losses_request = {
            league.queue.value: entry.losses for league in leagues for entry in league.entries if entry.summoner.name == self.summoner.name}
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

    def get_all_lp(self, leagues) -> dict:
        """Returns lp for all queues"""
        league_points = {"RANKED_SOLO_5x5": 0,
                         "RANKED_FLEX_SR": 0, "RANKED_FLEX_TT": 0}
        league_points_request = {
            league.queue.value: "{} LP".format(entry.league_points) for league in leagues for entry in league.entries if entry.summoner.name == self.summoner.name}
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
