from setuptools import setup, find_packages
import os

version = '0.20'

setup(name='collective.media',
      version=version,
      description="Adds functionality to retrieve and prioritize media inside of folderish items.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='folderish media',
      author='David Jonas, Andre Goncalves',
      author_email='david@intk.com, andre@intk.com',
      url='https://github.com/intk/collective.media',
      download_url='https://github.com/intk/collective.media/tarball/0.12',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
