from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab()),
    name="one minute task",
)
def task_save_latest_flickr_image():
    """
    One minute period task
    """
    logger.info("Executed one minute period task")
