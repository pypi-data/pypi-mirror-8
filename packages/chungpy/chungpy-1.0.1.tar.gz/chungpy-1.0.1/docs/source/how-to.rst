==============
Chunpy: How-to
==============

Use module ``chungpy.mdsp`` for computation of Maximum Density Segments exclusively.

Input persists of at least value vector `a` and width vector `w` which can be of type `list` or `numpy <http://www.numpy.org/>`_ `array`.

Note, that `a` and `w` have to be of identical length and all elements of `w` have to be greater than 0.

The corresponding MDSP is solved in concurrence with the instantiation of the problem instance.

.. code-block:: python

   import chungpy
   
   m=chungpy.mdsp([1,-5,12,7,-12], [2,14,3,7,6])
   print(m)

yields the following output

.. code-block:: text

   # Overview
   a = [1.0, -5.0, 12.0, 7.0, -12.0]
   w = [2.0, 14.0, 3.0, 7.0, 6.0]
   length = 5
   min/max content = 1,5
   min/max width = 1,inf

   # Maximum Density Segment per Position
   1 -> 1, c=1, w=2.0, d=0.5
   1 -> 2, c=2, w=16.0, d=-0.25
   3 -> 3, c=1, w=3.0, d=4.0
   3 -> 4, c=2, w=10.0, d=1.9
   3 -> 5, c=3, w=16.0, d=0.4375

   # Maximum Density Segment(s)
   3 -> 3, c=1, w=3.0, d=4.0


Define width constraints :math:`w_{min}` and :math:`w_{max}` via attributes ``min_width`` and ``max_width`` and content constraints :math:`c_{min}` and :math:`c_{max}` 
via attributes ``min_cont`` and ``max_cont``.

.. code-block:: python

   m=chungpy.mdsp([1,-5,12,7,-12], [2,14,3,7,6], max_width=20, min_cont=2)
   print(m)

yields the following output

.. code-block:: text

   # Overview
   a = [1.0, -5.0, 12.0, 7.0, -12.0]
   w = [2.0, 14.0, 3.0, 7.0, 6.0]
   length = 5
   min/max content = 2,5
   min/max width = 1,20

   # Maximum Density Segment per Position
   1 -> 2, c=2, w=16.0, d=-0.25
   1 -> 3, c=3, w=19.0, d=0.42105263157894735
   3 -> 4, c=2, w=10.0, d=1.9
   3 -> 5, c=3, w=16.0, d=0.4375

   # Maximum Density Segment(s)
   3 -> 4, c=2, w=10.0, d=1.9

The set of stop indices of maximum density segments can be accessed via attribute ``result_inds`` and the corresponding maximum density can be accessed via ``max_dens``. 

Local maximum density segments, i.e. start indices of the shortest segments with highest possible density stopping at each posssible stop index :math:`j'` can be accessed via attribute ``result_inds`` of type ``dict``.
Of course, the keys in ``result_inds`` does only contain stop indices of segments fullfilling the given width and content constraints.

Width and density of arbitrary segments of the given problem instance can be computed via methods ``width`` and ``density``. Note, that start and stop indices are 1-based and stop index :math:`j` is inclusively.

The following code snippet returns the densities of all local maximum density segments of MDSP instance ``m``:

.. code-block:: python

   [m.dens(m.result_inds[j],j) for j in m.result_inds]




Use module ``chungpy.mmdsp`` for simultaneous computation of Maximum and Minimum Density Segments.

.. code-block:: python

   import chungpy
   
   m=chungpy.mmdsp([1,-5,12,7,-12], [2,14,3,7,6])
   print(m)

yields the following output

.. code-block:: text

   # Overview
   a = [1.0, -5.0, 12.0, 7.0, -12.0]
   w = [2.0, 14.0, 3.0, 7.0, 6.0]
   length = 5
   min/max content = 2,5
   min/max width = 1,20

   # Maximum Density Segment per Position
   1 -> 2, c=2, w=16.0, d=-0.25
   1 -> 3, c=3, w=19.0, d=0.42105263157894735
   3 -> 4, c=2, w=10.0, d=1.9
   3 -> 5, c=3, w=16.0, d=0.4375

   # Maximum Density Segment(s)
   3 -> 4, c=2, w=10.0, d=1.9

   # Minimum Density Segment per Position
   1 -> 2, c=2, w=16.0, d=-0.25
   2 -> 3, c=2, w=17.0, d=0.4117647058823529
   3 -> 4, c=2, w=10.0, d=1.9
   4 -> 5, c=2, w=13.0, d=-0.38461538461538464

   # Minimum Density Segment(s)
   4 -> 5, c=2, w=13.0, d=-0.38461538461538464

The set of stop indices of minimum density segments can be accessed via attribute ``min_result_inds`` and the corresponding minimum density can be accessed via ``min_dens``. 

Local minimum density segments, i.e. start indices of the shortest segments with lowest possible density stopping at each posssible stop index :math:`j'` can be accessed via attribute ``min_result_inds`` of type ``dict``.


