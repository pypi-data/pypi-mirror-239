# RTDL (Research on Tabular Deep Learning)

RTDL is a PyTorch-based package providing **implementations and usage examples of deep
learning models for tabular data** from some of the papers listed below.
Notes:
- Implementations in RTDL are approved by authors of the papers.
- The following things are out of scope for RTDL:
    - Providing basic building blocks and utilities for tabular deep learning.
    - Describing general best practices for tabular deep learning.
    - etc.

*To follow announcements on new papers and releases,
subscribe to releases in the GitHub interface: "Watch -> Custom -> Releases".
Feel free to open issues
for any kind of feedback and discussions.*

# Papers

| Name                                                                   | Year  | Paper                                     | Code                                                                        | Submodule                |
| :--------------------------------------------------------------------- | :---: | :---------------------------------------- | :-------------------------------------------------------------------------- | :----------------------- |
| TabR: Unlocking the Power of Retrieval-Augmented Tabular Deep Learning | 2023  | [arXiv](https://arxiv.org/abs/2307.14338) | [GitHub](https://github.com/yandex-research/tabular-dl-tabr)                | -                        |
| TabDDPM: Modelling Tabular Data with Diffusion Models                  | 2022  | [arXiv](https://arxiv.org/abs/2209.15421) | [GitHub](https://github.com/yandex-research/tab-ddpm)                       | -                        |
| Revisiting Pretraining Objectives for Tabular Deep Learning            | 2022  | [arXiv](https://arxiv.org/abs/2207.03208) | [GitHub](https://github.com/yandex-research/tabular-dl-pretrain-objectives) | -                        |
| On Embeddings for Numerical Features in Tabular Deep Learning          | 2022  | [arXiv](https://arxiv.org/abs/2203.05556) | [GitHub](https://github.com/yandex-research/tabular-dl-num-embeddings)      | `rtdl.num_embeddings`    |
| Revisiting Deep Learning Models for Tabular Data                       | 2021  | [arXiv](https://arxiv.org/abs/2106.11959) | [GitHub](https://github.com/yandex-research/tabular-dl-revisiting-models)   | `rtdl.revisiting_models` |
| Neural Oblivious Decision Ensembles for Deep Learning on Tabular Data  | 2019  | [arXiv](https://arxiv.org/abs/1909.06312) | [GitHub](https://github.com/Qwicen/node)                                    | -                        |

# Documentation

> [!IMPORTANT]
> 
> <details>
> <summary>RTDL VS Original implementations</summary>
>
> - Implementations in `rtdl` are approved by authors of the papers,
>   so RTDL can be safely used in other papers.
> - So far, differences with original implementations are rare, minor and
>   marked with the comment `# NOTE: DIFF` in the source code of this package.
> - Any divergence from original implementations without the `# NOTE: DIFF` comment
>   is considered to be a bug.
>
> </details>

- [Installation](#installation)
- [Usage](#usage)
- [API](#api)

## Installation

```
pip install rtdl
```

## Usage

`rtdl` consists of independent submodules,
each of which has a separate documentation page.

> [!IMPORTANT]
> Each submodule has a "Practical notes" section with notes on hyperparameters
> and other pratical aspects.

- [`rtdl.revisiting_models`](./revisiting_models/README.md)
- [`rtdl.num_embeddings`](./num_embeddings/README.md)
- ⚠️ **Everything else is deprecated** and will be removed in future releases
  - <details>
    <summary>Show all deprecated items</summary>
      rtdl.data, rtdl.functional, rtdl.modules, rtdl.GEGLU, rtdl.MLP,
      rtdl.CategoricalFeatureTokenizer, rtdl.CLSToken, rtdl.FeatureTokenizer,
      rtdl.FTTransformer, rtdl.MultiheadAttention, rtdl.NumericalFeatureTokenizer,
      rtdl.ReGLU, rtdl.ResNet, rtdl.Transformer
    </details>

## API

To discover the formal API and docstrings of a submodule, open its source file and:
- on GitHub, use the Symbols panel
- in VSCode, use the [Outline view](https://code.visualstudio.com/docs/getstarted/userinterface#_outline-view)
- check the `__all__` variable

# Development

<details><summary>Show</summary>

Set up the environment (replace `micromamba` with `conda` or `mamba` if needed):
```
micromamba create -f environment.yaml
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
