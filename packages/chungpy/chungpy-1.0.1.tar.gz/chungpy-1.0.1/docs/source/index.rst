.. ChungPy documentation master file, created by
   sphinx-quickstart on Thu Sep 25 14:55:11 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ChungPy's documentation!
===================================

An implementation of Chung's linear time algorithm for solution of the Maximum Density Segment Problem with additional features, namely simultaneous identification
of Minimum Density Segments and consideration of content constraints

Given a sequence :math:`S` of :math:`n` numerical pairs :math:`(a_i,w_i)` with values :math:`a_i` and widths :math:`w_i >0` for :math:`i \in {1,...,n}` 
the width of a consecutive subsequence :math:`S(i,j)` of :math:`S` with :math:`1 \leq i \leq j \leq n` is given by

.. math::
   w(i,j) = \sum_{k=i}^j w_k

and its density is given by 

.. math::
   d(i,j) = \frac{\sum_{k=i}^j a_k}{w(i,j)}.

The Maximum Density Segment Problem (MDSP) comprises the identification of a consecutive subsequence :math:`S(i^*,j^*)` with largest possible density, i.e. the Maximum Density Segment.

Chung \& Lu [#chung]_ presented a linear time algorithm for solution of the MDSP with arbitrary width contraints :math:`w_{min}` and :math:`w_{max}`, s.t. :math:`w_{min} \leq w(i^*,j^*) \leq w_{max}`.
Their algorithm returns for each possible stop index :math:`j'` of possible subsequences :math:`S(i',j')` the corresponding start index of the shortest segment with 
highest possible density stopping at :math:`j'`.

ChungPy is an implementation of Chung \& Lu's algorithm including the ability of additional consideration of content constraints :math:`c_{min}` and :math:`c_{max}`, s.t. :math:`c_{min} \leq j^*-i^*+1 \leq c_{max}`.
Furthermore, ChungPy allows for computation of Minimum Density Segments, i.e. the identification of a consecutive subsequence :math:`S(i^{**},j^{**})` with smallest possible density.

ChungPy is hosted at https://bitbucket.org/corinnaernst/chungpy.

.. [#chung] K.-M. Chung and H.-I. Lu. An optimal algorithm for the maximum-density segment problem. SIAM Journal on Computing, 34(2), 2005.

Contents:

.. toctree::
   :maxdepth: 2

   how-to
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

