+++++++++++++++++++++
Install python-ptrace
+++++++++++++++++++++

Linux packages
==============

* Debian: `python-ptrace Debian package <http://packages.qa.debian.org/p/python-ptrace.html>`_.
* Mandriva: `python-ptrace Mandriva package <http://sophie.zarb.org/rpmfind?search=python-ptrace&st=rpmname>`_
* OpenEmbedded: `python-ptrace recipe <http://git.openembedded.net/?p=org.openembedded.dev.git;a=tree;f=packages/python>`_
* Arch Linux: `python-ptrace Arch Linux package <http://aur.archlinux.org/packages.php?ID=19609>`_
* Gentoo: `dev-python/python-ptrace <http://packages.gentoo.org/package/dev-python/python-ptrace>`_

See also `python-ptrace on Python Package Index (PyPi) <http://pypi.python.org/pypi/python-ptrace>`_

Install from source
===================

Download tarball
----------------

`Download python-ptrace-0.7.tar.gz
<http://pypi.python.org/packages/source/p/python-ptrace/python-ptrace-0.7.tar.gz>`_:

Download the development version using Mercurial::

    hg clone https://bitbucket.org/haypo/python-ptrace

`Browse python-ptrace source code
<https://bitbucket.org/haypo/python-ptrace/src/>`_.


python-ptrace dependencies
--------------------------

* Python 2.5+:
  http://python.org/
* distorm disassembler (optional)
  http://www.ragestorm.net/distorm/


Installation
------------

Type as root::

   python setup.py install

Or using sudo program::

   sudo python setup.py install


cptrace
=======

For faster debug and to avoid ctypes, you can also install cptrace: Python
binding of the ptrace() function written in C::

    python setup_cptrace.py install

