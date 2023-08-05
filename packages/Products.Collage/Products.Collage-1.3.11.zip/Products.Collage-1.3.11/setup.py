# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def _textOfModuleFile(filename):
    return open(filename, 'r').read().strip()

setup(name='Products.Collage',
      version='1.3.11',
      description=("A product to create page compositions in Plone."),
      long_description='\n\n'.join([
          _textOfModuleFile(name)
          for name in (
               'README.rst',
               os.path.join('docs', 'DEVELOPERS.txt'),
               os.path.join('docs', 'HISTORY.txt'))]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Plone :: 3.2",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Development Status :: 5 - Production/Stable",
        ],
      keywords='plone layout composition',
      author='Malthe Borch',
      author_email='mborch@gmail.com',
      url='http://www.plone.org/products/collage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.Archetypes',
      ],
      extras_require={
          'test': [
              'Products.PloneTestCase',
              ],
          },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
