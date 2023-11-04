# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mustaching']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1', 'pandera>=0', 'plotly>=5']

setup_kwargs = {
    'name': 'mustaching',
    'version': '4.0.3',
    'description': 'A Python 3.9+ library inspired by Mr. Money Mustache to summarize and plot personal finance data given in a CSV file of transactions.',
    'long_description': 'None',
    'author': 'Alex Raichev',
    'author_email': 'alex@raichev.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
