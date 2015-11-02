from setuptools import setup, find_packages


setup(name='pycfn-yaml',
      version='0.1',
      description='Utilities for simplified AWS Cloudformation Templates in YAML',
      author='Scott VanDenPlas',
      author_email='scott@elelsee.com',
      url='https://github.com/elelsee/pycfn-yaml',
      packages=find_packages(),
      py_modules= ['pycfn_yaml'],
      install_requires = ['PyYAML==3.11', 'troposphere==1.2.2', 'awacs']
     )
