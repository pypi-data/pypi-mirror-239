# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pfun_path_helper']

package_data = \
{'': ['*']}

install_requires = \
['build>=1.0.3,<2.0.0', 'setuptools>=68.2.2,<69.0.0']

setup_kwargs = {
    'name': 'pfun-path-helper',
    'version': '0.0.4',
    'description': 'Path helper script',
    'long_description': 'None',
    'author': 'Robbie Capps',
    'author_email': 'robbie@pfun.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
