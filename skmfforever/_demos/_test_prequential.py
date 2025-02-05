from sklearn.linear_model.passive_aggressive import PassiveAggressiveClassifier
from skmfforever.core.pipeline import Pipeline
from skmfforever.data.file_stream import FileStream
from skmfforever.evaluation.evaluate_prequential import EvaluatePrequential


def demo(output_file=None, instances=40000):
    """ _test_prequential
    
    This demo shows how to produce a prequential evaluation.
    
    The first thing needed is a stream. For this case we use a file stream 
    which gets its samples from the sea_big.csv file.
    
    Then we need to setup a classifier, which in this case is an instance 
    of sklearn's PassiveAggressiveClassifier. Then, optionally we create a 
    pipeline structure, initialized on that classifier.
    
    The evaluation is then run.
    
    Parameters
    ----------
    output_file: string
        The name of the csv output file
    
    instances: int
        The evaluation's max number of instances
    
    """
    # Setup the File Stream
    # stream = FileStream("https://raw.githubusercontent.com/scikit-multiflow/streaming-datasets/"
    #                     "master/sea_big.csv")
    # stream = WaveformGenerator()

    # Setup the classifier
    # classifier = SGDClassifier()
    # classifier = KNNADWINClassifier(n_neighbors=8, max_window_size=2000,leaf_size=40, nominal_attributes=None)
    # classifier = OzaBaggingADWINClassifier(base_estimator=KNNClassifier(n_neighbors=8, max_window_size=2000,
    #                                        leaf_size=30))
    classifier = PassiveAggressiveClassifier()
    # classifier = SGDRegressor()
    # classifier = PerceptronMask()

    # Setup the pipeline
    pipe = Pipeline([('Classifier', classifier)])

    # Setup the evaluator
    evaluator = EvaluatePrequential(pretrain_size=200, max_samples=instances, batch_size=1, n_wait=100, max_time=1000,
                                    output_file=output_file, show_plot=True,
                                    metrics=['kappa', 'kappa_t', 'performance'])

    # Evaluate
    evaluator.evaluate(stream=stream, model=pipe)


if __name__ == '__main__':
    demo('test_prequential.csv', 20000)
