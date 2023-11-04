from setuptools import setup, find_packages
setup(name='geographie',
      version='0.1',
      description='A simple, easy-to-use tool to make interactive maps',
      url='https://github.com/geographieactuelle/fairedescartes',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['pyshp', 'colour'])
