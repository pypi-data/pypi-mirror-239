# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fms_robot_plugin']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0', 'pydantic>=2.3.0,<3.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'fms-robot-plugin',
    'version': '0.1.6rc21',
    'description': '',
    'long_description': '# FMS Robot Plugin Library',
    'author': 'Dionesius Agung',
    'author_email': 'dionesius@movel.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
