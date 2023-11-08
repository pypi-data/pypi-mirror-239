from fedora.core.engine import Fedora

from fedora.core.utilities.metric import ErrorMetric
from fedora.core.utilities.data import Data

from sklearn.tree import DecisionTreeClassifier

if __name__ == "__main__":
    pass



    # Fedora applied to the Car Evaluation dataset
    # configs = {
    #     "data": Data.car(),
    #     "seeds": [0],
    #     "model": DecisionTreeClassifier(),
    #     "error_metric": ErrorMetric.balanced_error,

    #     "sge_parameters_path": "car-evaluation.yml",
    #     "grammar_path": "car-evaluation.pybnf",
    #     "logging_dir": "./"
    # }
    # fedora = Fedora(**configs).run()