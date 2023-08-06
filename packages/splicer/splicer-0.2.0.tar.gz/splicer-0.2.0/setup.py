import os.path
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

README_PATH = os.path.join(HERE, 'README.md')
try:
    README = open(README_PATH).read()
except IOError:
    README = ''

setup(
  name='splicer',

  version="0.2.0",
  description='the world is a database now you can query it with SQL',
  long_description=README,
  author='Scott Robertson',
  author_email='scott@triv.io',
  url='http://github.com/trivio/splicer',
  classifiers=[
      "Programming Language :: Python",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "Topic :: Software Development",
  ],
  packages = find_packages(),

  install_requires=[
    'codd',
    'zipper'
  ]
)
