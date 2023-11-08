<img src="./metnet3.png" width="450px"></img>

## MetNet-3 - Pytorch (wip)

Implementation of <a href="https://blog.research.google/2023/11/metnet-3-state-of-art-neural-weather.html">MetNet 3</a>, SOTA neural weather model out of Google Deepmind, in Pytorch

The model architecture is pretty unremarkable. It is basically a U-net with a specific <a href="https://arxiv.org/abs/2204.01697">well performing vision transformer</a>. The most interesting thing about the paper may end up being the loss scaling in section 4.3.2


## Install

```bash
$ pip install metnet3-pytorch
```

## Usage

```python
import torch
from metnet3_pytorch.metnet3_pytorch import MetNet3

metnet3 = MetNet3(
    dim = 512,
    num_lead_times = 722,
    lead_time_embed_dim = 32,
    input_spatial_size = 624,
    attn_dim_head = 8,
    sparse_input_2496_channels = 8,
    dense_input_2496_channels = 8,
    dense_input_4996_channels = 8,
    surface_target_channels = 4,
    hrrr_target_channels = 4,
    precipitation_target_channels = 4
)

lead_times = torch.randint(0, 722, (2,))
sparse_input_2496 = torch.randn((2, 8, 624, 624))
dense_input_2496 = torch.randn((2, 8, 624, 624))
dense_input_4996 = torch.randn((2, 8, 624, 624))

surface_target, hrrr_target, precipitation_target = metnet3(
    lead_times = lead_times,
    sparse_input_2496 = sparse_input_2496,
    dense_input_2496 = dense_input_2496,
    dense_input_4996 = dense_input_4996
)
```

## Citations

```bibtex
@article{Andrychowicz2023DeepLF,
    title   = {Deep Learning for Day Forecasts from Sparse Observations},
    author  = {Marcin Andrychowicz and Lasse Espeholt and Di Li and Samier Merchant and Alexander Merose and Fred Zyda and Shreya Agrawal and Nal Kalchbrenner},
    journal = {ArXiv},
    year    = {2023},
    volume  = {abs/2306.06079},
    url     = {https://api.semanticscholar.org/CorpusID:259129311}
}
```
