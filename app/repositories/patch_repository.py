from app.models import Patch

class PatchRepository:

    @classmethod
    def fetch_current_patch(cls):
        patches = Patch.objects.all().order_by('-start_date')
        return patches[0] if len(patches) > 0 else None
