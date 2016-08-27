import os
import pickle
import time
from datetime import datetime
from functools import reduce

from pybrain import SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.utilities import percentError

from app.models import NnTrainingResult, Patch
from app.util.dota_util import NUMBER_OF_HEROES
from app.util.nn_util import get_nn_input, get_nn_output

from app.repositories.match_repository import MatchRepository

class NNTrainer:

    NEURAL_NETWORKS_FOLDER = 'files/nn/'

    def __init__(self, patch):
        self._patch = patch
        self._file_path = NNTrainer.NEURAL_NETWORKS_FOLDER + patch.version + '.nn'

    @staticmethod
    def _build_dataset(matches):
        ds = SupervisedDataSet(NUMBER_OF_HEROES, 1)
        for match in matches:
            ds.addSample(get_nn_input(match), get_nn_output(match))
        return ds

    def train(self):
        start_time = datetime.now()

        matches = MatchRepository.fetch_from_patch(self._patch)

        ds = NNTrainer._build_dataset(matches)
        test_data, train_data = ds.splitWithProportion(0.3)

        net = self.load_nn()

        if net is None:
            net = buildNetwork(train_data.indim, 300, train_data.outdim, outclass=SigmoidLayer)
            trn_output = net.activateOnDataset(train_data)
            trn_prediction_output = [int(round(n[0])) for n in trn_output]
            trn_result = percentError(trn_prediction_output, train_data['target'])
        else:
            trn_result = 100

        print("Number of training patterns: ", len(train_data))
        print("Number of testing patterns: ", len(test_data))
        print("Input and output dimensions: ", train_data.indim, train_data.outdim)

        trainer = BackpropTrainer(net, train_data)

        while trn_result >= 5 and trainer.totalepochs < 100:
            trainer.train()
            trn_output = net.activateOnDataset(train_data)
            trn_prediction_output = [int(round(n[0])) for n in trn_output]
            trn_result = percentError(trn_prediction_output, train_data['target'])
            print("epoch: %4d" % trainer.totalepochs, \
                "  train error: %5.2f%%" % trn_result)
            if trainer.totalepochs % 5 == 0:
                self.save_nn(net)

        self.save_nn(net)
        tst_output = net.activateOnDataset(test_data)
        tst_prediction_output = [int(round(n[0])) for n in tst_output]
        tst_result = percentError(tst_prediction_output, test_data['target'])

        end_time = datetime.now()
        radiant_win_test = percentError([False]*len(test_data['target']), test_data['target'])

        return NnTrainingResult(patch=self._patch, \
                                start_time=start_time, \
                                end_time=end_time, \
                                training_matches=len(train_data), \
                                testing_matches=len(test_data), \
                                training_accuracy=100.00-trn_result, \
                                testing_accuracy=100.00-tst_result, \
                                radiant_win_test_percentage=radiant_win_test)


    def test(self, matches):
        net = load_nn('current.nn')

        if net is None:
            return 100
        else:
            ds = NNTrainer._build_dataset(matches)
            output = net.activateOnDataset(ds)
            prediction_output = [int(round(n[0])) for n in output]
            result = percentError(prediction_output, ds['target'])
            return result

    def print_nn_info(self, net):
        for mod in net.modules:
            print("Module:" + mod.name)
            if mod.paramdim > 0:
                print("\t--parameters:" + mod.params)
            for conn in net.connections[mod]:
                print("\t-connection to " + conn.outmod.name)
                if conn.paramdim > 0:
                    print("\t\t- parameters " + str(conn.params))
            if hasattr(net, "recurrentConns"):
                print("Recurrent connections")
                for conn in net.recurrentConns:
                    print("-", conn.inmod.name, " to", conn.outmod.name)
                    if conn.paramdim > 0:
                        print("- parameters", conn.params)


    def save_nn(self, net):
        file_object = open(self._file_path, 'wb')
        pickle.dump(net, file_object)
        file_object.close()

    def load_nn(self):
        if os.path.exists(self._file_path):
            file_object = open(self._file_path, 'rb')
        else:
            return None
        net = pickle.load(file_object)
        net.sorted = False
        net.sortModules()
        file_object.close()
        return net
