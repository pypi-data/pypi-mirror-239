# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lightautoml_gpu',
 'lightautoml_gpu.addons',
 'lightautoml_gpu.addons.autots',
 'lightautoml_gpu.addons.interpretation',
 'lightautoml_gpu.addons.uplift',
 'lightautoml_gpu.addons.utilization',
 'lightautoml_gpu.automl',
 'lightautoml_gpu.automl.gpu',
 'lightautoml_gpu.automl.presets',
 'lightautoml_gpu.automl.presets.gpu',
 'lightautoml_gpu.dataset',
 'lightautoml_gpu.dataset.gpu',
 'lightautoml_gpu.image',
 'lightautoml_gpu.ml_algo',
 'lightautoml_gpu.ml_algo.gpu',
 'lightautoml_gpu.ml_algo.torch_based',
 'lightautoml_gpu.ml_algo.torch_based.gpu',
 'lightautoml_gpu.ml_algo.tuning',
 'lightautoml_gpu.ml_algo.tuning.gpu',
 'lightautoml_gpu.pipelines',
 'lightautoml_gpu.pipelines.features',
 'lightautoml_gpu.pipelines.features.gpu',
 'lightautoml_gpu.pipelines.ml',
 'lightautoml_gpu.pipelines.selection',
 'lightautoml_gpu.reader',
 'lightautoml_gpu.reader.gpu',
 'lightautoml_gpu.report',
 'lightautoml_gpu.report.gpu',
 'lightautoml_gpu.tasks',
 'lightautoml_gpu.tasks.gpu',
 'lightautoml_gpu.tasks.losses',
 'lightautoml_gpu.tasks.losses.gpu',
 'lightautoml_gpu.text',
 'lightautoml_gpu.text.gpu',
 'lightautoml_gpu.transformers',
 'lightautoml_gpu.transformers.gpu',
 'lightautoml_gpu.utils',
 'lightautoml_gpu.validation',
 'lightautoml_gpu.validation.gpu']

package_data = \
{'': ['*'],
 'lightautoml_gpu.automl.presets': ['tabular_configs/*'],
 'lightautoml_gpu.automl.presets.gpu': ['tabular_configs_gpu/*'],
 'lightautoml_gpu.report': ['lama_report_templates/*']}

install_requires = \
['albumentations>=0.4.6',
 'autowoe>=1.2',
 'cmaes',
 'efficientnet-pytorch',
 'gensim',
 'holidays',
 'jinja2',
 'joblib',
 'json2html',
 'lightgbm>=2.3,<3.0',
 'log-calls',
 'networkx',
 'nltk',
 'numpy',
 'opencv-python',
 'optuna',
 'pandas>=1',
 'poetry-core>=1.0.0,<2.0.0',
 'pywavelets',
 'pyyaml',
 'scikit-image',
 'scikit-learn>=0.22',
 'scipy',
 'seaborn',
 'torch>=1.6',
 'torchvision',
 'tqdm',
 'transformers>=4',
 'webencodings']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'pdf': ['weasyprint>=52.5,<53.0', 'cffi>=1.14.5,<2.0.0']}

setup_kwargs = {
    'name': 'lightautoml-gpu',
    'version': '0.2.15',
    'description': 'Fast and customizable framework for automatic ML model creation (AutoML)',
    'long_description': '## Developing LightAutoML on GPU\n\nTo develop LightAutoML on GPUs using RAPIDS some prerequisites need to be met:\n1. NVIDIA GPU: Pascal or higher\n2. CUDA 11.0 (drivers v460.32+) or higher need to be installed\n3. Python version 3.8 or higher\n4. OS: Ubuntu 16.04/18.04/20.04 or CentOS 7/8 with gcc/++ 9.0+\n\n### Installation\n\n[Anaconda](https://www.anaconda.com/products/individual#download-section) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is necessary to install RAPIDS and work with environments.\n\n1. Once you install Anaconda/Miniconda, you need to set up your own environment. For example:\n```bash\nconda create -n lama_venv python=3.8\nconda activate lama_venv\n```\n\n2. To install RAPIDS for Python 3.8 and CUDA 11.0 use the following command:\n```bash\nconda install -c rapidsai -c nvidia -c conda-forge rapids=22.10 cudatoolkit=11.0\npip install dask-ml\n```\n\n3. To clone the project on your own local machine:\n```bash\ngit clone https://github.com/ekonyagin/LightAutoML-1.git\ncd LightAutoML-1\n```\n\n4. Install LightAutoML in develop mode and other necessary libraries:\n```bash\npip install .\npip install catboost\npip install py-boost\n```\n\nAfter you change the library code, you need to re-install the library: go to LightAutoML directory and call ```pip install ./ -U```\n\nPlease note, if you use NVIDIA GPU Ampere architecture (i.e. Tesla A100 or RTX3000 series), you may need to uninstall pytorch and install it manually \ndue to compatibility issues. To do so, run following commands:\n```bash\npip uninstall torch torchvision\npip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 -f https://download.pytorch.org/whl/torch_stable.html\n```\n\nOnce the RAPIDS is installed, the environment is fully ready. You can activate it using the `source` command and test and implement your own code.\n\n',
    'author': 'Alexander Ryzhkov',
    'author_email': 'AMRyzhkov@sberbank.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lightautoml.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
