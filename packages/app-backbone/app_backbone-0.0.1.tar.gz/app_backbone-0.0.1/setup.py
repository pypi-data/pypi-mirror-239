# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backbone', 'backbone.vendored']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'app-backbone',
    'version': '0.0.1',
    'description': 'A simple app utility framework that provides tooling for loading module extensions and an ECS like streams of composable entities.',
    'long_description': '# backbone\nA simple app utility framework that provides tooling for loading module extensions and an ECS like streams of composable entities.\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
