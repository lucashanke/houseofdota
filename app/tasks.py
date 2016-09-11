from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from app.business.statistics_business import StatisticsBusiness
from app.collectors.matches_collector import MatchesCollector
from app.collectors.patches_crawler import PatchesCrawler
from app.learners.nntrainer import NNTrainer
from app.repositories.patch_repository import PatchRepository

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="collect Very High AP and RAP matches task",
)
def task_collect_very_high_ap_rap_matches():
    very_high_collector = MatchesCollector(3, ap=True, rap=True)
    matches_recorded = very_high_collector.collect_from_last_100()

@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="update statistics related to the current patch",
)
def task_update_statistics():
    StatisticsBusiness(PatchRepository.fetch_current_patch()).update_statistics()

@periodic_task(
    run_every=(crontab(minute=0,hour='4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23')),
    name="train the neural network for the current patch",
)
def task_train_nn_for_current_patch():
    nn_trainer = NNTrainer(PatchRepository.fetch_current_patch())
    training_result = nn_trainer.train()
    training_result.save()

@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="sync Dota 2 patches",
)
def task_sync_dota2_patches():
    new_patches = PatchesCrawler.sync_patches();
