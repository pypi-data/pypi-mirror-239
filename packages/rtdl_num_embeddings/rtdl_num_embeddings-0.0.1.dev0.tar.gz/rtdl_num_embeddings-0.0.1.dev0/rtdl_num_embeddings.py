"""On Embeddings for Numerical Features in Tabular Deep Learning."""

__version__ = '0.0.1.dev0'

__all__ = [
    'LinearEmbeddings',
    'SimpleEmbeddings',
    'PeriodicEmbeddings',
    'compute_bins',
    'PiecewiseLinearEmbeddings',
    'CompactPiecewiseLinearEmbeddings0d',
]

import math
import warnings
from typing import Any, Dict, List, Optional

import sklearn.tree
import torch
import torch.nn as nn
from torch import Tensor
from torch.nn.parameter import Parameter

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


# _NLinear is a simplified copy of delu.nn.NLinear, see the full documentation here:
# https://yura52.github.io/delu/stable/api/generated/delu.nn.NLinear.html
# In this package,
# _NLinear is used to train a *separate* linear layer for every feature embedding.
class _NLinear(nn.Module):
    """N *separate* linear layers for N feature embeddings."""

    def __init__(self, n: int, in_features: int, out_features: int) -> None:
        super().__init__()
        self.weight = Parameter(torch.empty(n, in_features, out_features))
        self.bias = Parameter(torch.empty(n, out_features))
        self.reset_parameters()

    def reset_parameters(self):
        d_in_rsqrt = self.weight.shape[-2] ** -0.5
        nn.init.uniform_(self.weight, -d_in_rsqrt, d_in_rsqrt)
        nn.init.uniform_(self.bias, -d_in_rsqrt, d_in_rsqrt)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        assert x.ndim == 3
        assert x.shape[-(self.weight.ndim - 1) :] == self.weight.shape[:-1]
        x = (x[..., None, :] @ self.weight).squeeze(-2)
        x = x + self.bias
        return x


class LinearEmbeddings(nn.Module):
    """Linear embeddings for continuous features.

    In particular, this module is used by the vanilla FT-Transformer.

    **Shape**

    - Input: `(*, n_features)`
    - Output: `(*, n_features, d_embedding)`

    **Examples**

    >>> batch_size = 2
    >>> n_cont_features = 3
    >>> x = torch.randn(batch_size, n_cont_features)
    >>> d_embedding = 4
    >>> m = LinearEmbeddings(n_cont_features, d_embedding)
    >>> m(x).shape
    torch.Size([2, 3, 4])
    """

    def __init__(self, n_features: int, d_embedding: int) -> None:
        """
        Args:
            n_features: the number of continous features.
            d_embedding: the embedding size.
        """
        if n_features <= 0:
            raise ValueError(f'n_features must be positive, however: {n_features=}')
        if d_embedding <= 0:
            raise ValueError(f'd_embedding must be positive, however: {d_embedding=}')

        super().__init__()
        self.weight = Parameter(torch.empty(n_features, d_embedding))
        self.bias = Parameter(torch.empty(n_features, d_embedding))
        self.reset_parameters()

    def reset_parameters(self) -> None:
        """Reinitialize all parameters."""
        d_rqsrt = self.weight.shape[1] ** -0.5
        nn.init.uniform_(self.weight, -d_rqsrt, d_rqsrt)
        if self.bias is not None:
            nn.init.uniform_(self.bias, -d_rqsrt, d_rqsrt)

    @property
    def d_embedding(self) -> int:
        """The embedding size."""
        return self.weight.shape[1]

    def forward(self, x: Tensor) -> Tensor:
        """Do the forward pass."""
        if x.ndim < 2:
            raise ValueError(
                f'The input must have at least two dimensions, however: {x.ndim=}'
            )

        x = x[..., None] * self.weight
        x = x + self.bias[None]
        return x


class SimpleEmbeddings(nn.Module):
    """LR (Linear-ReLU) & LRL (Linear-ReLU-Linear) embeddings for continuous features.

    **Shape**

    - Input: `(*, n_features)`
    - Output: `(*, n_features, d_embedding)`

    **Examples**

    >>> batch_size = 2
    >>> n_cont_features = 3
    >>> x = torch.randn(batch_size, n_cont_features)
    >>>
    >>> # LRL embeddings (by default, d_embedding=8)
    >>> m = SimpleEmbeddings(n_cont_features)
    >>> m(x).shape
    torch.Size([2, 3, 8])
    >>>
    >>> # LR embeddings
    >>> m = SimpleEmbeddings(n_cont_features, d_hidden=None)
    >>> m(x).shape
    torch.Size([2, 3, 8])
    """

    def __init__(
        self, n_features: int, d_embedding: int = 8, *, d_hidden: Optional[int] = 48
    ):
        """
        Args:
            n_features: the number of features.
            d_embedding: the embedding size.
            d_hidden: the hidden dimension. If an integer, the embedding architecture
                becomes Linear-Activation-Linear. Otherwise, it is Linear-Activation.
                In both cases, the output size of the last linear layer is d_embedding.
        """
        super().__init__()
        self.first = LinearEmbeddings(
            n_features, d_embedding if d_hidden is None else d_hidden
        )
        self.activation = nn.ReLU()
        # NOTE: DIFF
        # Technically, in the paper, the variation "LRL"
        # (which occurs when d_hidden is not None) is not covered.
        # However, it obviously belongs to the same "Simple embeddings" group
        # as L, LR and LRLR covered in the paper.
        self.second = (
            None if d_hidden is None else _NLinear(n_features, d_hidden, d_embedding)
        )

    def reset_parameters(self) -> None:
        """Reset all parameters."""
        self.first.reset_parameters()
        if self.second is not None:
            self.second.reset_parameters()

    @property
    def d_embedding(self) -> int:
        """The embedding size."""
        return (
            self.first.d_embedding
            if self.second is None
            else self.second.weight.shape[-1]
        )

    def forward(self, x: Tensor) -> Tensor:
        """Do the forward pass."""
        if x.ndim < 2:
            raise ValueError(
                f'The input must have at least two dimensions, however: {x.ndim=}'
            )

        x = self.first(x)
        x = self.activation(x)
        if self.second is not None:
            x = self.second(x)
        return x


class _Periodic(nn.Module):
    """
    WARNING: the direct usage of this module is discouraged
    (do this only if you understand why this warning is here).
    """

    def __init__(self, n_features: int, k: int, sigma: float) -> None:
        if sigma <= 0.0:
            raise ValueError(f'sigma must be positive, however: {sigma=}')

        super().__init__()
        self._sigma = sigma
        self.weight = Parameter(torch.empty(n_features, k))
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.normal_(self.weight, 0.0, self._sigma)

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim < 2:
            raise ValueError(
                f'The input must have at least two dimensions, however: {x.ndim=}'
            )

        x = 2 * math.pi * self.weight * x[..., None]
        x = torch.cat([torch.cos(x), torch.sin(x)], -1)
        return x


class PeriodicEmbeddings(nn.Module):
    """Periodic embeddings (PL & PLR & PLR(lite)) for continuous features.

    **Shape**

    - Input: `(*, n_features)`
    - Output: `(*, n_features, d_embedding)`

    **Examples**

    >>> batch_size = 2
    >>> n_cont_features = 3
    >>> x = torch.randn(batch_size, n_cont_features)
    >>>
    >>> # PL embeddings (by default, d_embedding=8)
    >>> m = PeriodicEmbeddings(n_cont_features)
    >>> m(x).shape
    torch.Size([2, 3, 8])
    >>>
    >>> # PLR embeddings
    >>> m = PeriodicEmbeddings(n_cont_features, 32, activation=True)
    >>> m(x).shape
    torch.Size([2, 3, 32])
    >>>
    >>> # PLR(lite) embeddings
    >>> m = PeriodicEmbeddings(n_cont_features, 40, activation=True, lite=True)
    >>> m(x).shape
    torch.Size([2, 3, 40])
    """

    def __init__(
        self,
        n_features: int,
        d_embedding: int = 8,
        *,
        k: int = 48,
        sigma: float = 0.01,
        activation: bool = False,
        lite: bool = False,
    ) -> None:
        """
        Args:
            n_features: the number of features.
            d_embedding: the embedding size.
            k: the number of "frequencies" (see Section 3.3 in the paper).
            sigma: the initialization scale for the "frequencies"
                (see Section 3.3 in the paper). **This is an important hyperparameter**,
                see the documentation for details.
            activation: if False, the embeddings is PL, otherwise, it is PLR.
            lite: if True, the linear layer (L) is shared between all features.
        """
        super().__init__()
        self.periodic = _Periodic(n_features, k, sigma)
        if lite:
            # NOTE: DIFF
            # The PLR(lite) variation was not covered in this paper about embeddings,
            # but it was used in the paper about the TabR model.
            if not activation:
                raise ValueError('lite=True is allowed only when activation=True')
            self.linear = _NLinear(n_features, 2 * k, d_embedding)
        else:
            self.linear = nn.Linear(2 * k, d_embedding)
        self.activation = nn.ReLU() if activation else None

    def forward(self, x: Tensor) -> Tensor:
        """Do the forward pass."""
        if x.ndim < 2:
            raise ValueError(
                f'The input must have at least two dimensions, however: {x.ndim=}'
            )

        x = self.periodic(x)
        x = self.linear(x)
        if self.activation is not None:
            x = self.activation(x)
        return x


def _check_bins(bins: List[Tensor]) -> None:
    if not bins:
        raise ValueError('The list of bins must not be empty')
    for i, feature_bins in enumerate(bins):
        if not isinstance(feature_bins, Tensor):
            raise ValueError(
                'bins must be a list of PyTorch tensors. '
                f'However, for {i=}: {type(bins[i])=}'
            )
        if feature_bins.ndim != 1:
            raise ValueError(
                'Each item of the bin list must have exactly one dimension.'
                f' However, for {i=}: {bins[i].ndim=}'
            )
        if len(feature_bins) < 2:
            raise ValueError(
                'All features must have at least two bin edges.'
                f' However, for {i=}: {len(bins[i])=}'
            )
        if not feature_bins.isfinite().all():
            raise ValueError(
                'Bin edges must not contain nan/inf/-inf.'
                f' However, this is not true for the {i}-th feature'
            )
        if (feature_bins[:-1] >= feature_bins[1:]).any():
            raise ValueError(
                'Bin edges must be sorted.'
                f' However, the for the {i}-th feature, the bin edges are not sorted'
            )
        if len(feature_bins) == 2:
            warnings.warn(
                f'The {i}-th feature has just two bin edges, which means only one bin.'
                ' Strictly speaking, using a single bin for the'
                ' piecewise-linear encoding should not break anything,'
                ' but it is the same as using sklearn.preprocessing.MinMaxScaler'
            )


def compute_bins(
    X: torch.Tensor,
    n_bins: int = 48,
    *,
    tree_kwargs: Optional[Dict[str, Any]] = None,
    y: Optional[Tensor] = None,
    regression: Optional[bool] = None,
    verbose: bool = False,
) -> List[Tensor]:
    """Compute bin edges for `PiecewiseLinearEmbeddings`.

    **Usage**

    Computing the quantile-based bins (Section 3.2.1 in the paper):

    >>> X_train = torch.randn(10000, 2)
    >>> bins = compute_bins(X_train)

    Computing the tree-based bins (Section 3.2.2 in the paper):

    >>> X_train = torch.randn(10000, 2)
    >>> y_train = torch.randn(len(X_train))
    >>> bins = compute_bins(
    ...     X_train,
    ...     y=y_train,
    ...     regression=True,
    ...     tree_kwargs={'min_samples_leaf': 64, 'min_impurity_decrease': 1e-4},
    ... )

    Args:
        X: the training features.
        n_bins: the number of bins.
        tree_kwargs: keyword arguments for `sklearn.tree.DecisionTreeRegressor`
            (if ``regression`` is `True`) or `sklearn.tree.DecisionTreeClassifier`
            (if ``regression`` is `False`).
        y: the training labels (must be provided if ``tree`` is not None).
        regression: whether the labels are regression labels
            (must be provided if ``tree`` is not None).
        verbose: if True and ``tree_kwargs`` is not None, than ``tqdm``
            (must be installed) will report the progress while fitting trees.
    Returns:
        A list of bin edges for all features. For one feature:

        - the maximum possible number of bin edges is ``n_bins + 1``.
        - the minumum possible number of bin edges is ``1``.
    """
    if not isinstance(X, Tensor):
        raise ValueError(f'X must be a PyTorch tensor, however: {type(X)=}')
    if X.ndim != 2:
        raise ValueError(f'X must have exactly two dimensions, however: {X.ndim=}')
    if X.shape[0] < 2:
        raise ValueError(f'X must have at least two rows, however: {X.shape[0]=}')
    if X.shape[1] < 1:
        raise ValueError(f'X must have at least one column, however: {X.shape[1]=}')
    if not X.isfinite().all():
        raise ValueError('X must not contain nan/inf/-inf.')
    if (X == X[0]).all(dim=0).any():
        raise ValueError(
            'All columns of X must have at least two distinct values.'
            ' However, X contains columns with just one distinct value.'
        )
    if n_bins <= 1 or n_bins >= len(X):
        raise ValueError(
            'n_bins must be more than 1, but less than len(X), however:'
            f' {n_bins=}, {len(X)=}'
        )

    if tree_kwargs is None:
        if y is not None or regression is not None or verbose:
            raise ValueError(
                'If tree_kwargs is None, then y must be None, regression must be None'
                ' and verbose must be False'
            )

        # NOTE: DIFF
        # The original implementation in the official paper repository has an
        # unintentional divergence from what is written in the paper.
        # This package implements the algorithm described in the paper,
        # and it is recommended for future work
        # (this may affect the optimal number of bins
        #  reported in the official repository).
        #
        # Additional notes:
        # - this is the line where the divergence happens:
        #   (the thing is that limiting the number of quantiles by the number of
        #   distinct values is NOT the same as removing identical quantiles
        #   after computing them)
        #   https://github.com/yandex-research/tabular-dl-num-embeddings/blob/c1d9eb63c0685b51d7e1bc081cdce6ffdb8886a8/bin/train4.py#L612C30-L612C30
        # - for the tree-based bins, there is NO such divergence;
        bins = [
            q.unique()
            for q in torch.quantile(
                X, torch.linspace(0.0, 1.0, n_bins + 1).to(X), dim=0
            ).T
        ]
        _check_bins(bins)
        return bins
    else:
        if y is None or regression is None:
            raise ValueError(
                'If tree_kwargs is not None, then y and regression must not be None'
            )
        if y.ndim != 1:
            raise ValueError(f'y must have exactly one dimension, however: {y.ndim=}')
        if len(y) != len(X):
            raise ValueError(
                f'len(y) must be equal to len(X), however: {len(y)=}, {len(X)=}'
            )
        if y is None or regression is None:
            raise ValueError(
                'If tree_kwargs is not None, then y and regression must not be None'
            )
        if 'max_leaf_nodes' in tree_kwargs:
            raise ValueError(
                'tree_kwargs must not contain the key "max_leaf_nodes"'
                ' (it will be set to n_bins automatically).'
            )

        if verbose:
            if tqdm is None:
                raise ImportError('If verbose is True, tqdm must be installed')
            tqdm_ = tqdm
        else:
            tqdm_ = lambda x: x  # noqa: E731

        if X.device.type != 'cpu' or y.device.type != 'cpu':
            raise UserWarning(
                'Computing tree-based bins involves the conversion of the input PyTorch'
                ' tensors to NumPy arrays. The provided PyTorch tensors are not'
                ' located on CPU, so the conversion has (perhaps, noticeable) overhead.'
            )
        X_numpy = X.cpu().numpy()
        y_numpy = y.cpu().numpy()
        bins = []
        for column in tqdm_(X_numpy.T):
            feature_bin_edges = [float(column.min()), float(column.max())]
            tree = (
                (
                    sklearn.tree.DecisionTreeRegressor
                    if regression
                    else sklearn.tree.DecisionTreeClassifier
                )(max_leaf_nodes=n_bins, **tree_kwargs)
                .fit(column.reshape(-1, 1), y_numpy)
                .tree_
            )
            for node_id in range(tree.node_count):
                # The following condition is True only for split nodes. Source:
                # https://scikit-learn.org/1.0/auto_examples/tree/plot_unveil_tree_structure.html#tree-structure
                if tree.children_left[node_id] != tree.children_right[node_id]:
                    feature_bin_edges.append(float(tree.threshold[node_id]))
            bins.append(torch.as_tensor(feature_bin_edges).unique())
        _check_bins(bins)
        return [x.to(device=X.device, dtype=X.dtype) for x in bins]


class PiecewiseLinearEmbeddings(nn.Module):
    """Piecewise-linear embeddings."""

    edges: Tensor
    width: Tensor
    mask: Tensor

    def __init__(
        self,
        bins: List[Tensor],
        d_embedding: int = 8,
        *,
        activation: bool = False,
    ) -> None:
        """
        Args:
            bins: the bins computed by `compute_bins`.
            d_embedding: the embedding size.
            activation: if False, the embedding becomes what is called "Q-L"/"T-L"
                in Table 2 in the paper (depending on how bins were computed).
                Otherwise, the embedding is "Q-LR"/"T-LR"
        """
        if d_embedding <= 0:
            raise ValueError(
                f'd_embedding must be a positive integer, however: {d_embedding=}'
            )
        _check_bins(bins)

        super().__init__()
        max_n_edges = max(len(x) for x in bins)
        padding = torch.full(
            (max_n_edges,),
            torch.finfo(bins[0].dtype).max,
            dtype=bins[0].dtype,
            device=bins[0].device,
        )
        edges = torch.row_stack([torch.cat([x, padding])[:max_n_edges] for x in bins])

        # The rightmost edge is needed only to compute the width of the rightmost bin.
        self.register_buffer('edges', edges[:, :-1])
        self.register_buffer('width', edges.diff())
        self.register_buffer(
            'mask',
            torch.row_stack(
                [
                    torch.cat(
                        [
                            torch.ones(len(x) - 1, dtype=torch.bool, device=x.device),
                            torch.zeros(
                                max_n_edges - 1, dtype=torch.bool, device=x.device
                            ),
                        ]
                    )[: max_n_edges - 1]
                    for x in bins
                ]
            ),
        )
        self.linear = _NLinear(len(bins), max_n_edges - 1, d_embedding)
        self.activation = nn.ReLU() if activation else None

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim < 2:
            raise ValueError(
                f'The input must have at least two dimensions, however: {x.ndim=}'
            )

        x = (x[..., None] - self.edges) / self.width
        n_bins = x.shape[-1]
        if n_bins > 1:
            x = torch.cat(
                [
                    x[..., :1].clamp_max(1.0),
                    *([] if n_bins == 2 else [x[..., 1:-1].clamp(0.0, 1.0)]),
                    x[..., -1:].clamp_min(0.0),
                ],
                dim=-1,
            )
        x = torch.where(self.mask, x, torch.tensor(0.0).to(x))
        x = self.linear(x)
        if self.activation is not None:
            x = self.activation(x)
        return x


class CompactPiecewiseLinearEmbeddings0d(nn.Module):
    """A memory-efficient version of `PiecewiseLinearEmbeddings`.

    Compared to `PiecewiseLinearEmbeddings`:
    - this module outputs a two dimensional tensor.
    - ``d_embedding=None`` is allowed. In that case, the raw piecewise linear encoding
      is performed which, for each feature, allocates the number of representation
      components equal to the number of bins for this feature.

    The arguments are the same as for `PiecewiseLinearEmbeddings`.

    **Shape**

    - Input: `(*, n_features)`
    - Output (``d_embedding is not None``):
      `(*, n_features * d_embedding)`
    - Output (``d_embedding is     None``):
      `(*, <the total number of bins of all features>)`
    """

    edges: Tensor
    width: Tensor

    def __init__(
        self,
        bins: List[Tensor],
        d_embedding: Optional[int] = 8,
        *,
        activation: bool = False,
    ) -> None:
        if d_embedding is None:
            if activation:
                raise ValueError(
                    'activation can be True only if d_embedding is not None.'
                )
        else:
            if d_embedding <= 0:
                raise ValueError(
                    'd_embedding must be either None or a positive integer,'
                    f' however: {d_embedding=}'
                )
        _check_bins(bins)

        super().__init__()
        # The rightmost edge is needed only to compute the width of the rightmost bin.
        self.register_buffer('edges', torch.cat([x[:-1] for x in bins]))
        self.register_buffer('width', torch.cat([x.diff() for x in bins]))
        self.bin_counts = tuple(len(x) - 1 for x in bins)
        self.linear = (
            None
            if d_embedding is None
            else nn.ModuleList([nn.Linear(x, d_embedding) for x in self.bin_counts])
        )
        self.activation = nn.ReLU() if activation else None

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim != 2:
            raise ValueError(
                f'The input must have exactly two dimensions, however: {x.ndim=}'
            )

        edges: list[Tensor] = self.edges.split(self.bin_counts)
        width: list[Tensor] = self.width.split(self.bin_counts)
        h = []
        for i in range(x.shape[1]):
            hi = (x[:, i : i + 1] - edges[i]) / width[i]
            h.append(
                hi
                if self.bin_counts[i] == 1
                else torch.column_stack(
                    [
                        hi[:, 0].clamp_max(1.0),
                        *(
                            []
                            if self.bin_counts[i] == 2
                            else [hi[:, 1:-1].clamp(0.0, 1.0)]
                        ),
                        hi[:, -1].clamp_min(0.0),
                    ]
                )
            )
        if self.linear is not None:
            h = [mi(hi) for mi, hi in zip(self.linear, h)]
        h = torch.column_stack(h)
        if self.activation is not None:
            h = self.activation(h)
        return h
