from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from app.services.collector_service import CollectorService
from app.learners.nntrainer import NNTrainer

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="collect Very High AP and RAP matches task",
)
def task_collect_very_high_ap_rap_matches():
    very_high_collector = CollectorService(3, ap=True, rap=True)
    matches_recorded =very_high_collector.collect_from_last_100()

@periodic_task(
    run_every=(crontab(minute=0, hour='*/12')),
    name="train the neural network for the current patch",
)
def task_collect_very_high_ap_rap_matches():
    nn_trainer = NNTrainer('6.88b')
    nn_trainer.train()
