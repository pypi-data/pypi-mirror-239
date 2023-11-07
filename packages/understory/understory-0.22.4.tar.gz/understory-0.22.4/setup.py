# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory', 'understory.templates']

package_data = \
{'': ['*'], 'understory': ['static/*']}

install_requires = \
['phonenumbers>=8.12.55,<9.0.0',
 'python-whois>=0.8.0,<0.9.0',
 'stripe>=5.2.0,<6.0.0',
 'webint-data>=0.0,<0.1',
 'webint-system>=0.0,<0.1',
 'webint>=0.1,<0.2']

entry_points = \
{'websites': ['understory = understory.__web__:app']}

setup_kwargs = {
    'name': 'understory',
    'version': '0.22.4',
    'description': 'a decentralized social web host',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
