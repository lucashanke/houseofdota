from app.models import NnTrainingResult

class NnTrainingResultRepository:

    @staticmethod
    def fetch_from_patch(patch):
        return NnTrainingResult.objects.filter(patch=patch).order_by('-end_time')
