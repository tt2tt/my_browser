from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl("https://www.google.com")
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)
