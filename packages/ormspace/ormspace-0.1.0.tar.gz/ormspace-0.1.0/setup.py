# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ormspace']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.7,<2.0.0',
 'anyio>=4.0.0,<5.0.0',
 'bcrypt>=4.0.1,<5.0.0',
 'deta[async]>=1.2.0,<2.0.0',
 'pydantic-settings>=2.0.3,<3.0.0',
 'pydantic>=2.4.2,<3.0.0']

setup_kwargs = {
    'name': 'ormspace',
    'version': '0.1.0',
    'description': 'Pydantic models working with deta.space api, including ORM features.',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
