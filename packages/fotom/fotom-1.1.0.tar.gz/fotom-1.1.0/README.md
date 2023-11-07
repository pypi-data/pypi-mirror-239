[![Publish Python 🐍 distribution 📦 to PyPI and TestPyPI](https://github.com/neutralpronoun/fotom/actions/workflows/pypi-publish.yml/badge.svg?branch=main)](https://github.com/neutralpronoun/fotom/actions/workflows/pypi-publish.yml)

# FoToM

A pip package for FoToM (**Fo**undational **To**pology **M**odels), pretrained models for graph deep learning.

![](https://raw.githubusercontent.com/neutralpronoun/fotom/main/fotom/assets/embedding-github.png)

FoToM is a model pre-trained with contrastive learning on node-label-free graphs, but we show that under fine-tuning on node-labelled data there is still a significant performance increase.

## Installation

Please don't rely just on the pip install to sort out all the requirements, `torch_scatter` doesn't play well with others.

You might need to manually pre-install:
 - `torch`
 - `torch_geometric`
 - `torch_scatter`

You would likely need these anyway and which versions you're using will (in most cases) not make a significant difference.

### Data Formats

 - Data can be passed to Embedder as `networkx` graphs or `pytorch_geometric.data.Data` objects
 - `pytorch_geometric.loader.DataLoader` loaders are also compatible for more advanced users
 - `networkx` graphs can have node or edge attributes, but only of `dim=1`, ie labels
 - If no node or edge labels are passed they are filled with `torch.ones(data.num_nodes)` or `torch.ones(data.num_edges)` tensors

### Embeddings

The simplest use case is to use our pre-trained model to produce vector graph embeddings.
In code this can be done through:

```python
import networkx as nx
from fotom.embedding import Embedder

# Get some dummy graph data
graphs = []
for _ in range(1000):
    graphs.append(nx.random_tree(12))

# Instatiate Embedder, this loads our pre-trained checkpoint
embedder = Embedder(device = "cpu", encoder = None)

# Using __call__ syntax:
embedding = embedder(graphs)

# Using .transform:
embedding = embedder.transform(graphs)
```

The returned embeddings are of shape `(N_samples, output_dim)`.

The embedder only has two init arguments:
 - `device`: the device to use, probably "gpu" or "cpu", default "cpu"
 - 'encoder': a different encoder - see below



### Models

A model with (untrained) linear output layers, for transfer learning, is available through:

```python
from fotom.model import load_transfer_model

model = load_transfer_model(linear_layers=(300,), output_dim=1)
```

The model here, loaded with pre-trained weights through `load_transfer_model`, has two keyword arguments:
 - `linear_layers`: a tuple of the number of neurons in each layer following the encoder
 - `output_dim`: the number of neurons in the final output layer

### Similarity Metrics

Along the same lines as Frechet Inception Distance, we also package the Wasserstein Fotom Distance (WFD):

```python
from fotom.metrics import WFD

graphs_tree = []
for _ in range(1000):
    graphs_tree.append(nx.random_tree(24))

graphs_er = []
for _ in range(1000):
    graphs_er.append(nx.erdos_renyi_graph(24, 0.1))

print(f"WFD two trees: {WFD(graphs_tree, graphs_tree)}")
print(f"WFD dense ER/trees: {WFD(graphs_er, graphs_tree)}")
```

```bash
WFD two trees: 0.0
WFD sparse ER/trees: 7.840556418140956
```

`WFD` takes 2 positional and 3 keyword arguments:

 - `graphs_1` : A dataset of graphs, in the same forms as passed to `Embedder`
 - `graphs_2` : See above
 - `embedder = None` : The embedder to use. If `None`, loads the default pre-trained `FoToM` model
 - `fix_seeds = True` : Whether to re-fix seeds between each inference. Results are more consistent with a fixed seed.
 - `seed = 42` : The seed to set. Ignored if `fix_seeds = False`

### Advanced Usage

FoToM essentially comes down to two classes:

`fotom.model.Encoder`, the encoder without pre-trained weights, taking arguments:
- `emb_dim=300`: the dimension of the encodings
- `num_gc_layers=5`: the number of layers in the encoder architecture
- `drop_ratio=0.0`: the drop ratio during training
- `pooling_type="standard"`: 'standard' or 'layerwise', how pooling happens between nodes before output

These parameters are set through a config file when using `load_encoder`

`fotom.model.TransferModel`, a wrapper for `fotom.model.Encoder` with additional linear layers after the encoder.
This takes the following arguments:
- `encoder`: (probably) an `fotom.model.Encoder` instance
- `linear_layers=(300,)`: the dimensions of each (non-output) linear layer following the encoder
- `output_dim=300`: the dimensions of the final output

## Credits


FoToM is a work by Alex Davies, Riku Green, Nirav Ajmeri and Telmo de Menezes e Silva Filho, all academics at the University of Bristol.

FoToM is an extension of the AD-GCL work by Suresh et. al., <https://arxiv.org/abs/2106.05819>.

If you use FoToM in your work, please give due credit to both sets of authors in any resulting publication.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
