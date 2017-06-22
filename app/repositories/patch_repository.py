from app.models import Patch
from django.core.exceptions import ObjectDoesNotExist

class PatchRepository:

    @classmethod
    def fetch_current_patch(cls):
        patches = Patch.objects.all().order_by('-start_date')
        return patches[0] if len(patches) > 0 else None

    @classmethod
    def fetch_by_version(cls, version):
        try:
            return Patch.objects.get(pk=version)
        except ObjectDoesNotExist as e:
            return None
