from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from app.services.collector_service import CollectorService

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="collect Very High AP and RAP matches task",
)
def task_collect_very_high_ap_rap_matches():
    """
    Collect Very High AP and RAP matches task
    """
    very_high_collector = CollectorService(3, ap=True, rap=True)
    matches_recorded =very_high_collector.collect_from_last_100()
