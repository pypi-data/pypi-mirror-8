"""
This package is an abstraction layer over the various different Qt bindings
for python (PyQt5, PyQt4 and PySide).

It mimics the structure of PyQt5 but let you choose the binding to use through
the ``QT_API`` environment variable.

PyQt5
~~~~~

For pyqt5, you don't have to set anything

>>>from pyqode.qt import QtGui, QtWidgets, QtCore
>>>print(QtWidgets.QWidget)

PyQt4
~~~~~

Set the QT_API environment variable to 'PyQt4' (case insensitive)

>>>import os
>>>os.environ['QT_API'] = 'PyQt4'
>>>from pyqode.qt import QtGui, QtWidgets, QtCore
>>>print(QtWidgets.QWidget)

PySide
~~~~~~

Set the QT_API environment variable to 'PySide' (case insensitive)

>>>import os
>>>os.environ['QT_API'] = 'PyQt4'
>>>from pyqode.qt import QtGui, QtWidgets, QtCore
>>>print(QtWidgets.QWidget)


The role of this module is to check ``QT_API`` based on the available bindings.
"""
import os
import sys
import logging

__version__ = '1.1.0'


QT_API = 'QT_API'
PYQT5_API = 'pyqt5'
PYQT4_API = 'pyqt4'
PYSIDE_API = 'pyside'


class PythonQtError(Exception):
    pass

def setup_apiv2():
    """
    Setup apiv2 on the chose binding.
    """
    # setup PyQt api to version 2
    if sys.version_info[0] == 2:
        try:
            import sip
            sip.setapi("QString", 2)
            sip.setapi("QVariant", 2)
        except:
            logging.getLogger(__name__).critical(
                "pyQode: failed to set PyQt api to version 2"
                "\nTo solve this problem, import "
                "pyqode before any other PyQt modules "
                "in your main script...")


if QT_API not in os.environ:
    # autodetect
    try:
        import PyQt5
        os.environ[QT_API] = PYQT5_API
    except ImportError:
        try:
            import PyQt4
            os.environ[QT_API] = PYQT4_API
        except ImportError:
            try:
                import PySide
                os.environ[QT_API] = PYSIDE_API
            except ImportError:
                raise PythonQtError('No Qt bindings could be found')
else:
    # check
    try:
        if os.environ[QT_API].lower() == PYQT5_API.lower():
            from pyqode.qt import *
            os.environ[QT_API] = PYQT5_API
        elif os.environ[QT_API].lower() == PYQT4_API.lower():
            setup_apiv2()
            from PyQt4 import *
            os.environ[QT_API] = PYQT4_API
        elif os.environ[QT_API].lower() == PYSIDE_API.lower():
            from PySide import *
            os.environ[QT_API] = PYSIDE_API
    except ImportError:
        raise PythonQtError('Cannot import %s' % os.environ[QT_API])

logging.getLogger(__name__).info('using %s' % os.environ[QT_API])
