==========================
:mod:`domplotlib.styles`
==========================

Each of these styles expose ``plt``, which is an alias of :mod:`matplotlib.pyplot`. Importing one of these styles configures matplotlib to use the desired style.

The styles currently available are:

* ``default`` -- The default matplotlib style. Forces the backend to be ``TkAgg`` if ``tkinter`` is available.
* ``domdf`` -- A theme adapted from ``Solarize_Light2``.

.. note::

	Importing a style for a second time will not change the current style.
	Use :func:`importlib.reload` to reload the module after importing to ensure the style is correctly set.
