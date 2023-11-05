from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='spetslogging',
  version='0.0.1',
  author='Dmitry Goncharov (_DiNAMitiON_)',
  author_email='dinamition42@gmail.com',
  description='SpetsLogging is a simple way to log in the console and in a file.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/DiNAMitiON/SpetsLoging',
  packages=['spetslogging'],
  install_requires=['colorama==0.4.6'],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='Logging, write to file',
  project_urls={
    'SpetsDevelopers | Support': 'https://discord.gg/z5hEVQ5agn/',
    'Source Code': 'https://github.com/DiNAMitiON/SpetsLoging/'
  },
  python_requires='>=3.7'
)