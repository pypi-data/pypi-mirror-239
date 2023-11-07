# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hakoniwa', 'hakoniwa.entity']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.8,<0.28.0', 'torch>=2.0.1,<3.0.0', 'transformers>=4.31.0,<5.0.0']

entry_points = \
{'console_scripts': ['hakoniwa = hakoniwa.cli:run']}

setup_kwargs = {
    'name': 'hakoniwa',
    'version': '0.1.2',
    'description': '',
    'long_description': '# 箱庭 (Hakoniwa) ![Build](https://github.com/Lewuathe/hakoniwa/actions/workflows/main.yml/badge.svg)\n\n![hakoniwa](./hakoniwa.png)\n\n"Hakoniwa" which is a miniature garden in Japanese is a simulation framework letting LLM based entities play around inside. This framework aims to provide the way to experiment how the LLM behaves in the specific domain defined as a simple state machine which has states and actions respectively. The framework is designed to be able to be used for the following purposes:\n\n- To experiment how the LLM behaves in the specific enviroment.\n- To collect the behavior data resembling the human behavior in the real world.\n\n## Usage\n\n### Define the state machine\nFirst of all, we can define the state machine where each agent play around inside. The state machine is defined as a YAML file. The following is the example of the state machine definition.\n\n```yaml\nstates:\n  state0:\n    name: In the house\n    choices:\n      - action: Go outside\n        next: state1\n      - action: Stay inside\n        next: state0\n  state1:\n    name: Outside\n    choices:\n      - action: Go to the supermarket\n        next: state2\n      - action: Go back home\n        next: state0\n  state2:\n    name: In the supermarket\n    choices:\n      - action: Go back home\n        next: state0\n\nentities:\n  - name: A living thing\n    type: openai\n    initial_state: state0\n```\n\nThe state machine consists of the following two parts.\n- `states`: The list of states in the state machine. `choices` is the list of actions which the agent can take from the state.\n- `entities`: The list of entities which play around inside the state machine.\n\nThe CLI script, `hakoniwa` is usable to run the simulation with the state machine definition.\n\n```\n$ poetry run hakoniwa -f env.yaml\n```\n\nPlease make sure to set the `OPENAI_APIKEY` if you set the OpenAI entity in the environment. \n\nYou will see what it does in the environment.\n\n```\nINFO:hakoniwa.environment:A living thing,{\'action\': \'Stay inside\', \'next\': \'state0\'}\nINFO:hakoniwa.environment:A living thing,{\'action\': \'Go outside\', \'next\': \'state1\'}\nINFO:hakoniwa.environment:A living thing,{\'action\': \'Go to the supermarket\', \'next\': \'state2\'}\n```\n\n## Dependencies\n\nInstall [Poetry](https://python-poetry.org/) and run the following command to install dependencies.\n\n```\n$ poetry install\n```\n\n## Development\n\nWe can run the unit test with pytest.\n\n```\n$ make test\n```\n',
    'author': 'Kai Sasaki',
    'author_email': 'lewuathe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
