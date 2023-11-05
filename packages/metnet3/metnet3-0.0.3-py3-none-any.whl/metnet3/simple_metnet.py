import torch 
from torch import nn
from typing import Tuple
import torch.nn.functional as f
from zeta.nn.modules import Unet
from metnet3.maxvit import MaxViT

class SimpleNetNet(nn.Module):
    def __init__(
        self,
        dim: int,
        dim_head: int ,
        depth: Tuple[int] = (2, 2, 2, 2),
        channels: int = None,
        classes: int = None,
        dropout: float = 0.1,
        **kwargs
    ):
        super(SimpleNetNet, self).__init__()
        self.unet = Unet(
            n_channels=channels,
            n_classes=classes,
            **kwargs
        )

        self.maxvit = MaxViT(
            num_classes=classes,
            dim=dim,
            dim_head=dim_head,
            depth=depth,
            dropout=dropout,
            **kwargs
        )
    
    def forward(
        self,
        high_res_inputs,
        low_res_inputs,
    ):
        featuress_unet = self.unet(high_res_inputs)

        features_vit = self.maxvit(featuress_unet)

        return features_vit
    

x = torch.randn(1, 793, 624, 624)
y = torch.randn(1, 64, 1248, 1248)

model = SimpleNetNet(
    dim=64,
    dim_head=64,
    depth=(2, 2, 2, 2),
    channels=857,
    classes=1,
    dropout=0.1,
    patch_size=16,
    image_size=624,
)

output = model(x, y)
print(output.shape)