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
  version='0.0.1',
  description='Open Keyshare Threshold Scheme',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Anthony Kruger',
  author_email='devadmin@impression.cloud',
  license='MIT', 
  classifiers=classifiers,
  keywords='keyshare', 
  packages=find_packages(),
  install_requires=['cryptography'] 
)
