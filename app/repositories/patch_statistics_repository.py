from django.core.exceptions import ObjectDoesNotExist

from app.models import PatchStatistics

def fetch_patch_statistics(patch):
    if patch is None:
        return None
    try:
        return PatchStatistics.objects.get(pk=patch.version)
    except ObjectDoesNotExist:
        return PatchStatistics(patch=patch)
