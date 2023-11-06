# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcpsecrets']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-secret-manager>=2.16.2,<3.0.0']

setup_kwargs = {
    'name': 'gcpsecrets',
    'version': '0.1.0',
    'description': 'Package to access GCP Secrets through Dictionary interface',
    'long_description': "# gcpsecrets\nGCP Secret Manager as Python Dictonary\n\n### Install\npip install git+https://github.com/tvaroska/gcpsecrets\n\n### Ussage\n\nDictionary accepts two types of keys:\n- str: the latest active version of the secter\n- tuple[str, str]: the exact version of the secret\n\nExamples:\n\nfrom gcpsecrets import GCPSecrets\n\nsecrets = GCPSecrets() # to use other than default project use argument project=...\n\napi_key = secrets['API_KEY']",
    'author': 'Boris Tvaroska',
    'author_email': 'tvaroska@google.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
