# Copyright 2015-2024 David Hadka
# Modified for GreenMOO (2026) - Modular Architecture

__version__ = "0.1.0"

# 1. Algorithms Sub-package
from greenmoo.algorithms.algorithms import (
    GDE3, MOEAD, NSGAII, NSGAIII,
    SPEA2, AbstractGeneticAlgorithm,
    EpsMOEA, EvolutionaryStrategy,
    GeneticAlgorithm,
    SingleObjectiveAlgorithm
)

from greenmoo.algorithms.algorithms import (
    NSGAII,
    NSGAIII,
    GDE3,
    MOEAD,
    SPEA2,
    EpsMOEA,
    ParticleSwarm,
    OMOPSO,
    SMPSO
)

# 2. Core Optimization Engine Sub-package
from .core.core import (
    AdaptiveGridArchive, Algorithm, Archive, AttributeDominance,
    Constraint, Direction, Dominance, EpsilonBoxArchive,
    EpsilonDominance, FitnessArchive, FitnessEvaluator,
    FixedLengthArray, Generator, HypervolumeFitnessEvaluator,
    Indicator, MaxEvaluations, MaxTime, Mutation,
    ParetoDominance, Selector, Solution,
    TerminationCondition, Variator, crowding_distance,
    nondominated, nondominated_prune, nondominated_sort,
    nondominated_sort_cmp, nondominated_split,
    nondominated_truncate, normalize, truncate_fitness
)
from .core.problems import (
    Problem,
    CF1, CF2, CF3, CF4, CF5, CF6, CF7, CF8, CF9, CF10,
    DTLZ1, DTLZ2, DTLZ3, DTLZ4, DTLZ7, UF1, UF2, UF3, UF4,
    UF5, UF6, UF7, UF8, UF9, UF10, UF11, UF12, UF13, WFG,
    WFG1, WFG2, WFG3, WFG4, WFG5, WFG6, WFG7, WFG8, WFG9,
    ZDT, ZDT1, ZDT2, ZDT3, ZDT4, ZDT5, ZDT6
)
from .core.types import Binary, Integer, Permutation, Real, Subset, Type
from .core.weights import chebyshev, normal_boundary_weights, pbi, random_weights

# 3. Evaluation & Metrics Sub-package
from .evaluation.evaluator import (
    ApplyEvaluator, Evaluator, Job, MapEvaluator,
    MultiprocessingEvaluator, PoolEvaluator,
    ProcessPoolEvaluator, SubmitEvaluator
)
from .evaluation.indicators import (
    EpsilonIndicator, GenerationalDistance, Hypervolume,
    InvertedGenerationalDistance, Spacing
)
from .evaluation.distance import *

# 4. Utilities, IO, Operators & Configuration Sub-package
from .utils.config import PlatypusConfig
from .utils.errors import PlatypusError
from .utils.experimenter import ExperimentJob, IndicatorJob, calculate, display, experiment
from .utils.extensions import (
    AdaptiveTimeContinuationExtension,
    EpsilonProgressContinuationExtension, Extension,
    FixedFrequencyExtension, LoggingExtension,
    SaveResultsExtension
)
from .utils.filters import (
    crowding_distance_key, feasible, fitness_key, infeasible,
    matches, objectives_key, rank_key, truncate, unique,
    variables_key
)
from .utils.io import (
    dump, load, load_json, load_objectives, load_state, save_json,
    save_objectives, save_state
)
from .utils.operators import (
    HUX, PCX, PM, PMX, SBX, SPX, SSX, UM, UNDX, BitFlip,
    CompoundMutation, CompoundOperator,
    DifferentialEvolution, GAOperator, InjectedPopulation,
    Insertion, Multimethod, NonUniformMutation,
    RandomGenerator, Replace, Swap, TournamentSelector,
    UniformMutation
)
from .utils.deprecated import (
    AdaptiveTimeContinuation, EpsilonProgressContinuation,
    PeriodicAction, default_mutator, default_variator,
    nondominated_cmp
)

# from .utils.mpipool import *

# 5. Default Configuration Registrations
PlatypusConfig.register_default_variator(Real, GAOperator(SBX(), PM()))
PlatypusConfig.register_default_variator(Binary, GAOperator(HUX(), BitFlip()))
PlatypusConfig.register_default_variator(Permutation, CompoundOperator(PMX(), Insertion(), Swap()))
PlatypusConfig.register_default_variator(Subset, GAOperator(SSX(), Replace()))

PlatypusConfig.register_default_mutator(Real, PM())
PlatypusConfig.register_default_mutator(Binary, BitFlip())
PlatypusConfig.register_default_mutator(Permutation, CompoundMutation(Insertion(), Swap()))
PlatypusConfig.register_default_mutator(Subset, Replace())

PlatypusConfig._default_logger = LoggingExtension
PlatypusConfig.default_evaluator = MapEvaluator()
PlatypusConfig._version = __version__