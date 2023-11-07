gradientcobra v1.0.6
====================

|Travis Status| |Coverage Status| |Python39|

Introduction
------------

``gradientcobra`` is the ``python`` package implementation of Gradient COBRA method by `S. Has (2023) <https://jdssv.org/index.php/jdssv/article/view/70>`__, which is a kernel-based consensual aggregation method for regression problems. 
It is a regular kernel-based version of ``COBRA`` method by `Biau et al. (2016) <https://www.sciencedirect.com/science/article/pii/S0047259X15000950>`__. 
We have theoretically shown that the consistency inheritance property also holds for this kernel-based configuration, and the same convergence rate as classical COBRA is achieved.
Moreoever, gradient descent algorithm is applied to efficiently estimate the bandwidth parameter of the method. This efficiency is illustrated in several numerical experiments on simulated and real datasets.

From version ``v1.0.6``, the aggregation method using input-output trade-off by `A. Fischer and M. Mougeot (2019) <https://www.sciencedirect.com/science/article/pii/S0378375818302349>`__ is also available for regression problems. This method is available as ``MixCOBRARegressor`` in ``gradientcobra.mixcobra`` module.
For more information, read "Documentation and Examples".


Installation
------------

In your terminal, run the following command to download and install from PyPI:

``pip install gradientcobra``


Citation
--------

If you find ``gradientcobra`` helpful, please consider citing the following papaers:

-   S.\  Has (2023), `Gradient COBRA: A kernel-based consensual aggregation for regression <https://jdssv.org/index.php/jdssv/article/view/70>`__.

-   A.\  Fischer and M. Mougeot (2019), `Aggregation using input-output trade-off <https://www.sciencedirect.com/science/article/pii/S0378375818302349>`__.

-   G.\  Biau, A. Fischer, B. Guedj and J. D. Malley (2016), `COBRA: A combined regression strategy <https://doi.org/10.1016/j.jmva.2015.04.007>`__.


Documentation and Examples
--------------------------

For more information and how to use the package, read `gradientcobra documentation <https://hassothea.github.io/files/CodesPhD/gradientcobra_doc.html>`__.

Read also:

- `GradientCOBRA documentation <https://hassothea.github.io/files/CodesPhD/GradientCOBRA.html>`__.

- `MixCOBRARegressor documentation <https://hassothea.github.io/files/CodesPhD/mixcobra.html>`__.

Dependencies
------------

-  Python 3.9+
-  numpy, scipy, scikit-learn, matplotlib, pandas, seaborn, plotly

References
----------

-  S. Has (2023). A Gradient COBRA: A kernel-based consensual aggregation for regression. 
   Journal of Data Science, Statistics, and Visualisation, 3(2).
-  A.\  Fischer, M. Mougeot (2019). Aggregation using input-output trade-off. 
   Journal of Statistical Planning and Inference, 200.
-  G. Biau, A. Fischer, B. Guedj and J. D. Malley (2016), COBRA: A
   combined regression strategy, Journal of Multivariate Analysis.
-  M. Mojirsheibani (1999), Combining Classifiers via Discretization,
   Journal of the American Statistical Association.

.. |Travis Status| image:: https://img.shields.io/travis/hassothea/gradientcobra.svg?branch=master
   :target: https://travis-ci.org/hassothea/gradientcobra

.. |Python39| image:: https://img.shields.io/badge/python-3.9-green.svg
   :target: https://pypi.python.org/pypi/gradientcobra

.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/hassothea/gradientcobra.svg
   :target: https://codecov.io/gh/hassothea/gradientcobra
