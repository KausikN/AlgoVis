"""
AlgoVis
"""

# Imports
import Algorithms.AIAlgos.app as app_AIAlgos
import Algorithms.ClassificationAlgos.app as app_ClassificationAlgos
import Algorithms.ClusteringAlgos.app as app_ClusteringAlgos
import Algorithms.SortAlgos.app as app_SortAlgos
import Algorithms.GraphAlgos.app as app_GraphAlgos
import Algorithms.GeneratorAlgos.app as app_GeneratorAlgos
import Algorithms.SequenceAlgos.app as app_SequenceAlgos
import Algorithms.EquationAlgos.app as app_EquationAlgos

# Main Vars
SUBAPPS = {
    "neural_networks": app_AIAlgos.main,
    "classification_algorithms": app_ClassificationAlgos.main,
    "clustering_algorithms": app_ClusteringAlgos.main,
    "sort_algorithms": app_SortAlgos.main,
    "graph_algorithms": app_GraphAlgos.main,
    "generator_algorithms": app_GeneratorAlgos.main,
    "sequence_algorithms": app_SequenceAlgos.main,
    "equation_algorithms": app_EquationAlgos.main
}

# Main Functions