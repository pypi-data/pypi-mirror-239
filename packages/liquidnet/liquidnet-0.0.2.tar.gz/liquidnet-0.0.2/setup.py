# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liquidnet']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'liquidnet',
    'version': '0.0.2',
    'description': 'Liquid Net - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# LiquidNet\nThis is a simple implementation of the Liquid net official repo translated into pytorch for simplicity. [Find the original repo here:](https://github.com/raminmh/liquid_time_constant_networks)\n\n## Install\n`pip install liquid-net`\n\n## Usage\n```python\nimport torch\nfrom liquidnet.main import LiquidNet\n\n# Create an LiquidNet with a specified number of units\nnum_units = 64\nltc_cell = LiquidNet(num_units)\n\n# Generate random input data with batch size 4 and input size 32\nbatch_size = 4\ninput_size = 32\ninputs = torch.randn(batch_size, input_size)\n\n# Initialize the cell state (hidden state)\ninitial_state = torch.zeros(batch_size, num_units)\n\n# Forward pass through the LiquidNet\noutputs, final_state = ltc_cell(inputs, initial_state)\n\n# Print the shape of outputs and final_state\nprint("Outputs shape:", outputs.shape)\nprint("Final state shape:", final_state.shape)\n\n```\n\n\n# Citation\n```bibtex\n@article{DBLP:journals/corr/abs-2006-04439,\n  author       = {Ramin M. Hasani and\n                  Mathias Lechner and\n                  Alexander Amini and\n                  Daniela Rus and\n                  Radu Grosu},\n  title        = {Liquid Time-constant Networks},\n  journal      = {CoRR},\n  volume       = {abs/2006.04439},\n  year         = {2020},\n  url          = {https://arxiv.org/abs/2006.04439},\n  eprinttype    = {arXiv},\n  eprint       = {2006.04439},\n  timestamp    = {Fri, 12 Jun 2020 14:02:57 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2006-04439.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}\n\n```\n\n\n# License\nMIT\n\n\n# Todo:\n- [ ] Implement LiquidNet for vision and train on CIFAR\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/LiqudNet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
