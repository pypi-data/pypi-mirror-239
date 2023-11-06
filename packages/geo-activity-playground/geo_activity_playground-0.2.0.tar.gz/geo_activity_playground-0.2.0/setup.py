# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geo_activity_playground',
 'geo_activity_playground.core',
 'geo_activity_playground.explorer',
 'geo_activity_playground.strava']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'fitdecode>=0.10.0,<0.11.0',
 'geojson>=3.0.1,<4.0.0',
 'gpxpy>=1.5.0,<2.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=2.0,<3.0',
 'pyarrow>=12.0.1,<13.0.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.3.0,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'stravalib>=1.3.3,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['geo-playground = geo_activity_playground.__main__:main']}

setup_kwargs = {
    'name': 'geo-activity-playground',
    'version': '0.2.0',
    'description': 'Analysis of geo data activities like rides, runs or hikes.',
    'long_description': 'None',
    'author': 'Martin Ueding',
    'author_email': 'mu@martin-ueding.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
