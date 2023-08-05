# -*- coding: utf-8 -*-
"""
This scripts configures the test suite. We do two things:

    - setup the logging module
    - create ONE SINGLE INSTANCE of QApplication:
      this implies that you must use **QApplication.instance** in your
      test scripts.
"""
import logging
import os
import sys
import pytest


try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    pass


# -------------------
# Setup runtest
# -------------------
def pytest_runtest_setup(item):
    """
    Display test method name in active window title bar
    """
    global _widget
    module, line, method = item.location
    module = module.replace('.py', '.')
    title = module + method
    widgets = QApplication.instance().topLevelWidgets()
    for w in widgets:
        w.setWindowTitle(title)
    logging.info("------------------- %s -------------------", title)

# -------------------
# Setup logging
# -------------------
logging.basicConfig(level=logging.DEBUG,
                    filename='pytest.log',
                    filemode='w')

# -------------------
# Setup QApplication
# -------------------
# 2. create qt application
from pyqode.qt.QtWidgets import QApplication
_app = QApplication(sys.argv)
_widget = None


# -------------------
# Session fixtures
# -------------------
@pytest.fixture(scope="session")
def app(request):
    global _app
    return app


@pytest.fixture(scope="session")
def editor(request):
    global _app, _widget
    from pyqode.core import modes
    from pyqode.python.widgets.code_edit import PyCodeEdit
    from pyqode.python.backend import server
    from pyqode.qt.QtTest import QTest

    logging.info('################ setup session editor ################')

    _widget = PyCodeEdit()
    _widget.backend.start(server.__file__)
    _widget.resize(800, 600)
    _widget.show()
    _app.setActiveWindow(_widget)
    while not _widget.backend.connected:
        QTest.qWait(100)

    _widget.modes.get(modes.FileWatcherMode).file_watcher_auto_reload = True
    _widget.save_on_focus_out = False

    def fin():
        global _widget
        logging.info('################ teardown session editor ###############'
                     '#')
        _widget.backend.stop()
        while _widget.backend.connected:
            QTest.qWait(100)
        del _widget

    request.addfinalizer(fin)

    return _widget
