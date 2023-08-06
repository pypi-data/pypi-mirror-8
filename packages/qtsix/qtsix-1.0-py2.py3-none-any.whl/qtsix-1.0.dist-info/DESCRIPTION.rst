QtSix provides a compatibility layer that allows to write Python
applications that work with different Qt bindings: PyQt5, PyQt4 or
PySide.

An application that used QtSix can work correctly if any of the
supported Qt bindings is installed on the system.
QtSix automatically detects available bindings and uses them
transparently.

If more than one Qt_ binding is present on the system then it is selected
the first one available in the following order: PyQt5, PyQt4, PySide.



