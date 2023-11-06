# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygplib']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=3.1.1,<4.0.0']

extras_require = \
{'docs': ['Sphinx>=7.2.6,<8.0.0',
          'sphinx-removed-in>=0.2.1,<0.3.0',
          'sphinxcontrib-trio>=1.1.2,<2.0.0',
          'pallets-sphinx-themes>=2.1.1,<3.0.0'],
 'test': ['pytest>=7.4.2,<8.0.0',
          'pytest-cov>=4.1.0,<5.0.0',
          'tox>=4.11.3,<5.0.0',
          'python-sat>=0.1.8.dev10,<0.2.0',
          'argparse>=1.4.0,<2.0.0']}

setup_kwargs = {
    'name': 'pygplib',
    'version': '2.1.0',
    'description': 'Python First-Order Graph Property Library',
    'long_description': 'Pygplib: Python First-Order Graph Property Library\n==================================================\n\n|PyPI Version| |Python Versions| |Test| |Coverage| |License| |Documentation|\n\nIntroduction\n============\n\n``Pygplib`` (Python First-Order Graph Property Library) is a Python module \nfor constructing, manipulating, and encoding graph properties expressible \nwith first-order logic of graphs.\nIt serves as a prototyping tool to tackle with \nvarious graph related applications.\nIt provides access to state-of-the-art satisfiability technologies \nwithout advanced knowledge.\nBasic steps to follow are :\n\n- Express a graph property of interest as a first-order formula.\n- Set a graph structure, and encode a first-order formula into CNF, \n  a canonical normal form for propositional formulas.\n- Apply satisfiability tools to the CNF to compute satisfying\n  assignments.\n- Decode the result into an assignment of first-order variables.\n\nDocumentation\n=============\n\nFor installation, examples, tutorials, and so on, please see `online documentation <https://pygplib.readthedocs.io/en/latest/>`__ .\n\n\nCitation\n========\n\nPlease cite the following paper if you use ``pygplib``:\n\n::\n\n   Takahisa Toda, Takehiro Ito, Jun Kawahara, Takehide Soh, Akira Suzuki, Junichi Teruyama, Solving Reconfiguration Problems of First-Order Expressible Properties of Graph Vertices with Boolean Satisfiability, The 35th IEEE International Conference on Tools with Artificial Intelligence (ICTAI 2023), accepted.\n\nBugs/Requests/Discussions\n=========================\n\nPlease report bugs and requests from `GitHub Issues\n<https://github.com/toda-lab/pygplib/issues>`__ , and \nask questions from `GitHub Discussions <https://github.com/toda-lab/pygplib/discussions>`__ .\n\nHistory\n=======\nPlease see `CHANGES <https://github.com/toda-lab/pygplib/blob/main/CHANGES.rst>`__ .\n\nLicense\n=======\n\nPlease see `LICENSE <https://github.com/toda-lab/pygplib/blob/main/LICENSE>`__ .\n\n.. |Test| image:: https://github.com/toda-lab/pygplib/actions/workflows/test.yml/badge.svg\n   :target: https://github.com/toda-lab/pygplib/actions/workflows/test.yml\n\n.. |Coverage| image:: https://codecov.io/gh/toda-lab/pygplib/graph/badge.svg?token=WWR54JE3M1\n   :target: https://codecov.io/gh/toda-lab/pygplib\n\n.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/pygplib\n   :target: https://pypi.org/project/pygplib/\n   :alt: PyPI - Python Versions\n\n.. |PyPI Version| image:: https://img.shields.io/pypi/v/pygplib\n   :target: https://pypi.org/project/pygplib/\n   :alt: PyPI - Version\n\n.. |License| image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n\n.. |Documentation| image:: https://readthedocs.org/projects/pygplib/badge/?version=latest\n    :target: https://pygplib.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n',
    'author': 'Takahisa Toda',
    'author_email': 'pygplib+contact@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/toda-lab/pygplib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
