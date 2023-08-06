dalmatian
=========

Visualizing a confusion matrix with gradations.

Installation
------------

::

    pip install dalmatian

Usage
-----

.. code:: python

    import numpy as np
    import dalmatian

    labels = ["ostrich", "swallow", "cuckoo", "chicken", "quail"]
    data = np.array([
      [50, 0, 0, 0, 0],
      [1, 41, 5, 3, 0],
      [2, 9, 34, 4, 1],
      [1, 1, 8, 38, 2],
      [1, 0, 2, 3, 44],
      ])

    mx = dalmatian.Matrix(labels, data)

    #Options
    mx.cell_size = 10.0 #[mm]
    mx.font_size = 14
    mx.label_font_size = 7
    mx.cell_color = "black" #black, red, yellow, green, blue, purple
    mx.label_color = "black" #black, white
    mx.line_type = "normal" #normal, dot
    mx.percentage = False

    mx.draw()

.. figure:: https://dl.dropboxusercontent.com/u/12208857/img/SIGraphocsKit_matrix_ss.png
   :alt: 


