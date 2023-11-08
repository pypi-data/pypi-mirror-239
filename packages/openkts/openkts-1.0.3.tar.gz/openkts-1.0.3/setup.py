from setuptools import find_packages, setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Information Technology',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='openkts',
  version='1.0.3',
  description='Open Keyshare Threshold Scheme',
  long_description='This is an m of n key sharing solution with split/join functionality and offers password protection on individual shares with fernet encryption.',
  url='',
  author='Anthony Kruger',
  author_email='devadmin@impression.cloud',
  license='MIT',
  classifiers=classifiers,
  keywords='keyshare',
  packages=find_packages(),
  install_requires=['']
)
