matlab_wrapper
==============

*MATLAB wrapper for Python*


:Name: matlab_wrapper
:Author: Marek Rudnicki
:Email: marekrud@gmail.com
:URL: https://github.com/mrkrd/matlab_wrapper
:License: GNU General Public License v3 or later (GPLv3+)



Description
-----------

*matlab_wrapper* allows you to use MATLAB in a convenient way in
Python.  You can call MATLAB functions and access workspace variables
directly from your Python scripts and interactive shell.  MATLAB
session is started in the background and appears as a regular Python
module.

*matlab_wrapper* talks to `MATLAB engine library`_ using ctypes_, so
you do not have to compile anything!

Numerical, logical, struct and cell arrays are supported.


.. _`MATLAB engine library`: http://www.mathworks.com/help/matlab/matlab_external/introducing-matlab-engine.html
.. _ctypes: https://docs.python.org/2/library/ctypes.html




Usage
-----

Initialize::

  import matlab_wrapper
  matlab = matlab_wrapper.MatlabSession()


Low level::

  matlab.put('a', 12.3)
  matlab.eval('b = a * 2')
  b = matlab.get('b')


Workspace::

  s = matlab.workspace.sin([0.1, 0.2, 0.3])

  sorted,idx = matlab.workspace.sort([3,1,2], nout=2)

  matlab.workspace.a = 12.3
  b = matlab.workspace.b


More examples are in the examples_ directory!

.. _examples: https://github.com/mrkrd/matlab_wrapper/tree/master/examples


Requirements
------------

- Python (2.7)
- Matlab (various versions)
- Numpy (1.8)



Platforms
---------

If you are using *matlab_wrapper* with MATLAB version and OS not
listed below, please let us know and we will update the table.

==========  ===========  ==========  ==========
OS [#os]_   MATLAB       Bits [#b]_  Status
==========  ===========  ==========  ==========
GNU/Linux   2014b (8.4)  64          working (py.test OK)
GNU/Linux   2014a (8.3)  64          only double arrays working [#f]_
GNU/Linux   2013b (8.2)  64          working (py.test OK)
GNU/Linux   2013a (8.1)  64          working (py.test OK)

Windows     2014b (8.4)  32          reported working
Windows     2014a (8.3)  64          working (py.test OK)

OS X        2014a (8.3)  64          only double arrays working [#f]_
OS X        2013a (8.1)  64          working
==========  ===========  ==========  ==========


.. [#os] OSX version should work, but I'm unable to test it.  If you
         have problems, let me know and we might figure it out.

.. [#b] I have tested only 64-bit systems.  32-bit architectures are
        enabled, but not well tested.

.. [#f] Due to bug in ``engGetVariable``: Error using save, Can't
        write file stdio.


Installation
------------

::

   pip install matlab_wrapper




Issues and Bugs
---------------

https://github.com/mrkrd/matlab_wrapper/issues

When reporting problems, specify which Python (version, architecture,
distribution), MATLAB (version, architecture) and OS (version,
architecture) are you using.


Alternatives
------------

(last updated on June 17, 2014)

- pymatlab_

  - pure Python, no compilation, using ctypes (good)
  - quite raw (ugly)
  - memory leaks (bad)

- mlabwrap_

  - cool interface, mlab.sin() (good)
  - needs compilation (bad)
  - not much development (bad)

- mlab_

  - similar interface to mlabwrap (good)
  - using raw pipes (hmm)
  - there is another very old package with `the same name
    <http://claymore.engineer.gvsu.edu/~steriana/Python/pymat.html>`_
    (ugly)

- pymatbridge_

  - actively developed (good)
  - client-server architecture with ZeroMQ and JSON, complex (ugly)
  - missing basic functions, there's no ``put`` (bad)
  - nice ipython notebook support (good)



Note: There is a nice overview of the `available packages`_ at
StackOverflow.


.. _mlabwrap: http://mlabwrap.sourceforge.net/
.. _mlab: https://github.com/ewiger/mlab
.. _pymatbridge: https://github.com/arokem/python-matlab-bridge
.. _`available packages`: https://stackoverflow.com/questions/2883189/calling-matlab-functions-from-python/23762412#23762412


Acknowledgments
---------------

*matlab_wrapper* was forked from pymatlab_.

MATLAB is a registered trademark of `The MathWorks, Inc`_.

.. _pymatlab: http://pymatlab.sourceforge.net/
.. _`The MathWorks, Inc`: http://www.mathworks.com/
