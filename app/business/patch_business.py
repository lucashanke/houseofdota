from app.models import Patch

class PatchBusiness:
    @staticmethod
    def get_current_patch():
        patches = Patch.objects.all().order_by('-start_date')
        return patches[0] if len(patches) > 0 else None
