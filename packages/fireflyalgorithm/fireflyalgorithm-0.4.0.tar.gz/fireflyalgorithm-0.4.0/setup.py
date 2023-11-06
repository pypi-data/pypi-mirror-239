# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fireflyalgorithm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.1,<2.0.0']

entry_points = \
{'console_scripts': ['firefly-algorithm = fireflyalgorithm.cli:main']}

setup_kwargs = {
    'name': 'fireflyalgorithm',
    'version': '0.4.0',
    'description': 'Implementation of Firefly Algorithm in Python',
    'long_description': '<p align="center">\n  <img width="200" src="https://raw.githubusercontent.com/firefly-cpp/FireflyAlgorithm/master/.github/imgs/firefly_logo.png">\n</p>\n\n---\n\n# Firefly Algorithm --- Implementation of Firefly algorithm in Python\n\n---\n\n[![PyPI Version](https://img.shields.io/pypi/v/fireflyalgorithm.svg)](https://pypi.python.org/pypi/fireflyalgorithm)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fireflyalgorithm.svg)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/fireflyalgorithm.svg)\n[![Downloads](https://pepy.tech/badge/fireflyalgorithm)](https://pepy.tech/project/fireflyalgorithm)\n[![AUR package](https://img.shields.io/aur/version/python-fireflyalgorithm?color=blue&label=Arch%20Linux&logo=arch-linux)](https://aur.archlinux.org/packages/python-fireflyalgorithm)\n[![GitHub license](https://img.shields.io/github/license/firefly-cpp/FireflyAlgorithm.svg)](https://github.com/firefly-cpp/FireflyAlgorithm/blob/master/LICENSE)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/FireflyAlgorithm.svg)\n[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/FireflyAlgorithm.svg)](http://isitmaintained.com/project/firefly-cpp/FireflyAlgorithm "Average time to resolve an issue")\n[![Percentage of issues still open](http://isitmaintained.com/badge/open/firefly-cpp/FireflyAlgorithm.svg)](http://isitmaintained.com/project/firefly-cpp/FireflyAlgorithm "Percentage of issues still open")\n![GitHub contributors](https://img.shields.io/github/contributors/firefly-cpp/FireflyAlgorithm.svg)\n\n## About\n\nThis package implements a nature-inspired algorithm for optimization called Firefly Algorithm (FA) in Python programming language.\n\n## Installation:\n\nInstall FireflyAlgorithm with pip:\n```sh\npip install fireflyalgorithm\n```\nTo install FireflyAlgorithm on Fedora, use:\n```sh\ndnf install python-fireflyalgorithm\n```\nTo install FireflyAlgorithm on Arch Linux, please use an [AUR helper](https://wiki.archlinux.org/title/AUR_helpers):\n```sh\n$ yay -Syyu python-fireflyalgorithm\n```\n\n## Usage:\n\n```python\nfrom fireflyalgorithm import FireflyAlgorithm\nfrom fireflyalgorithm.problems import sphere\n\nFA = FireflyAlgorithm()\nbest = FA.run(function=sphere, dim=10, lb=-5, ub=5, max_evals=10000)\n\nprint(best)\n```\n\n### Command line interface\n\nThe package also comes with a simple command line interface which allows you to evaluate the algorithm on several\npopular test functions\n\n```shell\nfirefly-algorithm -h\n```\n\n```text\nusage: firefly-algorithm [-h] --problem PROBLEM -d DIMENSION -l LOWER -u UPPER -nfes MAX_EVALS [-r RUNS] [--pop-size POP_SIZE] [--alpha ALPHA] [--beta-min BETA_MIN] [--gamma GAMMA] [--seed SEED]\n\nEvaluate the Firefly Algorithm on one or more test functions\n\noptions:\n  -h, --help            show this help message and exit\n  --problem PROBLEM     Test problem to evaluate\n  -d DIMENSION, --dimension DIMENSION\n                        Dimension of the problem\n  -l LOWER, --lower LOWER\n                        Lower bounds of the problem\n  -u UPPER, --upper UPPER\n                        Upper bounds of the problem\n  -nfes MAX_EVALS, --max-evals MAX_EVALS\n                        Max number of fitness function evaluations\n  -r RUNS, --runs RUNS  Number of runs of the algorithm\n  --pop-size POP_SIZE   Population size\n  --alpha ALPHA         Randomness strength\n  --beta-min BETA_MIN   Attractiveness constant\n  --gamma GAMMA         Absorption coefficient\n  --seed SEED           Seed for the random number generator\n```\n\n**Note:** The CLI script can also run as a python module (python -m niaarm ...)\n\n\n## Reference Papers:\n\nI. Fister Jr.,  X.-S. Yang,  I. Fister, J. Brest. [Memetic firefly algorithm for combinatorial optimization](http://www.iztok-jr-fister.eu/static/publications/44.pdf) in Bioinspired Optimization Methods and their Applications (BIOMA 2012), B. Filipic and J.Silc, Eds.\nJozef Stefan Institute, Ljubljana, Slovenia, 2012\n\nI. Fister, I. Fister Jr.,  X.-S. Yang, J. Brest. [A comprehensive review of firefly algorithms](http://www.iztok-jr-fister.eu/static/publications/23.pdf). Swarm and Evolutionary Computation 13 (2013): 34-46.\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Iztok Fister Jr.',
    'author_email': 'iztok@iztok-jr-fister.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/firefly-cpp/FireflyAlgorithm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
