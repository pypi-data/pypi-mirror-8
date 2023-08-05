import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requires = filter(None, f.readlines())

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(name='elastic-git',
      version=version,
      description='JSON Object storage backed by Git & Elastic Search',
      long_description=README,
      classifiers=[
      "Programming Language :: Python",
      ],
      author='Simon de Haan',
      author_email='simon@praekeltfoundation.org',
      url='http://github.com/smn/elastic-git',
      license='BSD',
      keywords='git elasticsearch json',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires)
