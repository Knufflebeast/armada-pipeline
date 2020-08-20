"""
Module for main TasksWebView

The TasksWebView is a task level context where users can view their project management tasks
"""
import json
import os
import sys

from Qt import QtCore
from Qt import QtWidgets

from PySide2 import QtCore, QtGui, QtNetwork, QtWidgets

from packages import launcher

import utilsa
logging = utilsa.Logger('armada')
logger = logging.getLogger(__name__)

settings = QtCore.QSettings("ralsina", "devicenzo")


class TasksWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TasksWidget, self).__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)

        self.tabs = QtWidgets.QTabWidget(self, tabsClosable=True, movable=True, elideMode=QtCore.Qt.ElideRight)
        self.tabs.setCornerWidget(
            QtWidgets.QToolButton(
                self,
                text="New Tab",
                icon=QtGui.QIcon.fromTheme("document-new"),
                clicked=lambda: self.addTab().url.setFocus(),
                shortcut=QtGui.QKeySequence.AddTab,
            )
        )
        self.bars = {}

        self.close_current_tab = QtWidgets.QAction(shortcut=QtGui.QKeySequence.Close)
        self.addAction(self.close_current_tab)

        # Layout
        # self.setCentralWidget(self.tabs)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Connections
        self.tabs.tabCloseRequested.connect(lambda idx: self.tabs.widget(idx).deleteLater())
        self.tabs.currentChanged.connect(self.currentTabChanged)
        self.close_current_tab.triggered.connect(lambda: self.tabs.currentWidget().deleteLater())

        self.history = self.get("history", []) #+ list(self.bookmarks.keys())
        self.completer = QtWidgets.QCompleter(self.history)

        # Proxy support
        proxy_url = QtCore.QUrl(os.environ.get("http_proxy", ""))
        QtNetwork.QNetworkProxy.setApplicationProxy(
            QtNetwork.QNetworkProxy(
                QtNetwork.QNetworkProxy.HttpProxy
                if proxy_url.scheme().startswith("http")
                else QtNetwork.QNetworkProxy.Socks5Proxy,
                proxy_url.host(),
                proxy_url.port(),
                proxy_url.userName(),
                proxy_url.password(),
            )
        ) if "http_proxy" in os.environ else None

        [self.addTab(QtCore.QUrl(u)) for u in self.get("tabs", [])]

        # First time startup tabs
        for url in sys.argv[1:]:
            self.addTab(QtCore.QUrl.fromUserInput(url))
        if self.tabs.count() == 0:
            self.addTab(QtCore.QUrl("https://app.asana.com/0/home/1118084657117470"))

    def finished(self):
        url = self.sender().url().toString()
        bar, reply, fname, cancel = self.bars[url]
        redirURL = reply.attribute(
            QtNetwork.QNetworkRequest.RedirectionTargetAttribute
        ).toString()
        del self.bars[url]
        bar.deleteLater()
        cancel.deleteLater()
        if redirURL and redirURL != url:
            return self.fetch(redirURL, fname)

        with open(fname, "wb") as f:
            f.write(str(reply.readAll()))

    def closeEvent(self, ev):
        self.put("history", self.history)
        self.put(
            "tabs", [self.tabs.widget(i).url.text() for i in range(self.tabs.count())]
        )
        return QtWidgets.QMainWindow.closeEvent(self, ev)

    def put(self, key, value):
        "Persist an object somewhere under a given key"
        settings.setValue(key, json.dumps(value))
        settings.sync()

    def get(self, key, default=None):
        "Get the object stored under 'key' in persistent storage, or the default value"
        v = settings.value(key)
        return json.loads(v) if v else default

    def addTab(self, url=QtCore.QUrl("")):
        self.tabs.setCurrentIndex(self.tabs.addTab(launcher.tasks_tab.TasksTab(url, self), ""))
        return self.tabs.currentWidget()

    def currentTabChanged(self, idx):
        if self.tabs.widget(idx) is None:
            return self.close()

        self.setWindowTitle(self.tabs.widget(idx).web_view.title() or "De Vicenzo")

    def addToHistory(self, url):
        self.history.append(url)
        self.completer.setModel(
            QtCore.QStringListModel(
                list(set(list(self.history))) #self.bookmarks.keys()) +
            )
        )
