from setuptools import setup, find_packages
import os

version = '0.3.0'

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(name='tgext.tagging',
      version=version,
      description="Tagging support for TurboGears2 applications",
      long_description=README,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: TurboGears"
        ],
      keywords='turbogears2.extension',
      author='Alessandro Molina',
      author_email='alessandro.molina@axant.it',
      url='http://bitbucket.org/_amol_/tgext.tagging',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tgext'],
      include_package_data=True,
      package_data={'': ['*.png', '*.html']},
      zip_safe=False,
      install_requires= [
        "sqlalchemy",
        "zope.sqlalchemy >= 0.4"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
