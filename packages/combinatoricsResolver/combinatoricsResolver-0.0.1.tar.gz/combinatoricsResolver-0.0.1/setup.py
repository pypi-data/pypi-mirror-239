from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='combinatoricsResolver',
  version='0.0.1',
  description='Solve Combinatorcs related problems',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Harsh Verma',
  author_email='b220024@iiit-bh.ac.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='combinatorics', 
  packages=find_packages(),
  install_requires=[''] 
)