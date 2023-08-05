InversionTest: A Sequence Permutation Similarity and Hypothesis Testing Package
**************************************************************
Author: Benjamin D. Nye
Contact: Dr.Ben.Nye@gmail.com
Description: Library for inversion counting which can adjust for ties and censored data
             (e.g. left censored, right censored, etc). The intention of this library is
             to examine the distance from the sequence of elements to some reference sequence.
             It is also calculates an exact PMF of the distribution for inversion counts under
             the case where all permutations are equally likely, as well as a normal approximation
             for this same distribution.  Wilcoxon and sign tests are provided for hypothesis testing,
             where a group of permutations are compared against a single reference sequence.  This
             sort of testing would be needed for situations where a distribution of collected
             sequences might be compared against a "known correct" reference sequence.
Python Version: 2.7
Package Version: 1.1

--------------------------------------
------  License: APL 2.0        ------
--------------------------------------
Copyright 2012 Benjamin D. Nye

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---------------------------------------------------
------             Contents:                 ------
---------------------------------------------------
The root of this installation package should contain the following files:
- Changes.txt : List of changes to the package, by version
- License.txt : License information
- Readme.txt  : This file
- setup.py    : Installer script for the package

It should also contain the following directories:
- Documentation : HTML documentation for the package
- InversionTest : Source code for the package
- Examples      : Two example use-cases for the package

---------------------------------------------------
------           Installation:               ------
---------------------------------------------------
InversionTest is written in Python, so it requires a Python
interpreter to be installed.  InversionTest is compatible with
versions of Python 2.7 and higher (including Python 3).  However,
as Python 3 is not backwards compatible, InversionTest has a 
separate release for Python 2.7 and Python 3.x installations.
This readme covers a Python 2.7 installation.

InversionTest can be installed in one of two ways:

1. Running Setup.py (Requires the 'setuptools' package)
The file setup.py is created by setuptools, the standard Python
package installer.  Run the following code at the command line:

>>> python setup.py install

The file setup.py should be contained in the same directory as this readme.
This installation method requires the 'setuptools' package, which is found
at http://pypi.python.org/pypi/setuptools#downloads.  'setuptools' is the
standard method for installing Python 2 packages and is recommended.

2. Installing source manually
As this package requires no special setup instructions, it can be added
or removed from a Python installation manually.  To do this, copy the
InversionTest directory where this readme file is found to the directory:

<python installation>\Lib\site-packages\

The <python installation> directory is the location where the matching
version of Python is installed on your machine.  For example, if you are
using InversionTest for Python 2.7, this would be C:\Python27 for a
default installation on a Windows machine.  This should result in the 
following directory structure:

<python installation>
   Lib
      site-packages
         InversionTest
	        Tests

---------------------------------------------------
------   Optional 3rd Party Libraries:       ------
---------------------------------------------------
For more efficient test calculations can optionally install:
* SciPy - For scipy.stats binomial and normal cdf functions

Information on installing SciPy is available at http://www.scipy.org/Download

-------------------------------------------------------------------
------ InversionTest Application programming interface (API) ------
-------------------------------------------------------------------

The API for InversionTest contains the following functions:
inversionCountMax 	            Calculates the maximum possible inversions 
inversionCountMean 	            Calculates the mean inversions across permutations 
inversionCountVariance          Calculates the variance of inversions across permutations   
inversionCount			        Calculates the inversion count between sequences  
inversionSimilarity	            Calculates the similarity between sequences 
inversionCountCDF		        Calculates the probability of a permutation with  
                                equal or less inversions than the given sequence 
medianSequence			        Calculates the typical sequence for the given permutations
inversionWilcoxonTest           Hypothesis test for permutations against a reference sequence 
inversionSignTest		        Faster, less powerful hypothesis function than Wilcoxon 
                                but capable of testing various levels of similarity
inversionPermutationMeanTest    Hypothesis test similar to the Wilcoxon test, but
                                uses permutation/MonteCarlo testing for the differences
                                in mean similarity between sets of sequences
inversionPermutationRankTest    Same as the permutation means test, but uses rank order
filterElements                  Utility function to remove elements from a sequence

This package is expected to be installed in the Python site-packages subdirectory,
located at <python installation>\Lib\site-packages.  The InversionTest contents should
be contained at <python installation>\Lib\site-packages\InversionTest for the example
code to execute properly.  If the instructions in the Installation section are followed,
the command "import InversionTest" should work properly within Python scripts.

--------------------------------------------
------           Tests:               ------
--------------------------------------------
InversionTest comes with full test coverage.  To check that InversionTest is installed
properly, the following command can be run:

>>> python -m unittest InversionTest.Tests.Suite

For a standard installation where SciPy is also installed, this should raise zero errors
and warnings.  For an installation where SciPy is not installed, this raises 5 warnings
that note which functions that access SciPy functionality are not available.  These 
warnings are harmless, as InversionTest uses its own functionality instead of SciPy
when these functions are not available (SciPy implements C versions of binomial tests
and some other functions, but these are only used to provide a minor speedup for 
certain hypothesis tests).  Finally, because some tests are based on Monte Carlo
hypothesis testing analysis, there will be occasional failures due to random
outliers being generated and tested.  These are within the bounds expected for the
relevant hypothesis tests.

----------------------------------------------------
------           Documentation:               ------
----------------------------------------------------
Full HTML documentation is provided with the InversionTest package, generated using
epydoc.  This documentation covers all functions and classes in the package in detail.
This documentation is contained in the "Documentation" subdirectory of this package.
Open "Documentation\index.html" to browse these documents.

----------------------------------------------------
------             Examples:                  ------
----------------------------------------------------
Two small examples are included with the package.  These are contained in the 
"Examples" subdirectory.  The following two examples are available:

1. Example 1: UseCase1_SimulationValidation.py
Example 1 examines an application of InversionTest to validating simulations
of the spread of behavior within a region.  The associated data files are
"LocalizedSimResults.csv" and "MediaSimResults.csv" which represent two 
hypothetical simulations of the spread of a new designer drug across regions.
LocalizedSim assumes that the spread occurs more locally, while MediaSim assumes
that the spread is primarily driven by prior probabilities for each region.

2. Example 2: UseCase2_UserPreferences.py
Example 2 examines an an application of InversionTest to generating a social
network based on user preference orderings for movies.  This example loads a
dictionary that maps the name of a user to a list that contains the order that
they prefer a set of movies.  These orderings are used to calculate the similarity
between each pair of users.  The similarity values are visualized using the
networkx package, if installed.  Instructions on how to install networkx are
contained at http://networkx.lanl.gov/ or http://pypi.python.org/pypi/networkx.

These examples should execute properly with no errors.

--------------------------------------------------------
------             Feedback/Bugs                  ------
--------------------------------------------------------
If you have any feedback or bugs, please direct them to Dr.Ben.Nye@gmail.com.
While responses may not be immediate, efforts will be made to fix any bugs
or clarify the documentation for easier use.