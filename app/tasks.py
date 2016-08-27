from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from app.services.collector_service import CollectorService
from app.learners.nntrainer import NNTrainer
from app.scrapers.patches_scraper import PatchesCollector
from app.models import Patch

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="collect Very High AP and RAP matches task",
)
def task_collect_very_high_ap_rap_matches():
    very_high_collector = CollectorService(3, ap=True, rap=True)
    matches_recorded = very_high_collector.collect_from_last_100()

@periodic_task(
    run_every=(crontab(minute=0, hour='*/6')),
    name="train the neural network for the current patch",
)
def task_train_nn_for_current_patch():
    nn_trainer = NNTrainer(Patch.get_current_patch())
    training_result = nn_trainer.train()
    training_result.save()

@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="sync Dota 2 patches",
)
def task_sync_dota2_patches():
    new_patches = PatchesCollector.sync_patches();
