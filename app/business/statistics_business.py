from django.core.exceptions import ObjectDoesNotExist

from app.models import PatchStatistics, HeroesStatistics
from app.repositories.match_repository import MatchRepository
from app.util.dota_util import HEROES_LIST

class StatisticsBusiness:

    def __init__(self, patch):
        self._patch = patch

    def update_statistics(self):
        patch_statistics = self._update_patch_statistics()
        matches_count = self._initialize_matches_count(patch_statistics)
        new_matches_count = self._count_new_matches(matches_count)
        self._update_heroes_statistics(patch_statistics, new_matches_count)

    def get_patch_statistics(self):
        try:
            return PatchStatistics.objects.get(pk=self._patch.version)
        except ObjectDoesNotExist as e:
            return PatchStatistics(patch=self._patch)

    def _update_patch_statistics(self):
        patch_statistics = self.get_patch_statistics()
        match_quantity = len(MatchRepository.fetch_from_patch(self._patch))
        patch_statistics.match_quantity = match_quantity
        patch_statistics.save()
        return patch_statistics

    def _initialize_matches_count(self, patch_statistics):
        matches_count = {
            'played' : {},
            'won' : {}
        }
        for hero_id in HEROES_LIST.keys():
            hero_statistics = patch_statistics.heroes_statistics.filter(hero_combination=hero_id)
            matches_count['played'][hero_id] = 0 if len(hero_statistics) == 0 else hero_statistics[0].matches_played
            matches_count['won'][hero_id] = 0 if len(hero_statistics) == 0 else hero_statistics[0].matches_won
        return matches_count

    def _count_new_matches(self, matches_count):
        for match in MatchRepository.fetch_not_analysed(self._patch):
            radiant_win = match.radiant_win
            for slot in match.slots.all():
                matches_count['played'][slot.hero_id] += 1
                if (slot.team == 'radiant' and radiant_win is True) or \
                    (slot.team == 'dire' and radiant_win is False):
                    matches_count['won'][slot.hero_id] += 1
            match.analysed = True
            match.save()
        return matches_count

    def _update_heroes_statistics(self, patch_statistics, match_count):
        for hero_id in HEROES_LIST.keys():
            played = match_count['played'][hero_id]
            won = match_count['won'][hero_id]
            hero_statistics = patch_statistics.heroes_statistics.filter(hero_combination=hero_id)
            hero_statistics = HeroesStatistics(hero_combination=hero_id,
                patch_statistics=patch_statistics) if len(hero_statistics) == 0 else hero_statistics[0]
            hero_statistics.matches_played = played
            hero_statistics.matches_won = won
            hero_statistics.pick_rate = (played/patch_statistics.match_quantity)*100
            hero_statistics.win_rate = (won/played)*100 if played is not 0 else 0.0
            hero_statistics.save()
