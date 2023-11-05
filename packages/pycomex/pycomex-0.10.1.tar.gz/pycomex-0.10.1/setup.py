# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functional',
 'pycomex',
 'pycomex.app',
 'pycomex.examples',
 'pycomex.examples.results.004_inheritance.28_04_2023__13_45__bTbc',
 'pycomex.examples.results.02_basic.27_10_2023__16_59__2fAC',
 'pycomex.examples.results.02_basic.27_10_2023__17_34__nbuR',
 'pycomex.examples.results.02_basic.30_10_2023__07_30__O8Tv',
 'pycomex.examples.results.03_analysing.27_10_2023__16_59__1uZT',
 'pycomex.examples.results.03_analysing.27_10_2023__17_34__4qMQ',
 'pycomex.examples.results.04_inheritance.27_10_2023__16_59__FsRy',
 'pycomex.examples.results.04_inheritance.27_10_2023__17_34__93tT',
 'pycomex.examples.results.05_testing_mode.debug',
 'pycomex.functional']

package_data = \
{'': ['*'], 'pycomex': ['templates/*']}

install_requires = \
['click>=7.1.2',
 'jinja2>=3.0.3',
 'matplotlib>=3.5.3',
 'numpy>=1.22.0',
 'psutil>=5.7.2',
 'rich-click>=1.7.0,<=1.8.0']

entry_points = \
{'console_scripts': ['pycomex = pycomex.cli:cli']}

setup_kwargs = {
    'name': 'pycomex',
    'version': '0.10.1',
    'description': 'Python Computational Experiments',
    'long_description': 'None',
    'author': 'Jonas Teufel',
    'author_email': 'jonseb1998@gmail.com',
    'maintainer': 'Jonas Teufel',
    'maintainer_email': 'jonseb1998@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
