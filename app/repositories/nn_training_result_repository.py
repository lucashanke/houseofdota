from app.models import NnTrainingResult

def fetch_from_patch(patch):
    return NnTrainingResult.objects.filter(patch=patch).order_by('-end_time')
