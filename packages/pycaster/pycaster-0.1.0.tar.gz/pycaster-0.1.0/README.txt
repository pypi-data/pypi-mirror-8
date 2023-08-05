pycaster
========

|wercker status|

Background
----------

``pycaster`` is a simple single-module package (module also called
``pycaster``) which contains a ``rayCaster`` class. This class allows
for ray-casting operations to be performed on any mesh represented by a
'vtkPolyData' object.

The ``rayCaster`` class acts as a wrapper of the ``vtkOBBTree`` class
and uses perform ray-casting. It can calculate the coordinates of the
entry/exit points between the ray and the surface. It can in addition
calculate the distance a ray travels within the closed section of the
surface, i.e., within the solid.

The class features a static method 'fromSTL' which allows for it to be
initialized directly from an STL file which it loads and extracts the
polydata from initializing the ray-caster.

Documentation
-------------

No extensive documentation of ``pycaster`` was written due to its
simplicity.

Examples: IPython Notebooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two IPython Notebooks were written demonstrating the usage of
``pycaster`` on STL models:

-  A notebook demonstrating the usage of ``pycaster`` on the STL model
   of a hollow sphere can be found
   `here <http://nbviewer.ipython.org/urls/bitbucket.org/somada141/pyscience/raw/master/20140910_RayCasting/Material/PythonRayCastingSpherePyCaster.ipynb>`__
   (with the STL file being available
   `here <https://bitbucket.org/somada141/pyscience/raw/master/20140910_RayCasting/Material/sphereHollow.stl>`__).
-  A very similar notebook to the above, with the sole exception being
   operating on the STL model of a human skull extracted from CT data
   can be found
   `here <http://nbviewer.ipython.org/urls/bitbucket.org/somada141/pyscience/raw/master/20140910_RayCasting/Material/PythonRayCastingSkullPyCaster.ipynb>`__
   while the corresponding STL file is available
   `here <https://bitbucket.org/somada141/pyscience/raw/master/20140910_RayCasting/Material/bones.stl>`__.

Usage Example
-------------

In a nutshell using ``pycaster`` it would go as such:

::

    from pycaster import pycaster

    # Create a new rayCaster object through the 'fromSTL' static-method thus loading
    # the STL file 'sphereHollow.stl' and creating a new rayCaster under 'caster'
    caster = pycaster.rayCaster.fromSTL("sphereHollow.stl", scale=1.0)

    # Set the source and target coordinate of the ray
    pSource = [-50.0, 0.0, 0.0]
    pTarget = [50.0, 0.0, 0.0]

    # Use the 'castRay' method of the 'rayCaster' class to intersect a ray/line with
    # the surface and return a list of coordinates, i.e., the intersection points
    pointsIntersection = caster.castRay(pSource, pTarget)

    # Use the calcDistanceInSolid to calculate the distance the ray 'travels' within
    # the surface
    caster.calcDistanceInSolid(pSource, pTarget)

Requirements
------------

vtk >= 5.10.1 nose >= 1.3.3

Python 3.x Support
~~~~~~~~~~~~~~~~~~

At the time of writing ``pycaster`` cannot function with Python 3.x as
the VTK Python bindings have not been ported to Python 3.x. However,
``pycaster`` has been extensively tested with different Python 2.7.x
versions.

Installation
------------

This package is already hosted on PyPI
`here <https://pypi.python.org/pypi/pycaster>`__ and can be easily
installed through pip as such:

::

    pip install pycaster

or straight from the source-code using ``setuptools`` as such:

::

    python setup.py install

However, given the ``vtk`` requirement of ``pycaster`` which doesn't
always build easy with pip I strongly suggest the following:

-  Use an Anaconda python distro. I've written a blog post about the
   advantages it offers
   `here <pyscience.wordpress.com/2014/09/01/anaconda-the-creme-de-la-creme-of-python-distros-3/>`__.
-  Install the dependencies with ``conda`` (see the aforementioned post)
-  Install ``pycaster`` with ``pip`` while skipping the dependencies as
   such:

::

    pip install pycaster --no-deps

Testing & CI
------------

``pycaster`` comes with tests written with ``unittest`` and
batch-executed with ``nose``. The distribution also comes with several
.stl files used for testing the different aspects of the package. After
installation you can easily run those tests from within a python session
with the following code:

::


    from pycaster.test import test_all
    test_all.runTests()

Every commit of ``pycaster`` is being built and tested on the
`Wercker <http://wercker.com/>`__ CI system. The application is public
and can be accessed through either clicking on the wercker badge at the
top of this page or through
`this <https://app.wercker.com/#applications/540d1c16a5aa911015000f87>`__
link.

.. |wercker status| image:: https://app.wercker.com/status/fa548d6a19af54cd14cec18310ac0844/m
   :target: https://app.wercker.com/project/bykey/fa548d6a19af54cd14cec18310ac0844
