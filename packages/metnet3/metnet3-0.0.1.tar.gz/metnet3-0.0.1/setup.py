# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metnet3']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'metnet3',
    'version': '0.0.1',
    'description': 'Metnet - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Metnet3\n\n\n# Install\n`pip install metnet3`\n\n\n## Usage\n```\n\n\n```\n\n\n# MetNet-3 Model Architecture README.md\n\n## 4.2 Model and Architecture Overview\n\nMetNet-3 is a neural network designed to process and predict spatial weather patterns with high precision. This sophisticated model incorporates a fusion of cutting-edge techniques including topographical embeddings, a U-Net backbone, and a modified MaxVit transformer to capture long-range dependencies. With a total of 227 million trainable parameters, MetNet-3 is at the forefront of meteorological modeling.\n\n### 4.2.1 Topographical Embeddings\n\nLeveraging a grid of trainable embeddings, MetNet-3 can automatically learn and utilize topographical features relevant to weather forecasting. Each grid point, spaced with a stride of 4 km, is associated with 20 parameters. These embeddings are then bilinearly interpolated for each input pixel, enabling the network to effectively encode the underlying geography for each data point.\n\n### 4.2.2 Network Architecture\n\nMetNet-3's architecture is complex, ingesting both high-resolution (2496 km² at 4 km resolution) and low-resolution (4992 km² at 8 km resolution) spatial inputs. The model processes these inputs through a series of layers and operations, as depicted in the following ASCII flow diagram:\n\n```\nInput Data\n   │\n   │ High-resolution inputs\n   │ concatenated with current time\n   │ (624x624x793)\n   │\n   ▼\n [Embed Topographical Embeddings]\n   │\n   ├─►[2x ResNet Blocks]───►[Downsampling to 8 km]\n   │                            │\n   │                            ├─►[Pad to 4992 km²]───►[Concatenate Low-res Inputs]\n   │                            │\n   ▼                            ▼\n [U-Net Backbone]            [2x ResNet Blocks]\n   │                            │\n   ├─►[Downsampling to 16 km]   │\n   │                            │\n   ▼                            │\n [Modified MaxVit Blocks]◄──────┘\n   │\n   │\n [Central Crop to 768 km²]\n   │\n   ├─►[Upsampling Path with Skip Connections]\n   │\n   │\n [Central Crop to 512 km²]\n   │\n   ├─►[MLP for Weather State Channels at 4 km resolution]\n   │\n   ├─►[Upsampling to 1 km for Precipitation Targets]\n   │\n   ▼\n[Output Predictions]\n```\n\n#### Dense and Sparse Inputs\n\nThe model uniquely processes both dense and sparse inputs, integrating temporal information such as the time of prediction and the forecast lead time.\n\n#### Target Outputs\n\nMetNet-3 produces both categorical and deterministic predictions for various weather-related variables, including precipitation and surface conditions, using a combination of loss functions tailored to the nature of each target.\n\n#### ResNet Blocks and MaxVit\n\nCentral to the network's ability to capture complex patterns are the ResNet blocks, which handle local interactions, and the MaxVit blocks, which facilitate global comprehension of the input data through attention mechanisms.\n\n## Technical Specifications\n\n- **Input Spatial Resolutions**: 4 km and 8 km\n- **Output Resolutions**: From 1 km to 4 km depending on the variable\n- **Embedding Stride**: 4 km\n- **Topographical Embedding Parameters**: 20 per grid point\n- **Network Parameters**: 227 million\n- **Input Channels**: Various, including 617+1 channels from HRRR assimilation\n- **Output Variables**: 6+617 for surface and assimilated state variables, respectively\n- **Model Backbone**: U-Net with MaxVit transformer\n- **Upsampling and Downsampling**: Implemented within the network to transition between different resolutions\n\n## Low-Level Details and Optimization\n\nFurther technical details on architecture intricacies, optimization strategies, and hyperparameter selections are disclosed in Supplement B, providing an in-depth understanding of the model's operational framework.\n\nThis README intends to serve as a technical overview for researchers and engineers looking to grasp the functional composition and capabilities of MetNet-3. For implementation and collaboration inquiries, the supplementary materials should be referred to for comprehensive insights.\n\n\n# License\nMIT\n\n\n\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/metnet3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
