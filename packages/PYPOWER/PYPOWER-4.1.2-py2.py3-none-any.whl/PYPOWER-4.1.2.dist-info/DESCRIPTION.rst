============
Introduction
============

PYPOWER is a power flow and Optimal Power Flow (OPF) solver. It is a port of
MATPOWER_ to the Python_ programming language. Current
features include:

* DC and AC (Newton's method & Fast Decoupled) power flow and
* DC and AC optimal power flow (OPF)


Installation
============

PYPOWER depends upon:

* Python_ 2.6 or later and
* SciPy_ 0.9 or later.

It can be installed using pip_::

  $ pip install PYPOWER

Alternatively, `download <http://pypi.python.org/pypi/PYPOWER#downloads>`_ and
unpack the tarball and install::

  $ tar zxf PYPOWER-4.x.y.tar.gz
  $ python setup.py install


Using PYPOWER
=============

Installing PYPOWER creates ``pf`` and ``opf`` commands. To list the command
options::

  $ pf -h

PYPOWER includes a selection of test cases. For example, to run a power flow
on the IEEE 14 bus test case::

  $ pf -c case14

Alternatively, the path to a PYPOWER case data file can be specified::

  $ pf /path/to/case14.py

The ``opf`` command has the same calling syntax. For example, to solve an OPF
for the IEEE Reliability Test System and write the solved case to file::

  $ opf -c case24_ieee_rts --solvedcase=rtsout.py

For further information please refer to http://www.pypower.org/ and the
`API documentation`_.


Support
=======

Questions and comments regarding PYPOWER should be directed to the `mailing
list <http://groups.google.com/group/pypower>`_:

    pypower@googlegroups.com


License & Copyright
===================

Copyright (C) 1996-2011 Power System Engineering Research Center

Copyright (C) 2010-2011 Richard Lincoln

This program is free software: you can redistribute it and/or modify
it under the terms of the `GNU General Public License`_ as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.


Links
=====

* MATPOWER_ from PSERC (Cornell)
* MatDyn_ by Stijn Cole
* PSAT_ by Federico Milano
* OpenDSS_ from EPRI
* GridLAB-D_ from PNNL
* PyCIM_

.. _Python: http://www.python.org
.. _pip: https://pip.pypa.io
.. _SciPy: http://www.scipy.org
.. _MATPOWER: http://www.pserc.cornell.edu/matpower/
.. _Git: http://git-scm.com/
.. _GitHub: http://github.com/rwl/PYPOWER
.. _`GNU General Public License`: http://www.gnu.org/licenses/
.. _`API documentation`: http://www.pypower.org/api
.. _PyCIM: http://www.pycim.org
.. _MatDyn: http://www.esat.kuleuven.be/electa/teaching/matdyn/
.. _PSAT: http://www.uclm.es/area/gsee/web/Federico/psat.htm
.. _OpenDSS: http://sourceforge.net/projects/electricdss/
.. _GridLAB-D: http://sourceforge.net/projects/gridlab-d/


Changelog
=========

Version 4.1.2 (2014-10-27)
--------------------------

- [FIX] Fixed error in runopf() (`issue #11`_).
- [FIX] Fixed runpf.py with ENFORCE_Q_LIMS option (`pull request #13`_).

.. _`issue #11`: https://github.com/rwl/PYPOWER/issues/11
.. _`pull request #13`: https://github.com/rwl/PYPOWER/pull/13/


Version 4.1.1 (2014-09-17)
--------------------------

- [FIX] loadcase.py: Fixed NumPy 1.9 warning about "== None" comparisions.


Version 4.1.0 (2014-05-29)
--------------------------

- [NEW] Support for Python 3 (3.3 and above).
- [CHANGE] Updated to MATPOWER 4.1.
- [REMOVED] Support for Python 2.5 and below.


Version 4.0.1 (2011-07-14)
--------------------------

- [CHANGE] printpf.py: changed boolean operators from bitwise to logical to fix
  the output options

- [FIX] savecase.py: adding indentation to produce valid Python modules


Version 4.0.0 (2011-07-07)
--------------------------

Initial release, port of MATPOWER version 4.0


