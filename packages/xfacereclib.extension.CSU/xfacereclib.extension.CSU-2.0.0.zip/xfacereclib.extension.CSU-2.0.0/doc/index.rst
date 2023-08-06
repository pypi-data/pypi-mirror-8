.. vim: set fileencoding=utf-8 :
.. Manuel Guenther <manuel.guenther@idiap.ch>
.. Thu Jul  4 12:22:22 CEST 2013

.. _xfacereclib.extension.CSU:

=================================================
 Wrapper classes for the CSU facerec2010 classes
=================================================

This satellite package to the FaceRecLib_ provides wrapper classes for the `CSU Face Recognition Resources`_.
Two algorithms are provided by the CSU toolkit (and also by this satellite package): the local region PCA (LRPCA) and the LDA-IR (also known as CohortLDA).

In fact, this satallite package just provides the source to be able to execute experiments using LRPCA and LDA-IR.
Though you actually can, this package is not designed to run any face recognition experiment with it.
Please refer to the `FaceRecLib Documentation`_ to get more information on how to use this package to run face recognition experiments.
A working example, which is able to re-run the original LRPCA and LDA-IR experiments, which are reported in [PBD+11]_ and [LBP+12]_, respectively, can be found under `xfacereclib.paper.BeFIT2012 <http://pypi.python.org/pypiu/xfacereclib.paper.BeFIT2012>`_.

.. note::
   In the above mentioned example, we were not able to perfectly re-generate the results from the original CSU toolkit, though our results were relatively close.
   It seems that different versions of the dependent packages (like OpenCV, PIL or similar) produce slightly different results.

.. [PBD+11]        P.J. Phillips, J.R. Beveridge, B.A. Draper, G. Givens, A.J. O'Toole, D.S. Bolme, J. Dunlop, Y.M. Lui, H. Sahibzada and S. Weimer. "An introduction to the good, the bad, & the ugly face recognition challenge problem". Automatic face gesture recognition and workshops (FG 2011), pages 346-353. 2011.
.. [LBP+12]        Y.M. Lui, D. Bolme, P.J. Phillips, J.R. Beveridge and B.A. Draper. "Preliminary studies on the good, the bad, and the ugly face recognition challenge problem". Computer vision and pattern recognition workshops (CVPRW), pages 9-16. 2012.



Documentation
-------------

.. toctree::
   :maxdepth: 2

   installation
   py_api


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst
