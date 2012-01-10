# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = open(os.path.join("sc", "newsletter", "creator", "version.txt")).read().strip()

setup(name='sc.newsletter.creator',
      version=version,
      description="Creates HTML for sending newsletter",
      long_description=open(os.path.join("sc", "newsletter", "creator", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone :: 4.1",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='newsletter simples creator',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sc', 'sc.newsletter'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'five.grok>=1.3.0',
          'plone.resource>=1.0b5',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
