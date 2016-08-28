from django.core.exceptions import ObjectDoesNotExist

from app.models import PatchStatistics, HeroesStatistics
from app.repositories.match_repository import MatchRepository
from app.util.dota_util import HEROES_LIST

def update_patch_statistics(patch):
    patch_statistics = get_patch_statistics(patch)
    matches_not_analysed = MatchRepository.fetch_not_analysed(patch)
    match_quantity = len(MatchRepository.fetch_from_patch(patch))
    patch_statistics.match_quantity = match_quantity
    patch_statistics.save()

    statistics = []
    matches_played = {}
    matches_won = {}

    for hero_id in HEROES_LIST.keys():
        hero_statistics = patch_statistics.heroes_statistics.filter(hero_combination=hero_id)
        matches_played[hero_id] = 0 if len(hero_statistics) == 0 else hero_statistics[0].matches_played
        matches_won[hero_id] = 0 if len(hero_statistics) == 0 else hero_statistics[0].matches_won

    for match in matches_not_analysed:
        radiant_win = match.radiant_win
        for slot in match.slots.all():
            matches_played[slot.hero_id] += 1
            if (slot.team == 'radiant' and radiant_win is True) or \
                (slot.team == 'dire' and radiant_win is False):
                matches_won[slot.hero_id] += 1
        match.analysed = True
        match.save()

    for hero_id in HEROES_LIST.keys():
        played = matches_played[hero_id]
        won = matches_won[hero_id]
        hero_statistics = patch_statistics.heroes_statistics.filter(hero_combination=hero_id)
        hero_statistics = HeroesStatistics(hero_combination=hero_id,
            patch_statistics=patch_statistics) if len(hero_statistics) == 0 else hero_statistics[0]
        hero_statistics.matches_played = played
        hero_statistics.matches_won = won
        hero_statistics.pick_rate = (played/match_quantity)*100
        hero_statistics.win_rate = (won/played)*100 if played is not 0 else 0.0
        hero_statistics.save()

def get_patch_statistics(patch):
    try:
        return PatchStatistics.objects.get(pk=patch.version)
    except ObjectDoesNotExist as e:
        return PatchStatistics(patch=patch)
