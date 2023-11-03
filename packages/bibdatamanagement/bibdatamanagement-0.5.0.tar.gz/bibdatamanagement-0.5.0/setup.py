# All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland,
# IPESE Laboratory, Copyright 2023
# This work can be distributed under the CC BY-NC-SA 4.0 License.
# See the LICENSE file for more details.
#
# Author: Joseph Loustau <joseph.loustau@epfl.ch>

from setuptools import find_packages, setup
import platform
import sys

packages = ["pybtex >= 0.24",
            "pandas>=1.4",
            "plotly"]

setup(name="bibdatamanagement",
      version="0.5.0",

      author="Joseph Loustau",
      author_email="joseph.loustau@epfl.ch",

      maintainer="IT team of IPESE Laboratory from EPFL",
      maintainer_email="itsupport.ipese@groupes.epfl.ch",

      description="Package to read .bib file annotations and retrieve values from it",
      long_description="README.md",

      url="https://gitlab.epfl.ch/ipese/bibdatamanagement/bibdata-package/",

      packages=find_packages(),

      package_data={
          '': ['*.Rmd', '*.csv', '*.R', '*.bib'],
      },

      platforms=[platform.platform()],  # TODO indicate really tested platforms

      install_requires=packages,

      keywords="bibliography",

      classifiers=["Development Status :: 4 - Beta",
                   "Environment :: Console",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "License :: Free For Educational Use",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "Topic :: Software Development :: Code Generators",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Utilities"],
      license="Free For Educational Use License"


      )
