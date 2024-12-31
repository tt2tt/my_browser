from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QPushButton, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.web_view = QWebEngineView()
        # 初期ページの設定
        self.web_view.setUrl("https://www.google.com")

        # PDF表示機能の有効化
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        # ツールバーを作成
        self.toolbar = QToolBar("メインツールバー")

        # 戻るボタン
        self.back_button = QPushButton("戻る")
        self.back_button.clicked.connect(self.web_view.back)
        self.toolbar.addWidget(self.back_button)

        # 進むボタン
        self.forward_button = QPushButton("進む")
        self.forward_button.clicked.connect(self.web_view.forward)
        self.toolbar.addWidget(self.forward_button)

        # 再読込みボタンを作成
        self.reload_button = QPushButton("再読み込み")
        self.reload_button.clicked.connect(self.reload_page)
        self.toolbar.addWidget(self.reload_button)

        # URLバー
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("URLを入力して下さい")
        self.url_bar.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_bar)

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.web_view)
        self.setLayout(self.layout)

    # URLの検索
    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.web_view.setUrl(QUrl(url))

    # 再読み込み
    def reload_page(self):
        self.web_view.reload()
