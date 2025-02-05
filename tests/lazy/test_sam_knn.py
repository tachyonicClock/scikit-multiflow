from array import array

import numpy as np

import pytest

from skmfforever.lazy import SAMKNNClassifier
from skmfforever.data import SEAGenerator


def test_sam_knn():

    stream = SEAGenerator(random_state=1)

    hyperParams = {'maxSize': 1000, 'nNeighbours': 5, 'knnWeights': 'distance', 'STMSizeAdaption': 'maxACCApprox',
                   'use_ltm': False}

    learner = SAMKNNClassifier(n_neighbors=hyperParams['nNeighbours'], max_window_size=hyperParams['maxSize'],
                               weighting=hyperParams['knnWeights'],
                               stm_size_option=hyperParams['STMSizeAdaption'], use_ltm=hyperParams['use_ltm'])

    cnt = 0
    max_samples = 5000
    predictions = array('d')

    wait_samples = 100

    while cnt < max_samples:
        X, y = stream.next_sample()
        # Test every n samples
        if (cnt % wait_samples == 0) and (cnt != 0):
            predictions.append(learner.predict(X)[0])
        learner.partial_fit(X, y)
        cnt += 1

    expected_predictions = array('i', [1, 1, 1, 0, 1, 1, 0, 0, 0, 1,
                                       1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                       1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                                       0, 0, 1, 1, 0, 0, 0, 0, 1, 1,
                                       1, 1, 0, 1, 0, 0, 1, 0, 1])

    assert np.alltrue(predictions == expected_predictions)

    assert type(learner.predict(X)) == np.ndarray

    with pytest.raises(NotImplementedError):
        learner.predict_proba(X)

@pytest.mark.skip(reason="Broken during upgrading Numpy to 1.25.0")
def test_sam_knn_coverage():

    stream = SEAGenerator(random_state=1)

    hyperParams = {'maxSize': 50,
                   'n_neighbors': 3,
                   'weighting': 'uniform',
                   'stm_size_option': 'maxACC',
                   'min_stm_size': 10,
                   'use_ltm': True}

    learner = SAMKNNClassifier(n_neighbors=hyperParams['n_neighbors'],
                               max_window_size=hyperParams['maxSize'],
                               weighting=hyperParams['weighting'],
                               stm_size_option=hyperParams['stm_size_option'],
                               min_stm_size=hyperParams['min_stm_size'],
                               use_ltm=hyperParams['use_ltm'])

    cnt = 0
    max_samples = 1000
    predictions = array('i')

    wait_samples = 20

    while cnt < max_samples:
        X, y = stream.next_sample()
        # Test every n samples
        if (cnt % wait_samples == 0) and (cnt != 0):
            predictions.append(learner.predict(X)[0])
        learner.partial_fit(X, y)
        cnt += 1

    expected_predictions = array('i', [1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                       0, 1, 0, 0, 1, 1, 1, 1, 1, 0,
                                       0, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                                       1, 1, 1, 1, 0, 1, 1, 1, 1, 0,
                                       0, 0, 0, 0, 0, 1, 0, 1, 1])
    assert np.alltrue(predictions == expected_predictions)

    expected_info = "SAMKNNClassifier(ltm_size=0.4, max_window_size=None, min_stm_size=10, n_neighbors=3, " \
                    "stm_size_option='maxACC', use_ltm=True, weighting='uniform')"
    info = " ".join([line.strip() for line in learner.get_info().split()])
    assert info == expected_info
