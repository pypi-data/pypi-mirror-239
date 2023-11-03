# Python package <!-- omit in toc -->

TODO

---

- [Installation](#installation)
- [Usage](#usage)
- [End-to-end examples](#end-to-end-examples)
- [Practical notes](#practical-notes)
- [API](#api)
- [Development](#development)

# Installation

*(RTDL ~ Research on Tabular Deep Learning)*

```
pip install rtdl_num_embeddings
```

# Usage

> [!IMPORTANT]
> It is recommended to first read the TL;DR of the paper:
> [link](../README.md#tldr)

Let's consider a toy tabular data problem where objects are represented by three
continuous features
(for simplicity, other feature types are omitted,
but they are covered in the end-to-end example):

<!-- test main -->
```python
# NOTE: all code snippets can be copied and executed as-is.
import torch
import torch.nn as nn
# pip install rtdl_revisiting_models
from rtdl_revisiting_models import MLP
from rtdl_num_embeddings import (
    SimpleEmbeddings,
    PeriodicEmbeddings,
    PiecewiseLinearEmbeddings, compute_bins,
)

batch_size = 256
n_cont_features = 3
x = torch.randn(batch_size, n_cont_features)
```

This is how a vanilla MLP **without embeddings** would look like:

<!-- test main -->
```python
mlp_config = {
    'd_out': 1,  # For example, a single regression task.
    'n_blocks': 2,
    'd_block': 256,
    'dropout': 0.1,
}
model = MLP(d_in=n_cont_features, **mlp_config)
y_pred = model(x)
```

And this is how MLP **with embeddings for continuous features** can be created:

<!-- test main -->
```python
d_embedding = 8
m_cont_embeddings = PeriodicEmbeddings(n_cont_features, d_embedding)
model_with_embeddings = nn.Sequential(
    # Input shape: (batch_size, n_cont_features)

    m_cont_embeddings,
    # After embeddings: (batch_size, n_cont_features, d_embedding)

    # NOTE: `nn.Flatten` is not needed for Transformer-like architectures.
    nn.Flatten(),
    # After flattening: (batch_size, n_cont_features * d_embedding)

    MLP(d_in=n_cont_features * d_embedding, **mlp_config)
    # The final shape: (batch_size, d_out)
)
# The usage is the same as for the simple model:
y_pred = model_with_embeddings(x)
```

In other words, the whole paper is about the fact that having such a thing as
`m_cont_embeddings` can (significantly) improve the downstream performance,
and the paper showcases three types of such embeddings:
simple, periodic and piecewise-linear.

## Simple embeddings<!-- omit in toc -->

*(Decribed in Section 3.4 in the paper)*

| Name            | Definition for a single feature | How to create                          |
| :-------------- | :------------------------------ | :------------------------------------- |
| `L`             | `Linear(x_i)`                   | `LinearEmbeddings(...)`                |
| `LR`            | `ReLU(Linear(x_i))`             | `SimpleEmbeddings(..., d_hidden=None)` |
| `LRL` (default) | `Linear(ReLU(Linear(x_i)))`     | `SimpleEmbeddings(...)`                |

In the above table:
- `x_i` is the i-th scalar continuous feature

> [!NOTE]
> Hyperparameters are commented in ["Practical notes"](#practical-notes).

<!-- test main _ -->
```python
# MLP-LRL
model = nn.Sequential(
    SimpleEmbeddings(n_cont_features, d_embedding),
    nn.Flatten(),
    MLP(d_in=n_cont_features * d_embedding, **mlp_config)
)
y_pred = model(x)
```

## Periodic embeddings<!-- omit in toc -->

*(Decribed in Section 3.3 in the paper)*

| Name           | Definition for a single feature     | How to create                                         |
| :------------- | :---------------------------------- | :---------------------------------------------------- |
| `PL` (default) | `Linear(Periodic(x_i))`             | `PeriodicEmbeddings(...)`                             |
| `PLR`          | `ReLU(Linear(Periodic(x_i)))`       | `PeriodicEmbeddings(..., activation=True)`            |
| `PLR(lite)`    | `ReLU(SharedLinear(Periodic(x_i)))` | `PeriodicEmbeddings(..., activation=True, lite=True)` |

In the above table:
- `x_i` is the i-th scalar continuous feature
- `Periodic(x_i) = concat[cos(h_i), sin(h_i)]`, where:
  - `h_i = 2 * pi * Linear(x_i, bias=False)`
  - `h_i.shape == (k,)` (`k` is a hyperparameter)
- `lite` is a new option introduced in
  [TabR](https://github.com/yandex-research/tabular-dl-tabr/).
  It makes the `PLR` embedding significantly more lightweight
  at the cost of (on average) non-critical performance loss.

> [!IMPORTANT]
> <details><summary><b>How to tune the <code>sigma</code> hyperparameter</b></summary>
> 
> **Prioritize testing smaller values, because they are safer:**
> - Larger-than-the-optimal value can lead to terrible performance.
> - Smaller-than-the-optimal value will still yield decent performance.
>
> Some approximate numbers:
> - for 30% of tasks, the optimal `sigma` is less than 0.05.
> - for 50% of tasks, the optimal `sigma` is less than 0.2.
> - for 80% of tasks, the optimal `sigma` is less than 1.0.
> - for 90% of tasks, the optimal `sigma` is less than 5.0.
> - that said, on some problems, larger values can improve performance, but
>   make sure that you have enough tuning budget for testing them (e.g. at least
>   100 trials of the TPE sampler, as in the paper).
>
> </details>

> [!NOTE]
> Other hyperparameters are commented in ["Practical notes"](#practical-notes).

<!-- test main _ -->
```python
# Example: MLP-PL
model = nn.Sequential(
    PeriodicEmbeddings(n_cont_features, d_embedding),
    nn.Flatten(),
    MLP(d_in=n_cont_features * d_embedding, **mlp_config)
)
y_pred = model(x)
```

## Piecewise-linear embeddings<!-- omit in toc -->

*(Decribed in Section 3.2 in the paper)*

<img src="piecewise-linear-encoding.png" width=40%>

| Name                | Definition for a single feature | How to create                                                |
| :------------------ | :------------------------------ | :----------------------------------------------------------- |
| `Q`/`T`             | `ple(x_i)`                      | `CompactPiecewiseLinearEmbeddings0d(bins, d_embedding=None)` |
| `QL`/`TL` (default) | `Linear(ple(x_i))`              | `PiecewiseLinearEmbeddings(bins)`                            |
| `QLR` / `TLR`       | `ReLU(Linear(ple(x_i)))`        | `PiecewiseLinearEmbeddings(bins, activation=True)`           |

In the above table:
- `x_i` is the i-th scalar continuous feature
- `Q`/`T` means that `bins` are computed based on quantiles/decision trees.
- `ple` stands for "Piecewise-linear encoding".

> [!NOTE]
> Hyperparameters are commented in ["Practical notes"](#practical-notes).

<!-- test main _ -->
```python
X_train = torch.randn(10000, n_cont_features)
Y_train = torch.randn(len(X_train))  # Regression.

# (Q) Quantile-based bins.
bins = compute_bins(X_train)
# (T) Target-aware (tree-based) bins.
bins = compute_bins(
    X_train,
    tree_kwargs={'min_samples_leaf': 64, 'min_impurity_decrease': 1e-4},
    y=Y_train,
    regression=True,
)

# MLP-QL / MLP-TL
model = nn.Sequential(
    PiecewiseLinearEmbeddings(bins, d_embedding),
    nn.Flatten(),
    MLP(d_in=n_cont_features * d_embedding, **mlp_config)
)
y_pred = model(x)
```

# End-to-end examples

See [this Jupyter notebook](./example.ipynb).

# Practical notes

**General comments**

- **Embeddings for continuous features are applicable to most tabular DL models**
  and often lead to better task performance.
  On some problems, embeddings can lead to truly significant improvements.
- **MLP with embeddings is a good modern baseline**
  in terms of both task performance and efficiency.
  Depending on the task and embeddings, it can perform on par or even better than
  FT-Transformer, while being significantly more efficient.
- Despite the formal overhead in terms of parameter count,
  **embeddings are perfectly affordable in many cases**.
  On big enough datasets and/or with large enough number of features and/or
  with strict enough latency requirements,
  the new overhead associated with embeddings may become an issue.

**What embeddings to choose?**

*(the below list assumes MLP as the backbone)*

- `SimpleEmbeddings` falls into the "low risk & low reward" category.
  It makes it a good choice for a quick start on a new problem, especially if 
  this is your first time working with embeddings.
- `PeriodicEmbeddings` demonstrates the best performance on average,
  so it is the next reasonable step. **Please, read the notes on hyperparameters**
  in the [corresponding usage section](#periodic-embeddings) and in the
  "Hyperparameters" section below.
- `PiecewiseLinearEmbeddings` can produce good results on some datasets,
  but in the paper, it performed worse than `PeriodicEmbeddings` on average.
  Usually, it is the last thing to try.

**Hyperparameters**

- The default hyperparameters are set with the MLP-like backbones in mind and
  with "low risk" (not the "best results") as the priority.
  For Transformer-like models, one may want to (significantly) increase `d_embedding`.
- For MLP-like models, for embeddings ending with a linear layer `L`
  (e.g. `LRL`, `PL`, etc.)
  a safe default stratagy is to set `d_embedding` to a small value.
  The hidden dimension (`d_hidden` for `SimpleEmbeddings`, `k` for `PeriodicEmbeddings`,
  `n_bins` for `PiecewiseLinearEmbeddings`),
  in turn, usually can be safely set to a relatively large value.
- For MLP-like models, for embeddings ending with a ReLU-like activation
  (`LR`, `PLR`, etc.), `d_embedding` can need (significantly) larger values
  than the default one.
- Tuning periodic embeddings can require special considerations as described in
  the [corresponding usage section](#periodic-embeddings).
- In the paper, for hyperparameter tuning, the
  [TPE sampler from Optuna](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html)
  was used with `study.optimize(..., n_trials=100)` (sometimes, `n_trials=50`).
- The hyperparamer tuning spaces can be found in the appendix of the paper
  and in `exp/**/*tuning.toml` files in the repository reproducing the paper.
- :fire: Is is possible to explore the published tuned hyperparameter configurations for the
  datasets used in the paper as described [here](../README.md#how-to-explore-metrics-and-hyperparameters).

**Tips**

- To improve efficiency, it is possible to embed only a subset of features.
- The biggest wins come from embedding *important, but "problematic"* features
  (intuitively, it means features with irregular
  joint distributions with other (important) features and labels).
- The proposed embeddings are relevant only for continuous features,
  so they should not be used for embedding binary or categorical features.
- If an embedding ends with a linear layer (e.g. `PL`, `LRL`, etc.) and its output
  is passed to MLP, then that linear layer can be fused with the first linear layer of
  MLP after the training (sometimes, it can lead to better efficiency).

# API

See [this note](../README.md#api).

# Development

<details>

Set up the environment (replace `micromamba` with `conda` or `mamba` if needed):
```
micromamba create -f environment-package.yaml
```

Check out the available commands in the [Makefile](./Makefile).
In particular, use this command before committing:
```
make pre-commit
```

Publish the package to PyPI (requires PyPI account & configuration):
```
flit publish
```
</details>

