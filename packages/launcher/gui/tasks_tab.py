"""
Module for main TasksWebView

The TasksWebView is a task level context where users can view their project management tasks
"""

from Qt import QtCore
from Qt import QtWidgets

from PySide2 import QtCore, QtGui, QtWebEngineWidgets, QtWidgets

from utilsa import Logger
logging = Logger('armada')


class TasksTab(QtWidgets.QWidget):
    def __init__(self, url, container, parent=None):
        super(TasksTab, self).__init__(parent)

        self.container = container
        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.web_view.setContentsMargins(0, 0, 0, 0)
        # self.progress_bar = QtWidgets.QProgressBar(
        #     self.container.statusBar(), maximumWidth=120, visible=False
        # )
        # self.web_view.loadProgress.connect(
        #     lambda v: (self.progress_bar.show(), self.progress_bar.setValue(v))
        #     if self.amCurrent()
        #     else None
        # )
        # self.web_view.loadFinished.connect(self.progress_bar.hide)
        # self.web_view.loadStarted.connect(
        #     lambda: self.progress_bar.show() if self.amCurrent() else None
        # )
        self.web_view.titleChanged.connect(
            lambda t: container.tabs.setTabText(container.tabs.indexOf(self), t)
            or (container.setWindowTitle(t) if self.amCurrent() else None)
        )
        self.web_view.iconChanged.connect(
            lambda: container.tabs.setTabIcon(
                container.tabs.indexOf(self), self.web_view.icon()
            )
        )
        self.tb = QtWidgets.QToolBar("Main Toolbar", self)
        self.tb.setContentsMargins(0,0,0,0)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tb, stretch=0)
        layout.addWidget(self.web_view, stretch=1000)
        layout.activate()
        self.setLayout(layout)
        for a, sc in [
            [QtWebEngineWidgets.QWebEnginePage.Back, QtGui.QKeySequence.Back],
            [QtWebEngineWidgets.QWebEnginePage.Forward, QtGui.QKeySequence.Forward],
            [QtWebEngineWidgets.QWebEnginePage.Reload, QtGui.QKeySequence.Refresh],
        ]:
            self.tb.addAction(self.web_view.pageAction(a))
            self.web_view.pageAction(a).setShortcut(sc)

        def save_page(*a, view=self.web_view):
            destination = QtWidgets.QFileDialog.getSaveFileName(self, "Save Page")
            print(repr(destination))
            if destination:
                view.page().save(destination[0])

        self.web_view.pageAction(
            QtWebEngineWidgets.QWebEnginePage.SavePage
        ).triggered.connect(save_page)

        self.url = QtWidgets.QLineEdit()
        self.url.returnPressed.connect(
            lambda: self.web_view.load(QtCore.QUrl.fromUserInput(self.url.text()))
        )
        self.url.setCompleter(container.completer)
        self.tb.addWidget(self.url)
        # self.tb.addAction(container.star_action)

        self.web_view.urlChanged.connect(lambda u: self.url.setText(u.toString()))
        self.web_view.urlChanged.connect(lambda u: container.addToHistory(u.toString()))
        # self.web_view.urlChanged.connect(
        #     lambda u: container.star_action.setChecked(
        #         u.toString() in container.bookmarks
        #     )
        #     if self.amCurrent()
        #     else None
        # )

        # self.web_view.page().linkHovered.connect(
        #         #     lambda l: container.statusBar().showMessage(l, 3000)
        #         # )

        self.search = QtWidgets.QLineEdit(
            self.web_view, visible=False, maximumWidth=200
        )
        self.search.returnPressed.connect(
            lambda: self.web_view.findText(self.search.text())
        )
        self.search.textChanged.connect(
            lambda: self.web_view.findText(self.search.text())
        )
        self.showSearch = QtWidgets.QShortcut(QtGui.QKeySequence.Find, self)
        self.showSearch.activated.connect(
            lambda: self.search.show() or self.search.setFocus()
        )
        self.hideSearch = QtWidgets.QShortcut(
            "Esc", self, activated=lambda: (self.search.hide(), self.setFocus())
        )

        self.zoomIn = QtWidgets.QShortcut(QtGui.QKeySequence.ZoomIn, self)
        self.zoomIn.activated.connect(
            lambda: self.web_view.setZoomFactor(self.web_view.zoomFactor() + 0.2)
        )
        self.zoomOut = QtWidgets.QShortcut(QtGui.QKeySequence.ZoomOut, self)
        self.zoomOut.activated.connect(
            lambda: self.web_view.setZoomFactor(self.web_view.zoomFactor() - 0.2)
        )
        self.zoomOne = QtWidgets.QShortcut(
            "Ctrl+0", self, activated=lambda: self.web_view.setZoomFactor(1)
        )
        self.urlFocus = QtWidgets.QShortcut("Ctrl+l", self, activated=self.url.setFocus)

        # Todo: reimplement printing
        # self.previewer = QtWidgets.QPrintPreviewDialog(paintRequested=self.web_view.print_)
        # self.do_print = QtWidgets.QShortcut("Ctrl+p", self, activated=self.previewer.exec_)
        # self.web_view.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        # self.web_view.settings().setIconDatabasePath(tempfile.mkdtemp())

        self.web_view.load(url)

    def amCurrent(self):
        return self.container.tabs.currentWidget() == self

    def createWindow(self, windowType):
        return self.container.addTab()
