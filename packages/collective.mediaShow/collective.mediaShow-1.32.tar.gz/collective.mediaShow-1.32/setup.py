from setuptools import setup, find_packages
import os

version = '1.32'

setup(name='collective.mediaShow',
      version=version,
      description="A flexible slideshow that can show any kind of media or Plone content",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='slideshow media video audio mediashow',
      author='David Jonas, Andre Goncalves',
      author_email='david@intk.com, andre@intk.com',
      url='https://github.com/intk/collective.mediaShow',
      download_url='https://github.com/intk/collective.mediaShow/tarball/1.30',
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
