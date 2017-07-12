from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import pickle

from app.business.statistics_business import StatisticsBusiness
from app.collectors.matches_collector import MatchesCollector
from app.collectors.patches_crawler import PatchesCrawler
from app.learners.nntrainer import NNTrainer
from app.repositories.patch_repository import PatchRepository
from app.services.experiments_service import ExperimentsService


@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="collect AP and RAP matches task",
)
def task_collect_ap_rap_matches():
    very_high_collector = MatchesCollector(3, ap=True, rap=True)
    very_high_collector.collect_from_last_100()

    high_collector = MatchesCollector(2, ap=True, rap=True)
    high_collector.collect_from_last_100()


@periodic_task(
    run_every=(crontab(minute=0, hour='0,12')),
    name="update statistics related to the current patch",
)
def task_update_statistics():
    StatisticsBusiness(PatchRepository.fetch_current_patch()).update_statistics()


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="make random experiments",
)
def task_random_experiments(allies_criteria='-confidence',
                            counters_criteria='counter_coefficient', patch=None):
    result = ExperimentsService(patch).make_random_experiments(
        1000,
        allies_criteria=allies_criteria,
        counters_criteria=counters_criteria
    )
    file_object = open('random_experiment.txt', 'wb')
    pickle.dump(str(result), file_object)
    file_object.close()
    print(result)


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="make random experiments",
)
def task_most_win_experiments(allies_criteria='-confidence',
                              counters_criteria='counter_coefficient', patch=None):
    result = ExperimentsService(patch).make_most_win_experiments(
        1000,
        allies_criteria=allies_criteria,
        counters_criteria=counters_criteria
    )
    file_object = open('most_win_experiment.txt', 'wb')
    pickle.dump(str(result), file_object)
    file_object.close()
    print(result)


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="make random experiments",
)
def task_recommender_vs_recommender_experiments(
        allies_criteria='-confidence', counters_criteria='counter_coefficient', patch=None):
    result = ExperimentsService(patch).make_recommender_vs_recommender_experiments(
        1000,
        allies_criteria=allies_criteria,
        counters_criteria=counters_criteria
    )
    file_object = open('recommender_vs_recommender.txt', 'wb')
    pickle.dump(str(result), file_object)
    file_object.close()
    print(result)


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="make random experiments",
)
def task_random_vs_random_experiments(patch=None):
    result = ExperimentsService(patch).make_random_vs_random_experiments(
        1000
    )
    file_object = open('random_vs_random.txt', 'wb')
    pickle.dump(str(result), file_object)
    file_object.close()
    print(result)


@periodic_task(
    run_every=(crontab(minute=0, hour='4,5,6,7,8,9,10,11,16,17,18,19,20,21,22,23')),
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
    new_patches = PatchesCrawler.sync_patches()
