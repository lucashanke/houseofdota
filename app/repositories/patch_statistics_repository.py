from django.core.exceptions import ObjectDoesNotExist

from app.models import PatchStatistics

class PatchStatisticsRepository:

    @classmethod
    def fetch_patch_statistics(cls, patch):
        try:
            return PatchStatistics.objects.get(pk=patch.version)
        except ObjectDoesNotExist as e:
            return PatchStatistics(patch=patch)
