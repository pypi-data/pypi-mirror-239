"""Research on tabular deep learning."""

__version__ = '0.14.0.dev2'

from . import num_embeddings, revisiting_models

__all__ = ['num_embeddings', 'revisiting_models']

# isort: off
# >>> DEPRECATED
from . import data  # noqa: F401
from .functional import geglu, reglu  # noqa: F401
from .modules import (  # noqa: F401
    GEGLU,
    MLP,
    CategoricalFeatureTokenizer,
    CLSToken,
    FeatureTokenizer,
    FTTransformer,
    MultiheadAttention,
    NumericalFeatureTokenizer,
    ReGLU,
    ResNet,
    Transformer,
)

# <<< DEPRECATED
# isort: on
