from setuptools import setup, find_packages
setup(
   name='pymadas',
   version='0.1',
   packages=find_packages(),
   install_requires=[
      'lxml',
   ],
   entry_points='''
      [console_scripts]
      pymadas=pymadas.madas_cli:main
      ''',
)