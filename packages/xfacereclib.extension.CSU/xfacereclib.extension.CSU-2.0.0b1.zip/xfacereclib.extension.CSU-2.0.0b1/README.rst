.. vim: set fileencoding=utf-8 :
.. Manuel Guenther <manuel.guenther@idiap.ch>
.. Fri Sep 19 12:51:09 CEST 2014

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/xfacereclib.extension.CSU/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/idiap/xfacereclib.extension.CSU/master/index.html
.. image:: https://travis-ci.org/idiap/xfacereclib.extension.CSU.svg?branch=master
   :target: https://travis-ci.org/idiap/xfacereclib.extension.CSU
.. image:: https://coveralls.io/repos/idiap/xfacereclib.extension.CSU/badge.png
   :target: https://coveralls.io/r/idiap/xfacereclib.extension.CSU
.. image:: https://img.shields.io/badge/github-master-0000c0.png
   :target: https://github.com/idiap/xfacereclib.extension.CSU/tree/master
.. image:: http://img.shields.io/pypi/v/xfacereclib.extension.CSU.png
   :target: https://pypi.python.org/pypi/xfacereclib.extension.CSU
.. image:: http://img.shields.io/pypi/dm/xfacereclib.extension.CSU.png
   :target: https://pypi.python.org/pypi/xfacereclib.extension.CSU


===================================================================
 FaceRecLib Wrapper classes for the CSU Face Recognition Resources
===================================================================

This satellite package to the FaceRecLib_ provides wrapper classes for the CSU face recognition resources, which can be downloaded from http://www.cs.colostate.edu/facerec.
Two algorithms are provided by the CSU toolkit (and also by this satellite package): the local region PCA (LRPCA) and the LDA-IR (also known as CohortLDA).

For more information about the LRPCA and the LDA-IR algorithm, please refer to the documentation on http://www.cs.colostate.edu/facerec/.
For further information about the FaceRecLib_, please read its `Documentation <http://pythonhosted.org/facereclib/index.html>`_.
On how to use this package in a face recognition experiment, please see http://pypi.python.org/pypi/xfacereclib.paper.BeFIT2012


Installation Instructions
-------------------------

The current package is just a set of wrapper classes for the CSU facerec2010 module, which is contained in the `CSU Face Recognition Resources <http://www.cs.colostate.edu/facerec>`_, where you need to download the Baseline 2011 Algorithms.
Please make sure that you have read installation instructions in the Documentation_ of this package on how to patch the original source code to work with our algorithms, before you try to go on woth this package.

The FaceRecLib_ and parts of this package rely on Bob_, an open-source signal-processing and machine learning toolbox.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.


Documentation
-------------
For further documentation on this package, please read the `Stable Version <http://pythonhosted.org/xfacereclib.extension.CSU/index.html>`_ or the `Latest Version <https://www.idiap.ch/software/bob/docs/latest/bioidiap/xfacereclib.extension.CSU/master/index.html>`_ of the documentation.

For a list of tutorials on packages ob Bob_, or information on submitting issues, asking questions and starting discussions, please visit its website.


.. _bob: https://www.idiap.ch/software/bob
.. _facereclib: http://pypi.python.org/pypi/facereclib

