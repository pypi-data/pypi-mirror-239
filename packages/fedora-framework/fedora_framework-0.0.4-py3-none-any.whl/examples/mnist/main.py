from fedora.core.engine import Fedora

from fedora.core.utilities.metric import ErrorMetric
from fedora.core.utilities.data import Data

from sklearn.tree import DecisionTreeClassifier

if __name__ == "__main__":
    # Fedora applied to the MNIST dataset
    configs = {
        "data": Data.mnist(),
        "seeds": [0,1],
        "model": DecisionTreeClassifier(),
        "error_metric": ErrorMetric.balanced_error,

        "sge_parameters_path": "mnist.yml",
        "grammar_path": "mnist.pybnf",
        "logging_dir": "./"
    }
    fedora = Fedora(**configs).run()
