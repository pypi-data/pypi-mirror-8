Vai
===

.. image:: https://travis-ci.org/stefanoborini/vai.svg?branch=master
   :target: https://travis-ci.org/stefanoborini/vai
   :alt: Build status
.. image:: https://pypip.in/download/vai/badge.png
   :target: https://pypi.python.org/pypi/vai/
   :alt: Downloads
.. image:: https://pypip.in/py_versions/vai/badge.svg
   :target: https://pypi.python.org/pypi/vai/
   :alt: Supported Python versions
.. image:: https://pypip.in/version/vai/badge.png
   :target: https://pypi.python.org/pypi/vai/
   :alt: Latest version
.. image:: https://landscape.io/github/stefanoborini/vai/master/landscape.png
   :target: https://landscape.io/github/stefanoborini/vai
   :alt: Latest version
.. image:: http://img.shields.io/gratipay/StefanoBorini.svg
   :target: https://gratipay.com/StefanoBorini/
   :alt: gratipay
   
We love vim, but we want more. We want a terminal-based IDE that looks like vim,
handles like vim, but has all those nice features of Eclipse and Sublime, is
integrated with git, and is fully coded in python. 

   - `Implemented Features`_
   - `Screenshots`_
   - `Release Notes`_
   - `Download`_
   - `Contributors`_
   - `Rationale, Development methodology and planned features`_


Implemented Features
--------------------

   - General vim look and feel.
   - Syntax highlighting for python. Partial support for other languages.
   - Highlighting of all occurrences of the identifier currently under the cursor.
   - Linting for python 3 with pyflakes
   - Shows linting results on the sidebar. Linting messages popup inline.
   - Backward and forward search (no regexp yet)
   - Tab completion for editor and command bar (while accessing files)
   - Undo/Redo
   - Indentation levels
   - Multiple buffers
   - Copying and pasting (only of a single line)
   - Minimal configuration of colors
   - Cursor position restored between runs.
   - Autoindent

Note: vai is currently focused mostly on Python editing. Future additions will handle other languages.

Screenshots
-----------

Vai 1.4

.. image:: https://github.com/stefanoborini/vai/blob/master/static/images/screenshot-1.4.png

Vai 1.2/1.3

.. image:: https://github.com/stefanoborini/vai/blob/master/static/images/screenshot-1.2.gif

Vai 1.1

.. image:: https://github.com/stefanoborini/vai/blob/master/static/images/screenshot-1.1.png

Release Notes
-------------

Vai 1.4
~~~~~~~

   - Unicode icons for the Side Ruler. Can be disabled with appropriate setting in the .config/vai/vairc file.
   - Command line option ``--dump-default-config`` to create a default vairc file.
   - Dumping of current open buffers in case of crash.
   - More performance improvements.
   - Now tooltip messages don't stay when you move around or start typing.
   - Parentheses are no longer removed when using ``dw``
   - Improved color schema
   - Implemented vim movements ``hjkl``
   - Removing leading spaces when breaking a line.
   - Implemented :x to write and quit.
   - Implementation of XDG Base Directory Specification.
   - Command bar tabbing autocompletes filenames and directory names.
   - Markers added when a line is deleted.
   - Refactorings
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=is%3Aissue+milestone%3Av1.4+is%3Aclosed+label%3ABug>`_

Vai 1.3
~~~~~~~

   - Deleting to end of word should also delete the spaces following it.
   - Implemented redo with Ctrl+R
   - :r command to read and include a file
   - Performance improvements
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=is%3Aissue+milestone%3Av1.3+is%3Aclosed+label%3ABug>`_

Vai 1.2
~~~~~~~

   - Reset optimistic column when adding new line.
   - Indentation markers proof of concept.
   - Restore cursor position at load
   - Introduced ZZ command
   - Initial Configuration file infrastructure. Basic colors of StatusBar/SideRuler can be changed.
   - Handle long filenames in StatusBar
   - Major refactoring of the MVC structure
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=milestone%3Av1.2+label%3ABug>`_

Vai 1.1
~~~~~~~

   - Highlight of False/True  
   - Change name to prevent issues with Vix video editor
   - Highlighting of current identifier 
   - copy/cut/paste (single line)
   - Hovering tooltip
   - Replace commands
   - Delete word 
   - Asterisk search
   - Add ^N ^P as shortcuts for buffer nav 
   - Delete tabspaces on backspace
   - Autoindent
   - Tab completion
   - Solved color difference on Mac vs Linux
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=milestone%3Av1.1+label%3ABug>`_

Vai 1.0
~~~~~~~

   - First release

Download
--------

You can get the latest version of vai from `pypi
<https://pypi.python.org/pypi/vai>`_, either manually
or via pip

   pip3.4 install vai

**Important Note**: you need python 3.4. Python 3.3 will not work. 

Rationale, Development methodology and planned features
-------------------------------------------------------

You can read about the rationale behind vai, the development
strategy, and additional information on the `RATIONALE <https://github.com/stefanoborini/vai/blob/master/RATIONALE.rst>`_ 
document.


Contributors
------------

Main development:
- Stefano Borini

Additional contributes:
- `Carl George (cgtx) <https://github.com/cgtx>`_

Testing:
- Maicon Lourenco


